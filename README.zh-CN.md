<p align="center">
  <a href="./README.md">English</a> |
  <strong>简体中文</strong> |
  <a href="./README.ja.md">日本語</a> |
  <a href="./README.ko.md">한국어</a>
</p>

# C-SafeQA

<div align="center">

<img src="./assets/C-SafeQA-hero-zh-CN.jpg" alt="C-SafeQA——谁来评判评判者？" width="100%" />

<p><strong>谁来评判评判者？</strong><br />
一个基于政策、面向中文回复级安全评估的基准。</p>

<p>
  <a href="ARXIV_URL"><img src="https://img.shields.io/badge/Paper-PDF-B31B1B?style=flat-square&amp;logo=arxiv&amp;logoColor=white" alt="论文" /></a>
  <a href="https://github.com/SparkShieldLab/C-SafeQA"><img src="https://img.shields.io/badge/Code-GitHub-181717?style=flat-square&amp;logo=github&amp;logoColor=white" alt="代码" /></a>
  <a href="https://huggingface.co/datasets/SparkShieldLab/C-SafeQA"><img src="https://img.shields.io/badge/Dataset-Hugging_Face-FFD21E?style=flat-square&amp;logo=huggingface&amp;logoColor=black" alt="数据集" /></a>
  <a href="https://sai.xingdun-ai.com/home"><img src="https://img.shields.io/badge/Website-C--SafeQA-1677FF?style=flat-square&amp;logo=googlechrome&amp;logoColor=white" alt="网站" /></a>
  <a href="https://open.weixin.qq.com/qr/code?username=gh_89d544e1b8aa"><img src="https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1-WeChat-07C160?style=flat-square&amp;logo=wechat&amp;logoColor=white" alt="微信公众号" /></a>
</p>

<p>
  <strong>538</strong> 条基础问题 &nbsp;·&nbsp;
  <strong>8,877</strong> 条对抗问题 &nbsp;·&nbsp;
  <strong>37,660</strong> 个问题—回复对 &nbsp;·&nbsp;
  <strong>7</strong> 个安全判别器
</p>

</div>

## 概述

C-SafeQA 使用四个目标语言模型的回复评估七个自动化安全判别器。当前版本包含 37,660 条经过评估的问题—回复记录：

| 分区 | 记录数 | 说明 |
|---|---:|---|
| 基础集 | 2,152 | 538 条基础问题分别与四个目标模型的回复配对 |
| 变换集 | 35,508 | 通过 21 种受控问题变换得到的回复 |
| 总计 | 37,660 | 基础集与变换集记录 |

538 条基础提示覆盖 269 个风险点，每个风险点均以两种寻求危害的形式表达：一种是明确要求有害输出，另一种是旨在诱导模型产生有害内容的陈述式或诱导式提示。九种变换仅应用于其中一种形式，另有十二种变换同时应用于两种形式，因此每个目标模型产生 `9 × 269 + 12 × 538 = 8,877` 条对抗提示，四个模型合计产生 35,508 条变换记录。

所有基础提示和变换提示都被有意设计为诱导有害内容，但参考标签**仅根据模型回复**标注。因此，拒绝回答或安全引导的回复即使面对有害提示，也可以标记为 `Safe`；生成或实质性促进有害行为的回复标记为 `Unsafe`；存在歧义的情况标记为 `Disputed`。

参与评估的安全判别器包括 Llama Guard 4、MD-Judge、NeMoGuard、PolyGuard、Qwen3Guard、WildGuard 和 XGuard。目标模型包括 DeepSeek-V3.2、Kimi-K2.5、MiniMax-M2.5 和 Qwen3.5-397B-A17B。

## 动态

