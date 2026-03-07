import zipfile
from pathlib import Path
from utils import resolve_path

def package_skill(project_dir: str | Path, output_zip: str | Path):
    """
    指定ディレクトリをZIPにパッケージングする
    """
    base_dir = resolve_path(project_dir)
    out_file = resolve_path(output_zip)
    
    if not base_dir.exists() or not base_dir.is_dir():
        raise FileNotFoundError(f"Project directory not found: {base_dir}")
        
    with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root_path, dirs, files in base_dir.walk():
            # 無視ディレクトリ
            if "node_modules" in dirs: dirs.remove("node_modules")
            if "__pycache__" in dirs: dirs.remove("__pycache__")
            if "target" in dirs: dirs.remove("target")
            
            for file in files:
                lower_f = file.lower()
                if lower_f.endswith('.zip') or lower_f.startswith(".env") or "credential" in lower_f or "secret" in lower_f or lower_f == ".npmrc":
                    continue
                file_path = root_path / file
                if file_path.is_symlink():
                    continue
                arcname = file_path.relative_to(base_dir)
                zipf.write(file_path, arcname)

    return out_file.exists()

if __name__ == "__main__":
    print("Packaging module loaded.")
