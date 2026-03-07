import json
import sys
import argparse

CATEGORY_KEYWORDS = {
    "document_generation": {
        "primary": ["excel", "xlsx", "word", "docx", "powerpoint", "pptx", "pdf",
                     "スプレッドシート", "ワード", "パワーポイント", "ドキュメント",
                     "スライド", "プレゼン", "プレゼンテーション"],
        "secondary": ["テンプレート", "帳票", "レポート", "フォーマット", "書式"],
        "slidekit_triggers": ["pptx", "powerpoint", "パワーポイント", "スライド",
                              "プレゼン", "プレゼンテーション"],
        "official_templates": {
            "xlsx": "https://github.com/anthropics/skills/tree/main/skills/xlsx",
            "docx": "https://github.com/anthropics/skills/tree/main/skills/docx",
            "pptx": "https://github.com/anthropics/skills/tree/main/skills/pptx",
            "pdf": "https://github.com/anthropics/skills/tree/main/skills/pdf"
        },
        "external_templates": {
            "slidekit": "https://github.com/nogataka/SlideKit",
            "marp": "https://github.com/marp-team/marp-cli"
        }
    },
    "data_analysis": {
        "primary": ["データ", "分析", "csv", "json", "集計", "グラフ", "統計",
                     "pandas", "numpy", "data", "analysis", "aggregate"],
        "secondary": ["前処理", "クレンジング", "可視化", "ETL", "変換"]
    },
    "frontend_ui": {
        "primary": ["html", "css", "javascript", "ui", "ウェブ", "web", "画面",
                     "フロントエンド", "frontend", "ダッシュボード", "dashboard",
                     "react", "tailwind", "next.js", "vite",
                     "chrome拡張", "chrome extension", "拡張機能", "ブラウザ拡張"],
        "secondary": ["デザイン", "レイアウト", "インタラクティブ", "アニメーション",
                       "コンポーネント", "SPA", "manifest.json", "popup", "content script"],
        "wasm_triggers": ["画像処理", "暗号化", "複雑な計算", "大量データ",
                          "wasm", "webassembly", "rust", "wasm-pack",
                          "パフォーマンス", "高速化", "バイナリ"]
    },
    "backend_api": {
        "primary": ["api", "サーバー", "server", "バックエンド", "backend",
                     "rest", "graphql", "express", "fastapi", "node",
                     "エンドポイント", "endpoint", "マイクロサービス"],
        "secondary": ["データベース", "db", "認証", "auth", "ミドルウェア",
                       "ルーティング", "CRUD"]
    },
    "system_automation": {
        "primary": ["bash", "shell", "コマンド", "自動化", "スクリプト", "cli",
                     "cron", "デプロイ", "ファイル操作", "automation"],
        "secondary": ["バックアップ", "監視", "ログ", "パイプライン"],
        "python_triggers": ["ファイル変換", "API連携", "スクレイピング", "scraping",
                            "データ加工", "メール", "通知", "PDF操作"]
    }
}

def analyze_keywords(text: str) -> dict[str, int]:
    text_lower = text.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for word in keywords["primary"]:
            if word in text_lower:
                scores[category] += 2
        for word in keywords["secondary"]:
            if word in text_lower:
                scores[category] += 1
                
    # トリガーによる特別加算
    if has_trigger(text, CATEGORY_KEYWORDS["system_automation"].get("python_triggers", [])):
        scores["system_automation"] += 3
        
    if has_trigger(text, CATEGORY_KEYWORDS["frontend_ui"].get("wasm_triggers", [])):
        scores["frontend_ui"] += 2
        
    return scores

def has_trigger(text: str, triggers: list[str]) -> bool:
    text_lower = text.lower()
    return any(trigger in text_lower for trigger in triggers)

