### SuperNav

**完整标题：** SuperNav: An Agentic Navigation System for Any Task in Any Scene

**作者：** Jinkai Zhang等

**发表期刊/年份：** — / 2026

**arXiv：** [2610.12126v1](https://arxiv.org/abs/2610.12126v1)

**架构：** 预训练MLLM通过harness选择导航目标，无需导航专用微调。Navigation Skills提供搜索、恢复及完成判断的指导。工具返回四方向RGB图像、执行状态及诊断信息。统一图像坐标接口将MLLM连接至Geo-based Executor或Learned Executor。

**核心方法论：** MLLM在图像中选择目的地，执行器移动并返回反馈，支持下一次决策。目标记录管理未完成及已完成项目。上下文管理移除已被新观测替代的图像数据，但保留文本历史和图像路径。Geo-based Executor使用几何信息与路径规划。Learned Executor根据RGB观测及图像标记点预测局部移动。

**机器人/任务：** Habitat-GS中的实例及有序多对象导航、AI2-THOR中的需求驱动导航，以及HM3D上的类别级导航。真实机器人案例使用Unitree Go2搜索物体并依次访问目标。

**主要贡献：**

- 将图像目的地选择连接至可替换的运动执行器。
- 结合Navigation Skills、目标记录与上下文管理来处理不同请求。
- 评估多种导航任务，并通过消融实验分析harness的作用。

**定量结果：**

| 基准/任务 | 指标 | 数值 | 条件 |
|---|---|---|---|
| 基于InteriorGS的Habitat-GS，单对象导航 | SR | 78.00% | Geo-based Executor；150个任务；到批准目标视点的navmesh路径距离小于1 m，并明确STOP |
| 基于InteriorGS的Habitat-GS，有序多对象导航 | SR | 34.00% | Geo-based Executor；150个任务，每个含2–5个目标；按序到达并明确STOP |
| AI2-THOR中调整评估后的Demand-Bench | SR | 59.50% | Geo-based Executor；200个任务；不重复使用物体，按序进入2 m目标区域并明确STOP |
| HM3D-OVON val-unseen，Navigation Skills消融 | SR | 使用Skills：68.33%；移除Skills：35.00% | 相同120个回合、Geo-based Executor、GPT-5.6 Terra (high)及0.25 m阈值 |

**AI研究评分：** 三位评估者的平均分，满分10分。

| 维度 | 分数 | 理由 |
|---|---|---|
| 重要性 | 8.0 | 在陌生场景中处理不同请求对服务机器人很重要。推理成本、延迟波动及几何信息依赖限制实际应用。 |
| 增量贡献 | 6.0 | 可替换执行器、Skills和上下文管理扩展了已有harness方法。缺少与最接近的harness方法的直接比较。 |
| 方法质量 | 8.0 | 图像坐标目标和执行反馈将决策与运动分离。相同执行器下的消融支持该设计，但语义完成判断缺少独立验证。 |
| 有效性 | 7.0 | 结果支持多种导航任务。观测及执行条件不同限制了基线比较；真实机器人证据为定性案例。 |
| 空白弥补证据 | 7.0 | 结果支持超出固定流程与导航训练数据范围的任务及场景泛化。实际活动完成及较长真实环境序列仍未验证。 |

**综合评分：** 7.1/10。

**局限性/差距：**

- 语义判断和目标记录依赖MLLM，不构成独立语义验证。
- Geo-based Executor需要地图或场景几何信息。MLLM推理带来成本和延迟波动。
- 需求驱动评估衡量按序到达目标的能力，不评估所请求活动本身的完成情况。
- 基线保留各自输入及历史管理机制。观测和运动执行条件与SuperNav不同。
- 真实机器人证据为定性案例。长导航序列的可靠性及更广泛的真实环境评估仍待研究。

**开放权重/代码：** — / —。

## 推理/部署

- **推理延迟：** 存在波动；具体数值：—。
- **部署硬件：** Unitree Go2，使用四方向RGB相机、LiDAR及里程计；计算硬件：—。

## 数据集/数据收集

- **评估数据：** 基于InteriorGS的Habitat-GS包含150个单对象任务和150个有序多对象任务。AI2-THOR中调整评估后的Demand-Bench包含200个任务。类别级评估使用120个HM3D-OVON val-unseen回合及1,000个HM3Dv2验证回合。

**来源：** [论文正文](https://arxiv.org/html/2610.12126v1)第3–5节及附录A.1；[项目](https://zju3dv.github.io/SuperNav/)。
