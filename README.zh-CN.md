# Cortex-M HardFault 诊断 Skill

**中文** | **[English](./README.md)**

一个专门用于诊断 Cortex-M 系列崩溃的 skill，包括 HardFault、MemManage、BusFault 和 UsageFault。该工具帮助嵌入式开发者分析寄存器转储、异常栈帧、反汇编和 map 文件，以精确定位故障点和根本原因。

## 特性

- **全面的故障分析**：支持 HardFault、MemManage、BusFault 和 UsageFault 异常的诊断
- **多内核支持**：处理 Cortex-M0/M0+、M3、M4、M7、M33 以及带 FPU 的变体
- **基于证据的方法**：结构化工作流程，优先考虑证据而非推测
- **架构感知**：尊重不同 Cortex-M 变体的能力差异
- **工具链无关**：适用于 Keil、IAR、GCC、STM32CubeIDE、J-Link、OpenOCD 等
- **RTOS 支持**：处理裸机和 RTOS 上下文，包括 MSP/PSP 分析
- **自动解码**：包含 Python 脚本，用于快速寄存器位解码

## 快速开始

### 1. 分析崩溃

提供崩溃证据：

```
HFSR=0x40000000, CFSR=0x01008200, BFAR=0x20030000
LR=0xFFFFFFF9, PC=0x08001234, xPSR=0x21000000
MSP=0x20020000, PSP=0x2001F000
```

### 2. 使用解码脚本

```bash
python ./scripts/decode_fault.py \
  --core m7 \
  --hfsr 0x40000000 \
  --cfsr 0x00008200 \
  --bfar 0x20030000 \
  --lr 0xFFFFFFF9 \
  --pc 0x08001234 \
  --xpsr 0x21000000
```

### 3. 实现 HardFault Handler

参见 `references/handler-patterns.md` 获取可投入生产的 handler 实现，该实现能够捕获崩溃数据而不会导致二次故障。

## 项目结构

```
cortex-m-hardfault/
├── SKILL.md                          # 主要 skill 定义
├── agents/
│   └── openai.yaml                   # Agent 配置
├── references/
│   ├── workflow.md                   # 标准诊断流程
│   ├── register-decode.md            # HFSR/CFSR/MMFAR/BFAR 解码
│   ├── architecture-matrix.md        # 内核能力差异
│   ├── root-cause-patterns.md        # 常见故障模式
│   └── handler-patterns.md           # Handler 实现指南
└── scripts/
    └── decode_fault.py               # 自动化寄存器解码器
```

## 核心工作流程

1. **识别内核**：确定 Cortex-M 变体和能力
2. **收集证据**：收集故障状态寄存器和栈帧
3. **解码寄存器**：解析 HFSR、CFSR、MMFAR、BFAR、ABFSR
4. **恢复上下文**：解释 EXC_RETURN 以选择 MSP 或 PSP
5. **定位故障**：将栈中的 PC 映射到源代码或反汇编
6. **根因分析**：按证据排序可能的根本原因
7. **提出下一步**：提供具体的验证操作

## 最小必需证据

- 内核/MCU 型号（如 M0+、M4F、M7）
- HFSR、CFSR、MMFAR、BFAR（如果可用）
- 栈中的 R0-R3、R12、LR、PC、xPSR
- MSP 和 PSP 值
- 故障 PC 附近的反汇编或源代码行
- RTOS 和 FPU 状态

## 支持的内核

| 内核 | 故障支持 | 特殊注意事项 |
|------|---------|-------------|
| M0/M0+ | 仅基础 | 寄存器有限，依赖栈中 PC |
| M3 | 完整 | 标准 HFSR/CFSR/MMFAR/BFAR |
| M4/M4F | 完整 | 增加 FPU lazy stacking 检查 |
| M7 | 完整 + ABFSR | 检查辅助总线故障寄存器 |
| M33 | 完整 | 安全感知分析 |

## 常见故障模式

- 野指针 / 函数指针损坏
- 栈溢出 / 栈损坏
- 异常返回损坏
- 非对齐访问
- 除零
- 在不可执行内存中执行
- 非法外设访问 / 总线错误
- 中断向量表错误
- RTOS 任务栈损坏
- FPU lazy stacking 问题

## 文档

- **[SKILL.md](cortex-m-hardfault/SKILL.md)** - 主要 skill 定义和使用
- **[设计文档](hardfault-skill-design.md)** - 详细的设计原理
- **[参考资料](cortex-m-hardfault/references/)** - 全面的技术文档

## 要求

- Python 3.6+（用于解码脚本）
- 目标平台：Cortex-M 系列微控制器
- 调试接口：J-Link、ST-Link、OpenOCD 或等效工具

## 许可证

MIT License

## 贡献

欢迎贡献！请确保：

- 所有分析采用基于证据的方法
- 尊重内核能力差异
- 清晰记录假设条件
- 在多个 Cortex-M 变体上进行测试

## 致谢

基于 [Cortex-M3/M4/M7 芯片 Fault 分析原理与实战](https://yuxxxxxxxxxx.github.io/2024/10/07/Cortex-M3-M4-M7-%E8%8A%AF%E7%89%87-Fault-%E5%88%86%E6%9E%90%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E6%88%98/) 和 Arm CMSIS 文档。