# Cortex-M HardFault Skill 设计文档

## 1. 目标

设计一个面向 `Cortex-M` 系列的通用 `HardFault` 排查 skill，让 Codex 在遇到如下请求时能够稳定工作：

- 分析 `HardFault` / `MemManage` / `BusFault` / `UsageFault`
- 根据寄存器转储、异常栈帧、反汇编、链接映射文件定位故障点
- 指导用户在 `Keil / IAR / GCC / STM32CubeIDE / J-Link / OpenOCD` 等环境中补齐关键信息
- 对不同内核能力差异做分层处理，而不是把 `M3/M4/M7` 的寄存器模型硬套到所有 `Cortex-M`

该 skill 的核心价值不是“讲概念”，而是把 HardFault 诊断过程工程化、可复用化。

## 2. 主要参考

### 2.1 用户指定博客

- Yuxxxxxxxxxx，《Cortex-M3/M4/M7 芯片 Fault 分析原理与实战》
  - 链接：<https://yuxxxxxxxxxx.github.io/2024/10/07/Cortex-M3-M4-M7-%E8%8A%AF%E7%89%87-Fault-%E5%88%86%E6%9E%90%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E6%88%98/>

从该博客吸收的设计要点：

- `HardFault` 经常是 `MemManage / BusFault / UsageFault` 升级而来，必须优先检查 `HFSR.FORCED`
- `CFSR` 是主诊断入口，应继续拆解 `MMFSR / BFSR / UFSR`
- `MMFAR / BFAR` 只有在有效位成立时才可信
- `EXC_RETURN(LR)` 用于判断异常前使用的是 `MSP` 还是 `PSP`
- 自动入栈寄存器为 `R0/R1/R2/R3/R12/LR/PC/xPSR`
- `M7` 需要额外考虑 `ABFSR`
- `STKERR / UNSTKERR / MSTKERR / MUNSTKERR` 这类位通常意味着“栈本身或异常进出栈过程”有问题，不能只盯着 `PC`

### 2.2 辅助参考

- Arm CMSIS Core Register Mapping
  - <https://arm-software.github.io/CMSIS_6/latest/Core/regMap_pg.html>
- Arm CMSIS-View Fault Analysis
  - <https://arm-software.github.io/CMSIS-View/latest/fault.html>

引入这些辅助参考的原因：

- 用来约束架构差异，尤其是 `Cortex-M0/M0+` 没有完整 `CFSR/HFSR/MMFAR/BFAR` 这套能力
- 用来保证 skill 不会把 `M3/M4/M7` 的排查流程错误推广到所有 M 内核

## 3. 设计原则

### 3.1 先分层支持，再统一入口

skill 对外统一叫 “Cortex-M HardFault 排查”，但内部必须按能力分层：

- `Tier A`：`Cortex-M3/M4/M7/M33` 等具备完整 fault status/address 寄存器的内核
- `Tier B`：`Cortex-M0/M0+` 等 fault 信息有限的内核
- `Tier C`：带 FPU 或安全扩展的变体，只在检测到相关证据时展开分析

### 3.2 先拿证据，再做推断

skill 不应该一上来猜“可能是栈溢出”。它必须先确认：

- 当前内核型号
- 是否拿到了异常栈帧
- `SCB` 关键寄存器是否齐全
- `LR(EXC_RETURN)`、`PC`、`xPSR`、`MSP/PSP` 是否可用
- 是否有反汇编、map 文件、链接脚本、内存分区信息

### 3.3 输出必须包含“下一步动作”

skill 的最终输出不能停在“疑似野指针”。它必须继续给出：

- 最高概率根因
- 证据链
- 还缺什么信息
- 下一步验证动作
- 若需修改代码，应改哪里、加什么保护

## 4. 技能定位

### 4.1 skill 名称

建议名称：

- `cortex-m-hardfault`

命名理由：

- 足够直接，易于触发
- 覆盖范围明确，不局限于某家芯片厂商
- 后续可扩展到 `MemManage / BusFault / UsageFault`，但不需要在名字里全部展开

### 4.2 skill 触发描述

最终 `SKILL.md` 的 `description` 应覆盖这些触发场景：

- 用户要求分析 `HardFault`
- 用户贴出 `CFSR/HFSR/BFAR/MMFAR/ABFSR`
- 用户要求解释异常栈帧、`EXC_RETURN`、`MSP/PSP`
- 用户希望定位崩溃 `PC` 对应源码位置
- 用户需要编写或改造 `HardFault_Handler`
- 用户需要构建一套 Cortex-M 故障排查流程

## 5. 预期用户输入

skill 应优先支持以下几类输入：

1. 纯文字问题
   - 例如：“为什么我的 M4 会进 HardFault？”
2. 寄存器转储
   - 例如：`HFSR=0x40000000, CFSR=0x01008200, BFAR=0x20030000`
3. 异常栈帧
   - 例如：`R0~R3, R12, LR, PC, xPSR, MSP/PSP`
4. 代码片段
   - 例如：`HardFault_Handler`、疑似故障函数、上下文切换代码
5. 工程文件
   - 例如：启动文件、链接脚本、map 文件、RTOS 上下文切换实现

