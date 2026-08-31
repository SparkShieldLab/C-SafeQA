<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">简体中文</a> |
  <strong>日本語</strong> |
  <a href="./README.ko.md">한국어</a>
</p>

# C-SafeQA

<div align="center">

<img src="./assets/C-SafeQA-hero-ja.jpg" alt="C-SafeQA — 審判者を裁くのは誰か？" width="100%" />

<p><strong>審判者を裁くのは誰か？</strong><br />
ポリシーに基づく、中国語応答レベルの安全性評価ベンチマーク。</p>

<p>
  <a href="ARXIV_URL"><img src="https://img.shields.io/badge/Paper-PDF-B31B1B?style=flat-square&amp;logo=arxiv&amp;logoColor=white" alt="論文" /></a>
  <a href="https://github.com/YOUR_ORG/C-SafeQA"><img src="https://img.shields.io/badge/Code-GitHub-181717?style=flat-square&amp;logo=github&amp;logoColor=white" alt="コード" /></a>
  <a href="https://huggingface.co/datasets/SparkShieldLab/C-SafeQA"><img src="https://img.shields.io/badge/Dataset-Hugging_Face-FFD21E?style=flat-square&amp;logo=huggingface&amp;logoColor=black" alt="データセット" /></a>
  <a href="https://sai.xingdun-ai.com/home"><img src="https://img.shields.io/badge/Website-C--SafeQA-1677FF?style=flat-square&amp;logo=googlechrome&amp;logoColor=white" alt="ウェブサイト" /></a>
  <a href="https://open.weixin.qq.com/qr/code?username=gh_89d544e1b8aa"><img src="https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1-WeChat-07C160?style=flat-square&amp;logo=wechat&amp;logoColor=white" alt="WeChat公式アカウント" /></a>
</p>

<p>
  <strong>538</strong> 件のベースクエリ &nbsp;·&nbsp;
  <strong>8,877</strong> 件の敵対的クエリ &nbsp;·&nbsp;
  <strong>37,660</strong> 組のクエリ–応答ペア &nbsp;·&nbsp;
  <strong>7</strong> 種の安全性判定器
</p>

</div>

## 概要

C-SafeQA は、4つの評価対象言語モデルの応答を用いて、7つの自動安全性判定器を評価します。現在のリリースには、評価済みのクエリ–応答レコードが 37,660 件含まれています。

| パーティション | レコード数 | 説明 |
|---|---:|---|
| ベース | 2,152 | 538 件のベースクエリと4つの評価対象モデルの応答を組み合わせたもの |
| 変換 | 35,508 | 21種類の制御されたクエリ変換に対する応答 |
| 合計 | 37,660 | ベースレコードと変換レコード |

538 件のベースプロンプトは 269 のリスクポイントを対象とし、各ポイントは有害な出力を求める2つの形式で表現されています。1つは有害な出力を明示的に要求する形式、もう1つは有害な出力を誘発するよう設計された宣言的または誘導的な形式です。9種類の変換は一方の形式だけに適用され、12種類の変換は両方に適用されるため、評価対象モデルごとに `9 × 269 + 12 × 538 = 8,877` 件の敵対的プロンプト、4モデル全体で 35,508 件の変換レコードが生成されます。

すべてのベースプロンプトと変換プロンプトは有害な内容を引き出すことを意図して設計されていますが、参照ラベルは**モデルの応答のみ**に基づいて付与されます。そのため、有害なプロンプトに対する拒否や安全な方向への誘導は `Safe` と判定される場合があります。有害な行為を生成または実質的に助長する応答は `Unsafe`、判断が曖昧なケースは `Disputed` とラベル付けされます。

評価対象の判定器は Llama Guard 4、MD-Judge、NeMoGuard、PolyGuard、Qwen3Guard、WildGuard、XGuard です。評価対象モデルは DeepSeek-V3.2、Kimi-K2.5、MiniMax-M2.5、Qwen3.5-397B-A17B です。

## ニュース

