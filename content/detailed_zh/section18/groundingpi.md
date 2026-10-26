### GroundingPI

**完整标题：** GroundingPI: A Grounding Foundation Model towards Physical Intelligence with Visual Primitives

**作者：** Qize Yu等

**发表期刊/年份：** — / 2026

**arXiv：** [2609.39601v1](https://arxiv.org/abs/2609.39601v1)

**架构：** 4B grounding基础模型，结合MoonViT-V2视觉编码器和Qwen3-4B语言解码器。点和边界框使用共享词表中的量化坐标token。

**核心方法论：** 通过多模态与空间预训练、监督微调（SFT）和GRPO学习精确感知。操作任务将中间特征注入Action DiT各层的交叉注意力。每个基准内的骨干比较固定动作专家、动作数据、训练预算、动作表示和推理流程。

**机器人/任务：** RoboTwin 2.0评估固定基座双臂桌面操作。RoboCasa-GR1评估人形灵巧手操作。nuScenes评估开环驾驶轨迹预测。

**主要贡献：**
- 将生成式坐标grounding扩展到广泛的感知预训练及动作学习迁移。
- 在场景和实体变化的全部4个OOD操作设置中排名第一。
- 在RoboCasa-GR1上，用50%的演示训练即可超过用75%演示训练的比较骨干。

**定量结果：**

| 基准/任务 | 指标 | 数值 | 条件 |
|---|---|---|---|
| RoboTwin2.0 Full | 任务成功率 | 66.20% | 相同下游架构与训练协议 |
| RoboTwin2.0-Clean2Random | 任务成功率 | 17.60% | Rex-Omni：14.10%；在Clean上训练，在Randomized场景评估 |
| RoboCasa-GR1 Full | 任务成功率 | 37.75% | RynnBrain：39.00%；分布内评估 |
| nuScenes | 平均开环L2误差 | 0.296 m | 轨迹预测；未证明闭环性能 |

**AI研究评分：** 三位评估者的平均分，满分10分。

| 维度 | 分数 | 理由 |
|---|---|---|
| 重要性 | 8.0 | 精确感知可减轻稀缺动作数据的负担。超出已报告评估的实际效果仍不确定。 |
| 增量贡献 | 7.0 | 广泛感知预训练和动作迁移扩展了已有grounding模型。量化坐标生成采用已有方法。 |
| 方法质量 | 8.0 | GRPO处理定位、遗漏和重复，比较时固定Action DiT。骨干架构和预训练差异仍存在。 |
| 有效性 | 7.0 | 全部4个OOD操作设置领先。Clean2Random成功率仍低，驾驶改进较小。 |
| 空白弥补证据 | 7.3 | Grounding与受控动作迁移支持感知瓶颈的论点。开环驾驶未证明闭环性能。 |

**综合评分：** 7.4/10。

**局限性/差距：**
- RoboCasa-GR1 Full成功率低于RynnBrain，Clean2Random成功率仍低。
- nuScenes结果未证明闭环性能、延迟或标志识读的独立作用。
- 骨干架构和预训练不同，无法完全分离grounding训练本身的贡献。
- VisDrone仍有挑战；部分空间和GUI基准中GPT-6 Astra更强。

**开放权重/代码：** — / —（论文未报告）。

## 推理/部署

- **推理延迟：** —
- **部署硬件：** —

## 数据集/数据收集

- **训练数据：** 公开数据集及使用多教师和任务专用验证的数据引擎。
- **评估数据：** RoboTwin 2.0、RoboCasa-GR1、nuScenes，以及涵盖11种感知能力的34个grounding基准。

**来源：** [论文正文](https://arxiv.org/html/2609.39601v1)第3–5.2.2节。
