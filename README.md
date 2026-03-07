# Skill-Creator-Pro-MAX

エンタープライズグレードのClaudeスキルパッケージを自動生成する拡張版スキル。

## 概要

Skill-Creator-Pro-MAXは、[Anthropic公式skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) を拡張し、マルチファイル構造のスキルパッケージを自動生成します。

### 主な機能

- **技術スタック自動選定** — 5カテゴリ（データ分析 / 自動化 / フロントエンド / バックエンド / ドキュメント生成）
- **全14公式テンプレート統合** — xlsx, docx, pptx, pdf, algorithmic-art 他
- **SlideKit + Marp** — 2パイプラインのPPTX生成
- **Chrome拡張対応** — Manifest V3 + 複雑処理時Rust/WASM誘導
- **美学制約自動注入** — Tailwind CSS標準 / Cyberpunkグリッチエフェクト / ペルソナ対応
- **セキュリティ・ガバナンス** — クレデンシャルチェック / dry-runデフォルト
- **Progressive Disclosure** — SKILL.md理想300行/許容500行

## 対応IDE

| IDE | 対応状況 |
|-----|---------|
| Claude Code | ✅ |
| Antigravity | ✅ |
| Visual Studio Code（Claude拡張） | ✅ |
| Claude.ai | ✅ |
| Cowork | ✅ |

## 使い方

1. このリポジトリをクローンまたはダウンロード
2. Skills対応IDEのスキルディレクトリに配置
3. IDEで「新しいスキルを作りたい」と入力

```
例: 「株価データを分析するスキルを作って」
例: 「Chrome拡張で画像を圧縮するスキルを作って」（→ Rust/WASMに誘導）
例: 「営業報告書のPPTXスライドを自動生成するスキルを作って」
```

## 公式テンプレート参照元

- **Anthropic Skills**: https://github.com/anthropics/skills
- **SlideKit**: https://github.com/nogataka/SlideKit
- **Marp CLI**: https://github.com/marp-team/marp-cli

## ディレクトリ構造

```
skill-creator-pro-max/
├── README.md                          # 本ファイル
├── SKILL.md                           # メインプロンプト（オーケストレーター）
├── LICENSE                            # SUSHI-WARE LICENSE
├── .env.example                       # 環境変数テンプレート
├── .gitignore
│
├── doc/                               # 設計ドキュメント
│   ├── basic_design.md                #   基本設計書
│   ├── detailed_design.md             #   詳細設計書
│   └── requirements_definition.md     #   要件定義書
│
├── scripts/                           # ヘルパースクリプト群
│   ├── utils.py                       #   共通ユーティリティ（パス解決・ファイルI/O）
│   ├── checkpoint.py                  #   チェックポイント・リカバリ
│   ├── env_checker.py                 #   環境依存チェック（Python/Node/Rust等）
│   ├── tech_stack_router.py           #   技術スタック自動選定ルーター
│   ├── template_fetcher.py            #   テンプレート取得（モック）
│   ├── structure_generator.py         #   ディレクトリ構造自動生成
│   ├── yaml_validator.py              #   SKILL.md YAML Frontmatter検証
│   ├── security_checker.py            #   ハードコードクレデンシャル検出
│   └── package_skill.py               #   ZIPパッケージング
│
├── references/                        # 参照ドキュメント（Progressive Disclosure）
│   ├── aesthetics_constraints.md      #   UI美学制約（Tailwind/Cyberpunk/ペルソナ）
│   ├── tech_stack_guide.md            #   技術スタック選定ガイド
│   ├── security_policy.md             #   セキュリティポリシー
│   ├── yaml_spec.md                   #   YAML Frontmatter仕様
│   ├── progressive_disclosure.md      #   段階的開示ガイドライン
│   └── schemas.md                     #   スクリプト間通信JSONスキーマ
│
├── assets/                            # テンプレート・ダミーデータ
│   ├── mock_dummy_data/               #   テスト生成用ダミーデータ
│   └── skill_templates/               #   カテゴリ別スキルテンプレート
│       ├── python_general/            #     Python汎用テンプレート
│       │   └── main_template.py
│       ├── bash_automation/           #     Bash自動化テンプレート
│       │   └── main_template.sh
│       ├── frontend_tailwind/         #     React + Tailwindテンプレート
│       │   └── App.jsx
│       ├── chrome_extension_wasm/     #     Chrome拡張 + Rust/WASMテンプレート
│       │   └── manifest.json
│       ├── backend_api/               #     Node.js/Expressテンプレート
│       │   └── server_template.js
│       └── document_gen/              #     ドキュメント生成テンプレート
│           └── excel_template.py
│
├── templates/                         # 公式テンプレート参照定義
│   └── official/
│       ├── templates.json             #   全14公式テンプレートURL一覧
│       ├── slidekit/
│       │   └── meta.json              #   SlideKitメタデータ
│       └── marp/
│           └── meta.json              #   Marp CLIメタデータ
│
├── tests/                             # テストスイート
│   ├── test_prompts.json              #   テストプロンプト集
│   ├── run_tests.py                   #   テスト実行スクリプト
│   └── sample_data/                   #   サンプルデータ
│       ├── generate_samples.py        #     ダミーデータ生成スクリプト
│       ├── test_data.csv              #     テスト用CSV
│       ├── test_config.json           #     テスト用設定JSON
│       └── test_slide.md              #     テスト用Marpスライド
│
├── evals/                             # 評価プロンプトセット
│   └── evals.json                     #   評価メトリクス定義
│
├── agents/                            # 評価エージェント
│   ├── grader.md                      #   採点エージェント
│   ├── comparator.md                  #   比較エージェント
│   └── analyzer.md                    #   分析エージェント
│
└── eval-viewer/                       # 評価結果ビューア
    ├── generate_review.py             #   HTML評価レポート生成スクリプト
    └── index.html                     #   生成済みサンプルレポート
```

## テスト

```powershell
python scripts/yaml_validator.py --test
python scripts/security_checker.py --test
python scripts/tech_stack_router.py --test
python tests/run_tests.py
```

## セキュリティ

- APIキー等は `.env` ファイルで管理（`.env.example` を参照）
- スクリプト内へのクレデンシャルハードコードは禁止
- 破壊的コマンドはデフォルトで `--dry-run` を適用

## ライセンス

[SUSHI-WARE LICENSE](https://github.com/MakeNowJust/sushi-ware)

> "THE SUSHI-WARE LICENSE"
> <because@sushi.ware> wrote this. As long as you retain this notice you
> can do whatever you want with this stuff. If we meet some day, and you think
> this stuff is worth it, you can buy me a sushi 🍣 in return.