def route_tech_stack(user_intent: str) -> dict:
    """
    ユーザーの意図テキストから最適な技術スタックを選定する。
    
    @param user_intent: ユーザーの目的記述テキスト（自然言語）
    @return: 選定結果の辞書
    @throws ValueError: user_intentが空文字の場合
    """
    if not user_intent or not user_intent.strip():
        raise ValueError("user_intent cannot be empty")
        
    scores = analyze_keywords(user_intent)
    
    # 決定されたカテゴリ（一番スコアが高いもの、同点なら固定優先順）
    preferred_order = ["document_generation", "frontend_ui", "backend_api", "data_analysis", "system_automation"]
    best_category = "data_analysis"
    max_score = 0
    
    for category in preferred_order:
        if scores[category] > max_score:
            best_category = category
            max_score = scores[category]
    
    # スコアが0ならデフォルトフォールバック
    if max_score == 0:
        best_category = "data_analysis"
        
    confidence = min(max_score / 4.0, 1.0) if max_score > 0 else 0.5
    
    result = {
        "category": best_category,
        "tech_stack": "python",
        "tools": [],
        "template_path": "",
        "official_base": None,
        "slidekit_mode": False,
        "marp_mode": False,
        "use_python_for_automation": False,
        "chrome_extension": False,
        "wasm_mode": False,
        "venv_required": False,
        "confidence": confidence
    }
    
    if best_category == "document_generation":
        result["tech_stack"] = "official_template"
        keyword_map = {
            "xlsx": ["excel", "xlsx", "スプレッドシート"],
            "docx": ["word", "docx", "ワード"],
            "pdf": ["pdf"]
        }
        for template_key, words in keyword_map.items():
            if any(word in user_intent.lower() for word in words):
                result["official_base"] = CATEGORY_KEYWORDS["document_generation"]["official_templates"][template_key]
            
        if has_trigger(user_intent, CATEGORY_KEYWORDS["document_generation"]["slidekit_triggers"]):
            # SlideKit vs Marp の選択。今回は自然言語から「Marp」とあればMarp、なければSlideKit判定
            if "marp" in user_intent.lower() or "markdown" in user_intent.lower():
                result["marp_mode"] = True
                result["tools"] = ["marp-cli"]
            else:
                result["slidekit_mode"] = True
                result["official_base"] = CATEGORY_KEYWORDS["document_generation"]["official_templates"]["pptx"]
                result["tools"] = ["slidekit"]
    
    elif best_category == "data_analysis":
        result["tech_stack"] = "python"
        result["tools"] = ["pandas", "numpy"]
        result["venv_required"] = True
        
    elif best_category == "frontend_ui":
        result["tech_stack"] = "html_tailwind_react"
        result["tools"] = ["tailwind", "react"]
        
        # Chrome拡張判定
        if has_trigger(user_intent, ["chrome", "extension", "拡張"]):
            result["chrome_extension"] = True
            result["tools"].append("chrome_extension")
            
            # WASM誘導判定
            if has_trigger(user_intent, CATEGORY_KEYWORDS["frontend_ui"]["wasm_triggers"]):
                result["wasm_mode"] = True
                result["tools"].append("wasm")
                
    elif best_category == "backend_api":
        # node vs python判定
        if "python" in user_intent.lower() or "fastapi" in user_intent.lower():
            result["tech_stack"] = "python"
            result["tools"] = ["fastapi"]
            result["venv_required"] = True
        else:
            result["tech_stack"] = "nodejs"
            result["tools"] = ["express"]
            
    elif best_category == "system_automation":
        if has_trigger(user_intent, CATEGORY_KEYWORDS["system_automation"]["python_triggers"]) or "python" in user_intent.lower():
            result["tech_stack"] = "python"
            result["use_python_for_automation"] = True
            result["venv_required"] = True
        else:
            result["tech_stack"] = "bash"

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skill-Creator-Pro-MAX Tech Stack Router Test")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("intent", nargs="*", help="User intent string")
    args = parser.parse_args()

    if args.test:
        test_cases = [
            ("画面の見た目をかっこよくしてAIチャットのChrome拡張を作って", "frontend_ui", True, False),
            ("Chrome拡張で画像をフィルタリングして暗号化・圧縮したい", "frontend_ui", True, True),
            ("Excelの売上データを集計してグラフ化する", "data_analysis", False, False),
            ("スライドをいい感じに作ってPPTXで出力して", "document_generation", False, False),
            ("サーバー作ってREST APIでDB保存したい", "backend_api", False, False),
            ("スクレイピングしてJSONに変換するスクリプト", "system_automation", False, False),
        ]
        all_passed = True
        for intent, expected_cat, expected_ext, expected_wasm in test_cases:
            res = route_tech_stack(intent)
            pass_cat = res["category"] == expected_cat
            pass_ext = res["chrome_extension"] == expected_ext
            pass_wasm = res["wasm_mode"] == expected_wasm
            
            print(f"[{'PASS' if pass_cat and pass_ext and pass_wasm else 'FAIL'}] {intent}\n"
                  f"  Got: cat={res['category']} ext={res['chrome_extension']} wasm={res['wasm_mode']}\n"
                  f"  Exp: cat={expected_cat} ext={expected_ext} wasm={expected_wasm}")
            if not (pass_cat and pass_ext and pass_wasm):
                all_passed = False
                
        if all_passed:
            print("\nAll tech stack router tests passed.")
            sys.exit(0)
        else:
            print("\nSome tests failed.")
            sys.exit(1)
    else:
        intent_str = " ".join(args.intent)
        if not intent_str:
            print(json.dumps({"error": "No intent provided"}))
            sys.exit(1)
        print(json.dumps(route_tech_stack(intent_str), indent=2, ensure_ascii=False))