## 6. 输出目标

skill 的标准输出应尽量稳定为以下结构：

1. 故障类别判断
   - `HardFault` 直发
   - 由 `MemManage / BusFault / UsageFault` 升级
2. 关键证据
   - 哪些寄存器位支持这个判断
3. 故障点定位
   - `PC` 对应函数/源码位置
   - `LR` 和 `EXC_RETURN` 的含义
   - 当前使用的是 `MSP` 还是 `PSP`
4. 高概率根因列表
   - 按概率排序，而不是平铺罗列
5. 下一步验证动作
   - 需要用户补充什么
   - 需要在代码里插什么日志或断言
   - 需要检查哪段汇编/内存布局

## 7. skill 文件结构设计

建议结构如下：

```text
cortex-m-hardfault/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── register-decode.md
│   ├── architecture-matrix.md
│   ├── root-cause-patterns.md
│   └── handler-patterns.md
└── scripts/
    └── decode_fault.py
```

说明：

- `SKILL.md` 只保留工作流、决策顺序、文件导航
- 详细寄存器说明放进 `references/`
- 需要重复执行的寄存器解码逻辑放进 `scripts/`
- 不建议引入 `assets/`，当前场景不是模板资源型 skill

## 8. 各文件职责

### 8.1 `SKILL.md`

只保留高价值、低冗余内容：

- 进入 skill 后的默认工作流
- 如何先确认内核型号和 fault 能力
- 何时读取哪个 reference
- 何时调用脚本解码
- 如何组织最终答复

避免把所有寄存器位说明都塞进 `SKILL.md`，否则触发后上下文会过重。

### 8.2 `references/workflow.md`

定义标准排查流程，建议分为两个版本：

- `快速版`
  - 适合只有寄存器 dump 的场景
- `完整版`
  - 适合带 map、反汇编、源码、RTOS 上下文的场景

核心流程建议：

1. 确认内核型号和是否支持完整 fault 寄存器
2. 读取 `HFSR`
3. 若 `FORCED=1`，拆解 `CFSR`
4. 验证 `MMFAR/BFAR` 有效位
5. 解析 `LR(EXC_RETURN)`，确定使用 `MSP` 或 `PSP`
6. 还原自动入栈帧，取 `PC/LR/xPSR`
7. 将 `PC` 映射到反汇编/源码
8. 结合寄存器位判断根因类别
9. 输出下一步验证动作

### 8.3 `references/register-decode.md`

按下面方式组织，而不是纯抄手册：

- `HFSR`：重点讲 `FORCED`、`VECTTBL`
- `CFSR`
  - `MMFSR`
  - `BFSR`
  - `UFSR`
- `MMFAR/BFAR`
- `ABFSR`（仅 `M7`）
- `CCR` 中与 `DIV_0_TRP`、`UNALIGN_TRP` 相关的辅助判断
- `SHCSR` 中 fault enable/active/pended 状态的辅助意义

每个寄存器位都应配：

- 典型含义
- 常见根因
- 对定位最有帮助的配套证据
- 容易误判的地方

### 8.4 `references/architecture-matrix.md`

这个文件非常关键，用来实现“通用 Cortex-M”而不是“只支持 M3/M4/M7”。

建议至少覆盖：

- `M0/M0+`
  - 只有最小 fault 能力时如何退化分析
- `M3/M4`
  - 标准 `HFSR/CFSR/MMFAR/BFAR`
- `M7`
  - 增加 `ABFSR`
- `带 FPU`
  - `LSPERR/MLSPERR`
- `RTOS 场景`
  - `PSP` 常见于线程栈，`MSP` 常见于异常栈

### 8.5 `references/root-cause-patterns.md`

按“故障模式”归纳比按寄存器更适合实战。

建议覆盖：

- 野指针跳转 / 函数指针损坏
- 栈溢出 / 栈踩坏
- 异常返回损坏
- 非对齐访问
- 除 0
- 执行到不可执行区域
- 非法外设访问 / 总线错误
- 中断向量表错误
- RTOS 任务栈损坏
- FPU lazy stacking 相关问题

每种模式都应回答：

- 常见寄存器组合
- 常见现场特征
- 如何进一步验证
- 修复优先级

### 8.6 `references/handler-patterns.md`

提供与工具链无关的 handler 设计建议，而不是只给单一厂商范例：

- 如何抓取自动入栈帧
- 如何区分 `MSP/PSP`
- 如何保存 `SCB` 关键寄存器
- 调试版本如何 `BKPT`
- 量产版本如何写入保留 RAM / Flash 日志
- 如何避免 handler 里再触发 fault

### 8.7 `scripts/decode_fault.py`

建议实现一个命令行脚本，输入若干寄存器值，输出初步解码结果。

建议支持参数：

```text
--core m0|m3|m4|m7|m33
--hfsr 0x...
--cfsr 0x...
--mmfar 0x...
--bfar 0x...
--abfsr 0x...
--lr 0x...
--pc 0x...
--xpsr 0x...
--msp 0x...
--psp 0x...
```

脚本输出建议包括：

