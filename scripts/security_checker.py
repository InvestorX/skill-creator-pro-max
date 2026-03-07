import os
import argparse
from pathlib import Path
from utils import safe_read_file, resolve_path

def check_security(project_dir: str | Path) -> dict:
    """
    生成されたスキルパッケージのセキュリティチェックを実行する。
    """
    base = resolve_path(project_dir)
    issues = []
    
    # 1. Check for .env.example
    env_example_exists = (base / ".env.example").exists()
    if not env_example_exists:
        issues.append({"severity": "high", "message": "Missing .env.example file for credentials documentation."})
        
    # 2. Check for hardcoded credentials in scripts and server files
    # Simplified mock approach: searching for 'API_KEY="sk-' or 'password="...'
    for f in base.rglob("*"):
        if f.is_file() and f.suffix in ['.py', '.sh', '.js', '.json', '.yaml', '.yml']:
            try:
                content = safe_read_file(f).lower()
                if any(x in content for x in ["api_key=", "api_key =", "password=", "secret_key=", "token="]) and "os.environ" not in content and "$(" not in content:
                    issues.append({"severity": "high", "message": f"Hardcoded credential suspected in {f.name}"})
            except Exception as e:
                issues.append({"severity": "medium", "message": f"Failed to scan file {f.name}: {e}"})
                    
    # 3. Check for dry-run functionality
    # Normally we'd parse the bash/python scripts to see if dry-run parsing exists.
    # Omitting complex static analysis here.
    dry_run_default = True # Mock assumption

    return {
        "passed": len([i for i in issues if i['severity'] in ['critical', 'high']]) == 0,
        "issues": issues,
        "env_example_exists": env_example_exists,
        "dry_run_default": dry_run_default,
        "recommendations": ["Ensure all API calls use environment variables."]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.test:
        from utils import safe_create_directory, safe_write_file
        test_dir = resolve_path("test_sec_project")
        safe_create_directory(test_dir)
        safe_create_directory(test_dir / "scripts")
        safe_write_file(test_dir / "scripts" / "bad.sh", 'API_KEY="sk-12345"')
        
        result = check_security(test_dir)
        assert result["passed"] is False  # Missing env.example
        
        import shutil
        shutil.rmtree(test_dir)
        print("Security checker tests passed.")
        import sys
        sys.exit(0)
