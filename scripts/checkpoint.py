import json
import logging
from pathlib import Path
from utils import resolve_path, safe_open, safe_write_file

CHECKPOINT_FILE = ".skill-creator-progress.json"

def save_checkpoint(phase: str, step: int, metadata: dict) -> None:
    """
    生成進捗をチェックポイントファイルに保存。途中失敗時の再開に使用。
    
    @param phase: 現在のフェーズ名
    @param step: ステップ番号
    @param metadata: 追加メタデータ
    """
    ckpt_path = resolve_path(CHECKPOINT_FILE)
    
    data = {"phase": phase, "step": step, "metadata": metadata}
    try:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        safe_write_file(ckpt_path, content, overwrite=True)
    except Exception as e:
        logging.warning(f"Failed to save checkpoint: {e}")

def load_checkpoint() -> dict | None:
    """
    チェックポイントファイルを読み込み。存在しなければNone。
    
    @return: チェックポイントデータまたはNone
    """
    ckpt_path = resolve_path(CHECKPOINT_FILE)
    if not ckpt_path.exists():
        return None
        
    try:
        with safe_open(ckpt_path, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        logging.warning(f"Failed to load checkpoint: {e}")
        return None

def clear_checkpoint() -> None:
    """
    完了時にチェックポイントファイルを削除する。
    """
    ckpt_path = resolve_path(CHECKPOINT_FILE)
    if ckpt_path.exists():
        try:
            ckpt_path.unlink()
        except OSError:
            pass
