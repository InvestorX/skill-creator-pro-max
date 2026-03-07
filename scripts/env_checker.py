import shutil
import subprocess

def _check_command(command: str) -> dict:
    """
    コマンドが存在するか、およびそのバージョンを確認する内部関数。
    """
    if not shutil.which(command):
        return {"available": False, "version": None}
    try:
        # 多くのコマンドは --version をサポートしている
        result = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            return {"available": True, "version": version.split('\n')[0][:50]} # 最初の行のみ
    except Exception:
        pass
        
    return {"available": True, "version": "unknown"}

def check_environment() -> dict:
    """
    実行環境の必要ツール・ランタイムの有無を検出する。
    
    @return: 環境チェック結果
        {
            "python": {"available": bool, "version": str|None},
            "node": {"available": bool, "version": str|None},
            "npm": {"available": bool, "version": str|None},
            "marp": {"available": bool, "version": str|None},
            "git": {"available": bool, "version": str|None},
            "rustup": {"available": bool, "version": str|None},
            "wasm-pack": {"available": bool, "version": str|None},
            "copilot": {"available": bool, "version": str|None},
            "missing": list[str],    # 不足ツール名リスト
            "guidance": list[str]    # インストールガイダンス
        }
    """
    results = {
        "python": _check_command("python"),
        "node": _check_command("node"),
        "npm": _check_command("npm"),
        "marp": _check_command("marp"),
        "git": _check_command("git"),
        "rustup": _check_command("rustup"),
        "wasm-pack": _check_command("wasm-pack"),
        "copilot": _check_command("copilot"),
        "missing": [],
        "guidance": []
    }
    
    if not results["python"]["available"]:
        results["missing"].append("python")
        results["guidance"].append("Pythonはデータ分析や自動化全般で推奨されます。インストールをご検討ください。")
        
    if not results["node"]["available"]:
        results["missing"].append("node")
        results["guidance"].append("Node.jsはフロントエンド(React, Tailwind)やバックエンド(Express)で必要です。")
        
    if not results["rustup"]["available"] or not results["wasm-pack"]["available"]:
        results["missing"].extend([c for c in ["rustup", "wasm-pack"] if not results[c]["available"]])
        results["guidance"].append("Rust/WASM（Chrome拡張時の複雑処理）を使う場合は、rustupとwasm-packをインストールしてください。")
        
    if not results["copilot"]["available"]:
        results["missing"].append("copilot")
        results["guidance"].append("GitHub Copilot CLIが未インストールです。自動コードレビューに必要です。(`npm install -g @githubnext/github-copilot-cli`)")

    return results

if __name__ == "__main__":
    import json
    print(json.dumps(check_environment(), indent=2, ensure_ascii=False))