- 检测到的 fault 位
- 自动推断的 fault 分类
- 栈选择推断（`MSP/PSP`）
- 需要人工继续确认的风险点

这个脚本不是为了替代分析，而是为了避免每次手工解码 bit 位。

## 9. 核心工作流设计

skill 的默认工作流建议固定为下面的顺序。

### 阶段 1：识别上下文

先确认：

- 芯片和内核型号
- 是否 RTOS
- 是否带 FPU
- 当前拿到的是现场 dump、源码、还是口头描述

### 阶段 2：最小证据集检查

优先要求以下信息：

- `HFSR`
- `CFSR`
- `MMFAR`
- `BFAR`
- `ABFSR`（若 `M7`）
- `LR / PC / xPSR`
- `MSP / PSP`

如果用户缺信息，skill 应直接给出“最小采集模板”，而不是继续猜。

### 阶段 3：分类分析

顺序固定：

1. 先判断是否 `FORCED HardFault`
2. 再判断是 `MemManage / BusFault / UsageFault` 哪一路
3. 再看是否是 `stacking/unstacking` 类问题
4. 最后才结合代码上下文判断是野指针、栈溢出、非法返回、除 0 等具体根因

### 阶段 4：故障点回溯

必须使用：

- `EXC_RETURN`
- 自动入栈帧中的 `PC`
- 必要时配合 `LR`
- map 文件或反汇编

这里要明确告诉使用 skill 的 Codex：

- `PC` 最有价值，但不是任何情况下都绝对可信
- 当出现 `IMPRECISERR`、`STKERR`、`UNSTKERR` 等位时，`PC` 可能只是“观测点”，不是“根因点”

### 阶段 5：输出结论

结论模板建议统一为：

- 结论
- 证据
- 不确定性
- 下一步验证
- 可能修复方向

## 10. 关键差异点设计

### 10.1 为什么不能只照着博客做成 “M3/M4/M7 专用”

用户要求是 “Cortex-M 系列通用”，而博客重点是 `M3/M4/M7`。因此 skill 必须在设计上补上这层抽象：

- 如果是 `M0/M0+`，不能要求用户提供不存在的 `CFSR/BFAR/MMFAR`
- 如果是 `M7`，需要额外检查 `ABFSR`
- 如果是带 FPU 的 `M4/M7`，需要考虑 lazy stacking 位
- 如果是 RTOS，`PSP` 通常比 `MSP` 更重要

### 10.2 为什么需要“根因模式库”

多数 HardFault 分析最后都要落回少数几类工程问题。单纯按寄存器解释还不够，必须让 skill 能把“寄存器模式”映射到“工程根因模式”。

例如：

- `INVSTATE + LSB=0` 更像函数指针跳转错误
- `STKERR/MSTKERR` 更像栈边界或栈指针损坏
- `DIVBYZERO` 需要检查 `CCR.DIV_0_TRP`
- `UNALIGNED` 需要确认 `CCR.UNALIGN_TRP`
- `PRECISERR + BFARVALID` 可优先追 `BFAR`
- `IMPRECISERR` 需要扩大搜索范围，不能只盯当前 `PC`

## 11. 建议的实现阶段

### Phase 1

先完成最小可用 skill：

- `SKILL.md`
- `references/workflow.md`
- `references/register-decode.md`
- `references/architecture-matrix.md`

这个阶段先让 skill 能稳定分析大多数 `M3/M4/M7` dump，并且不会误导 `M0/M0+` 用户。

### Phase 2

补齐实战价值最高的内容：

- `references/root-cause-patterns.md`
- `references/handler-patterns.md`
- `scripts/decode_fault.py`

### Phase 3

补充增强项：

- 更细的 RTOS 场景
- 对常见工具链的最小抓取模板
- Forward test 示例

## 12. 验收标准

该 skill 至少应满足以下验收条件：

1. 用户只给 `HFSR/CFSR/BFAR/MMFAR/LR/PC/xPSR` 时，skill 能给出结构化初判
2. 用户给的是 `M0/M0+` 场景时，skill 不会错误索要不存在的寄存器
3. 用户给的是 `M7` 场景时，skill 会主动检查 `ABFSR`
4. 用户给出 `EXC_RETURN` 时，skill 会主动判断 `MSP/PSP`
5. skill 输出中始终包含“下一步验证动作”
6. skill 不会把“可能性列表”当成结论，而会按证据强弱排序

## 13. 建议的下一步

在你确认这份设计后，下一步直接进入实现：

1. 初始化 skill 目录 `cortex-m-hardfault`
2. 编写 `SKILL.md`
3. 拆出 `references/` 中的 5 个文件
4. 视时间决定是否同步实现 `scripts/decode_fault.py`

## 14. 设计结论

这个 skill 的正确做法不是“把博客改写成一篇说明文”，而是：

- 把博客中的 fault 理论抽成决策树
- 把架构差异补齐
- 把寄存器知识拆成按需引用的 references
- 把重复 bit 解码下沉到脚本
- 让最终 skill 具备真实排障能力

如果按这个方案实现，最终产物会是一个真正可复用的 `Cortex-M HardFault` 排查 skill，而不是一份静态笔记。
