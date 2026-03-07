# 技术スタック選定ガイド (Tech Stack Guide)

このドキュメントは、ユーザーの要望に応じて最適な技術スタックを決定するための評価基準を定義します。

## 1. 5つの主要カテゴリ

### 1.1 `data_analysis` (データ分析)
- **判定基準**: CSV/JSONデータの集計、統計処理、グラフ描画、データクレンジング。
- **キーワード**: データ, 分析, csv, json, 集計, グラフ, pandas, numpy
- **推奨スタック**: Python (`scripts/main.py`)
- **利用ツール**: pandas, numpy, matplotlib 等

### 1.2 `system_automation` (システム自動化)
- **判定基準**: CLIツール、ファイル/ディレクトリ操作、デプロイ、定期実行ジョブ。
- **キーワード**: bash, コマンド, 自動化, スクリプト, cli, ファイル操作
- **推奨スタック**:
  - **Bash (`scripts/main.sh`)**: 単純なファイル操作、システムコマンド呼び出し。
  - **Python (`scripts/main.py`)**: API連携、スクレイピング、複雑な文字列処理/ファイル変換を含む場合。

### 1.3 `frontend_ui` (フロントエンドUI)
- **判定基準**: Webブラウザで動作する画面、UI、ダッシュボード、Chrome拡張機能。
- **キーワード**: html, css, js, ui, ウェブ, 画面, フロントエンド, chrome拡張
- **推奨スタック**: Tailwind CSS + React
- **Chrome拡張モード**: 
  - Chrome拡張機能の要望があれば、Manifest V3 (`manifest.json`, `popup.html`, `background.js`) 構成とする。
  - **Rust/WebAssemblyモード**: 「画像処理」「暗号化」「大量データの解析・変換」「リアルタイム処理」「複雑な計算」の要望（wasm_triggers）が含まれる場合は、純粋なJS実装ではなく、必ず処理エンジンとして **Rust/wasm-pack** の実装を誘導する。 （`wasm/Cargo.toml`, `wasm/src/lib.rs` を構成に含める）

### 1.4 `backend_api` (バックエンドAPI)
- **判定基準**: サーバーサイド処理、REST/GraphQLエンドポイント、データベース連携。
- **キーワード**: api, サーバー, バックエンド, express, fastapi, データベース
- **推奨スタック**: 
  - Node.js (Express) または Python (FastAPI)。ユーザーの言語指定等に応じて決定。

### 1.5 `document_generation` (ドキュメント生成)
- **判定基準**: xlsx, docx, pptx, pdfの読み書き、操作、スライド化。
- **キーワード**: excel, xlsx, word, docx, powerpoint, pptx, pdf, スプレッドシート, スライド
- **推奨スタック**: 
  - 基本は Anthropic公式提供のテンプレート（`skills/xlsx` 等）を利用する。
  - **PPTX生成モード**: 
    - ユーザーからPPTXスライドの自動生成を求められた場合は、事前に **[SlideKit (HTMLベースで/pptxを活用)]** か **[Marp CLI (Markdownベース)]** のどちらを使用するか確認し、専用テンプレートスタックを構築する。

## 2. フォールバック戦略
- 意図が不明確な場合や複数にまたがる場合は、コンテキストや要件のヒアリングを行い、最も主となる機能をカテゴリとして選定する。
- わからない場合は `data_analysis` (Python) をデフォルトの安全な選択肢として扱う。