- **2026-08-11** 🏆 私たちの合同チームは **ArA-DF 2026 の Acoustic Robustness Track** で第1位を獲得し、堅牢なアラビア語音声ディープフェイク検出において **0.6575%** の等誤り率（EER）を達成しました。[詳細](https://mp.weixin.qq.com/s/zAXZINkpC4_ROFxdT8CYyg)。
- **2026-07-22** 🚀 3つの AI セキュリティ製品を発表しました。LLM コンテンツ安全性ガバナンスの**星界**、エージェントアプリケーションのセキュリティを担う**星驭**、信頼できる AIGC コンテンツガバナンスの**星鉴**です。これらは、エンドツーエンドのコンテンツガバナンス、エージェントセキュリティ、信頼できる AIGC の来歴管理を包括的に支援します。[詳細](https://yf2ljykclb.xfchat.iflytek.com/wiki/S1LqweZxMifmpIkluKvrh2ibzMc)。
- **2026-06-23** 🛡️ Agent Skills のデプロイ前にサプライチェーンおよびランタイムのリスクを特定するセキュリティ評価サービス、**SparkShield SkillScanner** を発表しました。[詳細](https://mp.weixin.qq.com/s/fv5OvFgrpiJX_i7lU3orsQ)。

## リポジトリの内容

この GitHub リポジトリでは、評価対象となる7つの安全性ガードモデルから生の出力を取得するために使用した推論ランナーを公開しています。ベンチマークデータは [Hugging Face](https://huggingface.co/datasets/SparkShieldLab/C-SafeQA) で別途公開しています。

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

## インストール

```bash
git clone https://github.com/[ORG]/C-SafeQA.git
cd C-SafeQA
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install transformers vllm
```

## データの読み込み

```python
from datasets import load_dataset

dataset = load_dataset("SparkShieldLab/C-SafeQA", revision="v1.0.0")
print(dataset)
print(dataset["base"].features)
```

本リリースは `base` スプリットと、評価対象モデルごとに1つの変換スプリットを提供します。フィールド定義、コンテンツリスク、来歴、許可される用途については、[データセットカード](https://huggingface.co/datasets/SparkShieldLab/C-SafeQA)を参照してください。

## 安全性判定器の出力を再現する

各ランナーは、トップレベルが配列である UTF-8 JSON ファイルを受け取ります。各レコードには、文字列型の `prompt` フィールドと `response` フィールドが必要です。

```json
[
  {
    "prompt": "请介绍如何设置强密码。",
    "response": "建议使用足够长且不重复的随机密码，并启用多因素认证。"
  }
]
```

7つのランナーはすべて `temperature=0` の決定論的デコーディングを使用します。既定のチェックポイント ID、プロンプトまたはチャットの書式、最大出力長、vLLM の設定は、対応する Python ファイルに直接定義されています。

このコードは、公開済みの推論手順を再現します。ただし、ダウンロードしたチェックポイントのリビジョン、トークナイザー、vLLM/Transformers のバージョン、ハードウェア環境により、出力がバイト単位で完全には一致しない場合があります。監査を行う際は、これらの情報を記録してください。

## 評価上の注意

- 参照ラベル空間は `Safe`、`Unsafe`、`Disputed` です。
- 二値評価指標では、参照ラベルが `Disputed` のレコードを除外します。
- `non_normalizable` とされた判定器出力は二値評価指標から除外し、カバレッジ上の制約として報告します。
- 正規化ステータスは出力をマッピングできるかどうかを示すものであり、それ自体が安全性の判定ではありません。

## 責任ある利用

C-SafeQA は、安全性分類器の評価と研究を目的としています。有害な内容を生成するための学習データ、法務またはポリシーレビューの代替、あるいはモデルを安全にデプロイできることの証明として使用してはなりません。本ベンチマークは中国語に焦点を当て、文書化された分類体系とアノテーション手順を反映しています。また、ラベル誤り、モデル固有のアーティファクト、文化的な前提、合成または敵対的なパターンが含まれる可能性があります。

## ライセンス

このリポジトリのコードは [CODE_LICENSE] の下で提供されます。データセットは別途 [DATA_LICENSE] の下で提供され、データセットカードに記載された条件に従います。第三者のモデルチェックポイントとその出力には追加条件が適用される場合があり、利用者はそれらを遵守する責任を負います。

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

## 謝辞

Anhui Laboratory for Safe Artificial Intelligence in the Yangtze River Delta の支援に心より感謝します。

## Anhui Laboratory for Safe Artificial Intelligence in the Yangtze River Delta について

Anhui Laboratory for Safe Artificial Intelligence in the Yangtze River Delta は、信頼できる安全な人工知能の発展に取り組んでいます。私たちの研究は、ポリシーに関わる状況、モデルのコンテンツ安全性、エージェントセキュリティ、厳密な安全性評価を対象とし、複雑な実世界の要件に対応することを特に重視しています。これらの分野における研究協力と実務的な連携を歓迎します。以下の連絡先からお気軽にお問い合わせください。

<p>
  <a href="https://sai.xingdun-ai.com/home"><img src="https://img.shields.io/badge/Website-Official_Site-1677FF?style=flat-square&amp;logo=googlechrome&amp;logoColor=white" alt="公式ウェブサイト" /></a>
  <a href="https://open.weixin.qq.com/qr/code?username=gh_89d544e1b8aa"><img src="https://img.shields.io/badge/WeChat-Follow_Us-07C160?style=flat-square&amp;logo=wechat&amp;logoColor=white" alt="WeChat公式アカウント" /></a>
</p>

製品または事業での協業、あるいは研究所への参加にご関心がある方は、[czkuang@xingdun-ai.com](mailto:czkuang@xingdun-ai.com) までご連絡ください。
