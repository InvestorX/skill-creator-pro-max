import json
from pathlib import Path

def main():
    prompts_file = Path(__file__).parent / "test_prompts.json"
    if not prompts_file.exists():
        print("test_prompts.json not found")
        return
        
    with open(prompts_file, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
        
    for p in prompts:
        print(f"[{p['id']}] Intent: {p['intent']}")
        print(f"  -> Expects: {p['expected_category']}\n")

if __name__ == "__main__":
    main()
