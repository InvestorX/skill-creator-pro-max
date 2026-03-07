import re
import argparse
import sys
from utils import safe_read_file, resolve_path

VALIDATION_RULES = {
    "name": {
        "pattern": r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$",
        "max_length": 64,
        "reserved_words": {"claude", "anthropic", "skill", "skills", "agent", "mcp"}
    },
    "description": {
        "max_length": 1024,
        "warning_if_missing": ["when", "negative"]
    },
    "allowed-tools": {
        "valid_values": {"Bash", "WebFetch", "Read", "Write", "computer"}
    }
}

def validate_yaml_frontmatter(skill_md_path: str) -> dict:
    """
    SKILL.md のYAML Frontmatterを検証する。
    """
    path = resolve_path(skill_md_path)
    content = safe_read_file(path)
    
    # 簡易YAMLパーサー（Frontmatter部分の抽出）
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {"valid": False, "errors": [{"message": "No YAML frontmatter found"}], "warnings": [], "suggestions": []}
        
    yaml_text = match.group(1)
    
    # 手動簡易パース（本来はPyYAML等を使うべきだが、依存関係の排除のため）
    parsed = {}
    current_key = None
    for line in yaml_text.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        if line.startswith('  -'):
            if current_key and isinstance(parsed[current_key], list):
                parsed[current_key].append(line[3:].strip())
        elif ':' in line:
            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip()
            if not v and k == "allowed-tools":
                parsed[k] = []
                current_key = k
            elif v == "|":
                parsed[k] = ""
                current_key = k
            else:
                parsed[k] = v
                current_key = None
        elif current_key and isinstance(parsed[current_key], str):
            parsed[current_key] += " " + line.strip()

    errors = []
    warnings = []
    
    # name
    name = parsed.get('name', '')
    if not name:
        errors.append({"field": "name", "message": "name is required"})
    else:
        if len(name) > VALIDATION_RULES["name"]["max_length"]:
            errors.append({"field": "name", "message": f"name length exceeds {VALIDATION_RULES['name']['max_length']}"})
        if not re.match(VALIDATION_RULES["name"]["pattern"], name):
            errors.append({"field": "name", "message": "name must be kebab-case"})
        if name in VALIDATION_RULES["name"]["reserved_words"]:
            errors.append({"field": "name", "message": f"name '{name}' is a reserved word"})

    # description
    desc = parsed.get('description', '')
    if not desc:
        errors.append({"field": "description", "message": "description is required"})
    else:
        if len(desc) > VALIDATION_RULES["description"]["max_length"]:
            errors.append({"field": "description", "message": "description exceeds max length"})
        
        # When / Negative check
        desc_lower = desc.lower()
        if "when" not in desc_lower and "use this" not in desc_lower:
            warnings.append({"field": "description", "message": "Consider adding a 'when' condition clause"})
        if "not use" not in desc_lower and "do not" not in desc_lower and "never" not in desc_lower:
            warnings.append({"field": "description", "message": "Consider adding negative triggering examples"})

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "suggestions": ["Make sure the description is clear and concise."]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.test:
        from utils import safe_write_file, resolve_path
        test_path = resolve_path("test-skill.md")
        safe_write_file(test_path, "---\nname: invalid_name\ndescription: Too short.\n---\nBody")
        res = validate_yaml_frontmatter(test_path)
        assert res["valid"] is False
        assert any("kebab-case" in str(e) for e in res["errors"])
        test_path.unlink()
        print("YAML Validator tests passed.")
        sys.exit(0)
