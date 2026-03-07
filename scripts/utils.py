import os
from pathlib import Path

def resolve_path(*parts: str) -> Path:
    """
    OS非依存のパスを生成する。全スクリプトでこの関数を使用。
    os.path.joinの使用を避け、必ずpathlib.Pathを用いる。
    
    @param parts: パスの構成要素
    @return: 結合されたPathオブジェクト
    """
    return Path(*parts).resolve()

def safe_open(filepath: str | Path, mode: str = 'r'):
    """
    UTF-8エンコーディングでファイルを開く。全スクリプトでこの関数を使用。
    
    @param filepath: ファイルパス
    @param mode: オープンモード ('r', 'w', 'a')
    @return: ファイルオブジェクト
    """
    return open(filepath, mode, encoding='utf-8')

def safe_create_directory(path: str | Path, exist_ok: bool = True) -> bool:
    """
    既存チェック付きディレクトリ作成。存在する場合はスキップ。
    
    @param path: 作成するディレクトリパス
    @param exist_ok: 既存時にエラーを出さないか
    @return: 新規作成された場合True、既に存在した場合False
    """
    p = Path(path)
    if p.exists():
        return False
    p.mkdir(parents=True, exist_ok=exist_ok)
    return True

def safe_write_file(path: str | Path, content: str, overwrite: bool = False) -> bool:
    """
    既存ファイルチェック付き書き込み。上書き確認あり。
    
    @param path: ファイルパス
    @param content: 書き込み内容
    @param overwrite: 上書き許可フラグ
    @return: 書き込み成功時True
    @throws FileExistsError: overwrite=Falseで既存ファイルがある場合
    """
    p = Path(path)
    if p.exists() and not overwrite:
        raise FileExistsError(f"FIle already exists: {path}")
        
    with safe_open(p, 'w') as f:
        f.write(content)
    return True

def safe_read_file(path: str | Path) -> str:
    """
    安全にファイルを読み込むユーティリティ関数。
    
    @param path: ファイルパス
    @return: 読み込んだファイル内容文字列
    @throws FileNotFoundError: ファイルが存在しない場合
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
        
    with safe_open(p, 'r') as f:
        return f.read()
