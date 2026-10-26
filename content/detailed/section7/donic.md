### 7.4 DONIC

**Full title:** DONIC: Generalist Dexterous Bimanual Tracking Control from Human Demonstrations

**Authors:** Mingze Sun, Ziang Cao, Yuan Fei, Qiankuan Tao, Zihan Wang, Tianqi Liu, Junhao Chen, Haiwen Diao, Fangzhou Hong, Zhaoxi Chen, Ziwei Liu (Ropedia)

**Venue/Year:** arXiv 2026

**arXiv:** https://arxiv.org/abs/2610.29997v1

**Project page:** https://ropedia.github.io/DONIC

**RL algorithm:** Proximal policy optimization (PPO) with behavioral cloning (BC). Verified successful executions become training demonstrations. Clip-Centered Advantages (CCA) subtract the mean advantage for each reference clip before PPO updates.

**Hand hardware:** Two Wuji Hand V1 robot models in simulation; DoF not reported.

**Sim platform:** Isaac Gym

**Sim2Real?** No. Quantitative evaluation uses simulation. Transfer to physical bimanual systems is future work.

**Tasks:** Bimanual reference tracking across operation categories and human-motion sources. One policy controls both hands to reproduce reference object motion.

**Key methodology:** Human hand–object motions are reconstructed, retargeted, and screened by replay. One policy predicts corrections to the next reference for both hands. An object-centered reward tracks object motion and supervises each hand according to its reference contact role. PPO and BC training reuses verified successes. CCA removes clip-specific advantage offsets while preserving differences within each clip.

**Main contributions:**

- One bimanual tracker learns across operation categories and human-motion sources. It tracks unseen trajectories and objects without fine-tuning.
- BiHOI adds 1,575 multi-view interaction sequences covering 229 objects.
- Per-hand contact rewards and CCA support shared training across different contact roles and clip difficulty.

**Results:** On 53 unseen trajectories of training objects, DONIC achieves 86.79% success and 67.62% completion. On 164 clips with held-out objects, it achieves 57.32% success and 54.69% completion. With BiHOI added to training, success reaches 88.68% and 59.76%, respectively. All results use simulation and no fine-tuning. Success uses trajectory-averaged error thresholds for both hands; completion measures the fraction of frames that meet all thresholds for both hands.

**Limitations/Gaps:** Quantitative evaluation covers simulated single-object interactions with reconstructed, retargeted references. Longer tasks, multiple objects, an independent benchmark, and physical transfer remain future work. Net contact force cannot identify the collision partner. Success based on average errors does not establish stable tracking at every frame.

**Code:** —

**Weights:** —

## AI Research Assessments

Mean AI research assessments from three reviewers, on a 10-point scale. Overall: **7.3/10**.

- **Importance: 8.0/10.** Shared learning of support and manipulation roles addresses useful coordination for household, assembly, and assistive robots. Physical transfer remains untested.
- **Contribution beyond prior work: 7.0/10.** Per-hand contact rewards, CCA, and BiHOI extend DexTrack's PPO + BC approach to one bimanual policy. The training framework builds on prior work.
- **Method quality: 7.7/10.** Separate object-motion and per-hand contact feedback fits asynchronous coordination. Net contact force cannot identify the collision partner, and the proposed explanation for CCA's effect has indirect support.
- **Effectiveness: 7.3/10.** Shared-data comparisons and ablations support better tracking. Held-out-object success remains partial, and trajectory-average success does not establish continuous stability.
- **Evidence for closing the research gap: 7.0/10.** One policy tracks unseen references without fine-tuning, and added BiHOI data helps. Evidence remains limited to selected single-object simulations.

## Dataset / Data Collection

- **Dataset used:** GRAB, GigaHands, OakInk2, TACO, and H2O provide public references. The additional-data variant also uses BiHOI.
- **Collection method:** BiHOI records human hand–object interactions with 32 calibrated RGB cameras. Reconstructed hand and object motion becomes robot references through retargeting. Public references are also retargeted and screened by replay.
- **Data scale:** 1,845 public-data training clips; 3,420 with BiHOI. BiHOI contains 1,575 sequences, 229 objects, and 14.77 hours of interaction.
- **Teleop equipment:** —
- **Data format:** Reconstructed hand parameters, object meshes and poses, and retargeted wrist and finger references.
- **Publicly available?** —

## Inference / Deployment

- **Inference latency:** —
- **Deployment hardware:** Evaluated with two Wuji Hand V1 models in Isaac Gym. Physical deployment remains future work.
- **Real-time capable?** —
