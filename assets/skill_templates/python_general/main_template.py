import sys
import argparse
from pathlib import Path

def setup_argparse() -> argparse.ArgumentParser:
    """
    引数パーサーをセットアップする。
    """
    parser = argparse.ArgumentParser(description="Script Description Here")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-o", "--output", default="output.json", help="Path to output file")
    parser.add_argument("--dry-run", action="store_true", help="実行せずに結果のみを出力する")
    return parser

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Processing {input_path}...")
    
    # --- YOUR LOGIC HERE ---
    
    if args.dry_run:
        print("[DRY RUN] The output would be written to:", output_path)
    else:
        # with open(output_path, 'w', encoding='utf-8') as f:
        #     f.write("result")
        print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
