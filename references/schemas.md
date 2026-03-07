# データ構造スキーマ (Schemas)

Skill-Creator-Pro-MAX がスクリプト間で連携するための主要なデータ構造（JSON）定義です。

## 1. Template Fetcher (`fetch_and_customize_template`)

```json
{
  "template_type": "string (e.g., 'pptx', 'slidekit-create')",
  "target_dir": "string (path)",
  "customizations": {
    "additional_columns": ["string"],
    "brand_colors": {
      "primary": "string (hex)",
      "secondary": "string (hex)"
    },
    "custom_prompts": ["string"],
    "metadata_overrides": {},
    "slidekit_options": {}
  }
}
```

## 2. Tech Stack Router (`route_tech_stack`)

```json
{
  "category": "data_analysis | system_automation | frontend_ui | backend_api | document_generation",
  "tech_stack": "python | bash | html_tailwind_react | nodejs | official_template",
  "tools": ["string"],
  "template_path": "string",
  "official_base": "string or null",
  "slidekit_mode": "boolean",
  "marp_mode": "boolean",
  "use_python_for_automation": "boolean",
  "chrome_extension": "boolean",
  "wasm_mode": "boolean",
  "venv_required": "boolean",
  "confidence": "float (0.0-1.0)"
}
```

## 3. Verification Controller / API

```json
{
  "skill_name": "string",
  "timestamp": "ISO 8601 date-time format",
  "changes": [
    {
      "action": "create | modify | delete",
      "target": "file path string",
      "description": "string describing change",
      "reversible": "boolean",
      "dry_run_available": "boolean"
    }
  ],
  "verification_steps": ["string"]
}
```