- **2026-08-11** 🏆 我们的联合团队在 **ArA-DF 2026 声学鲁棒性赛道**中获得第一名，在鲁棒阿拉伯语语音深度伪造检测任务上取得 **0.6575%** 的等错误率（EER）。[阅读详情](https://mp.weixin.qq.com/s/zAXZINkpC4_ROFxdT8CYyg)。
- **2026-07-22** 🚀 我们发布了三款 AI 安全产品：面向大模型内容安全治理的**星界**、面向智能体应用安全的**星驭**，以及面向 AIGC 可信内容治理的**星鉴**。三者共同覆盖端到端内容治理、智能体安全与可信 AIGC 溯源。[阅读详情](https://yf2ljykclb.xfchat.iflytek.com/wiki/S1LqweZxMifmpIkluKvrh2ibzMc)。
- **2026-06-23** 🛡️ 我们推出了 **SparkShield SkillScanner**，这是一项安全评估服务，旨在识别 Agent Skills 部署前的供应链与运行时风险。[阅读详情](https://mp.weixin.qq.com/s/fv5OvFgrpiJX_i7lU3orsQ)。

## 仓库内容

本 GitHub 仓库发布用于获取七个被评估安全防护模型原始输出的推理运行脚本。基准数据在 [Hugging Face](https://huggingface.co/datasets/SparkShieldLab/C-SafeQA) 上单独发布。

```text
code/
├── llama_guard_judge.py
├── mdjudge_judge_merged.py
├── nemoguard_judge_merged.py
├── polyguard_judge_merged.py
├── qwen3guard_judge_merged.py
├── wildguard_judge_merged.py
└── xguard_judge_merged.py
```

## 安装

```bash
git clone https://github.com/SparkShieldLab/C-SafeQA.git
cd C-SafeQA
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install transformers vllm
```

## 加载数据

```python
from datasets import load_dataset

dataset = load_dataset("SparkShieldLab/C-SafeQA", revision="v1.0.0")
print(dataset)
print(dataset["base"].features)
```

该版本提供一个 `base` 划分，并为每个目标模型提供一个变换数据划分。字段定义、内容风险、数据来源和允许用途请参阅[数据集卡片](https://huggingface.co/datasets/SparkShieldLab/C-SafeQA)。

## 复现安全判别器输出

每个运行脚本接收一个 UTF-8 编码的 JSON 文件，其顶层结构必须为数组。每条记录都必须包含字符串类型的 `prompt` 和 `response` 字段：

```json
[
  {
    "prompt": "请介绍如何设置强密码。",
    "response": "建议使用足够长且不重复的随机密码，并启用多因素认证。"
  }
]
```

七个运行脚本均使用 `temperature=0` 的确定性解码。各脚本对应的默认检查点 ID、提示词或聊天格式、最大输出长度和 vLLM 设置均直接定义在相应 Python 文件中。

这些代码可复现发布版本所采用的推理流程。由于下载的检查点版本、分词器、vLLM/Transformers 版本和硬件环境不同，输出仍可能无法做到逐字节完全一致，因此用户在执行审计时应记录这些信息。

## 评估说明

- 参考标签空间为 `Safe`、`Unsafe` 和 `Disputed`。
- 二分类指标不包含参考标签为 `Disputed` 的记录。
- 安全判别器输出若标记为 `non_normalizable`，则不纳入二分类指标，并作为覆盖范围限制单独报告。
- 归一化状态表示输出能否被映射，本身并不是安全结论。

## 负责任使用

C-SafeQA 用于评估和研究安全分类器，不应被视为生成有害内容的训练集、法律或政策审查的替代方案，也不能作为模型可安全部署的证明。本基准聚焦中文，体现其文档所述的分类体系与标注流程，并可能包含标注错误、模型特定伪影、文化假设以及合成或对抗模式。

## 许可证

本仓库代码采用 [Apache License 2.0](./LICENSE) 许可。数据集采用单独的 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可，并受其数据集卡片所列条款约束。第三方模型检查点及其输出可能适用其他条款，用户有责任确保合规使用。

## 引用

```bibtex
@misc{csafeqa2026,
  title        = {WHO JUDGES THE JUDGES? A CHINESE SAFETY QA BENCHMARK FOR EVALUATING LLM RESPONSES AND SAFETY JUDGES},
  author       = {Ziqi Zhao and Qingzhong Yan and Yuhang Sun and Rui Yang and Shuang Huang and Junhua Liu and Cong Liu and Guoping Hu and Jing Shao},
  year         = {2026},
  eprint       = {[ARXIV_ID]},
  archivePrefix= {arXiv},
  primaryClass = {[ARXIV_PRIMARY_CLASS]},
  url          = {https://arxiv.org/abs/[ARXIV_ID]}
}
```

## 致谢

衷心感谢长三角安全人工智能安徽省实验室的支持。

## 关于长三角安全人工智能安徽省实验室

长三角安全人工智能安徽省实验室致力于推动可信与安全人工智能的发展。我们的工作涵盖政策敏感场景、模型内容安全、智能体安全和严格的安全评估，并尤其关注复杂现实需求下的安全问题。我们欢迎这些方向的科研合作与产业合作，欢迎通过以下渠道与我们联系。

<p>
  <a href="https://sai.xingdun-ai.com/home"><img src="https://img.shields.io/badge/Website-Official_Site-1677FF?style=flat-square&amp;logo=googlechrome&amp;logoColor=white" alt="官方网站" /></a>
  <a href="https://open.weixin.qq.com/qr/code?username=gh_89d544e1b8aa"><img src="https://img.shields.io/badge/WeChat-Follow_Us-07C160?style=flat-square&amp;logo=wechat&amp;logoColor=white" alt="微信公众号" /></a>
</p>

<p align="center">
  <strong>扫描下方二维码加入微信群。</strong>
</p>

<p align="center">
  <img src="./assets/wechat-group-qr.jpg" alt="C-SafeQA 微信群二维码" width="220" />
</p>
