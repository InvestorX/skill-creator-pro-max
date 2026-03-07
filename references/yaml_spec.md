# YAML Frontmatter 仕様 (YAML Spec)

SKILL.md の冒頭に配置されるYAMLメタデータの仕様基準です。生成するスキルはこの仕様に従う必要があります。

## 1. 必須フィールド

### `name` (スキル名)
- **形式**: `kebab-case` のみ (a-z, 0-9, ハイフン)。ハイフン連続や末尾ハイフンは不可。
- **制約**: 64文字以内。
- **禁止ワード**: 予約語（`claude`, `anthropic`, `skill`, `skills`, `agent`, `mcp`）のみで構成される、または名前全体として誤認を招く使い方は避ける。接頭/接尾辞での使用は文脈により許容（例: `data-agent` は可、単なる `agent` は不可）。

### `description` (説明)
- **形式**: 複数行可能（`|` または `>` を利用）。
- **制約**: 1024文字以内。
- **構成**:
  - 【What】何を行うスキルか。
  - 【When】どのようなユースケース、入力でトリガーすべきか。
  - 【Negative】どのような時に実行すべき「でない」か。

### `allowed-tools` (ツールセット)
- **形式**: リスト。
- **制約**: 実行を許可するツールのリスト。
- **許容値**: `Bash`, `WebFetch`, `Read`, `Write`, `computer`
- **備考**: `system_automation` 等、シェル操作が必要な場合は `Bash` を必ず含める。

## 2. 推奨される定義例

```yaml
---
name: monthly-report-generator
description: |
  A skill to generate monthly sales reports from CSV data and upload them to S3.
  Use when the user provides a raw sales CSV file.
  Do NOT use if the user just wants to view a simple text summary.
allowed-tools:
  - Bash
  - Read
  - Write
---
```
