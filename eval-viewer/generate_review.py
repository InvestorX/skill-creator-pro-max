import json
import sys
import html
from pathlib import Path

def generate_html(data):
    """
    Generates a simple Sakura Pink themed HTML report from evaluation results
    """
    html_output = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill-Creator-Pro-MAX Eval Results</title>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 2rem;
            background: linear-gradient(135deg, #ffffff 0%, #ffe4ec 50%, #e0f7fa 100%);
            color: #333;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(255, 107, 157, 0.15);
            padding: 2rem;
            backdrop-filter: blur(10px);
        }}
        h1 {{
            color: #ff6b9d;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,212,255,0.2);
        }}
        .card {{
            background: #fff;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #00d4ff;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(255, 107, 157, 0.2);
        }}
        .score {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #00d4ff;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #ffe4ec;
        }}
        th {{
            color: #ff6b9d;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Evaluation Results Overview</h1>
        <div id="results">
"""
    
    # Mock rendering based on general data shape
    # For a real implementation, it would iterate over JSON
    test_id = html.escape(str(data.get("test_id", "Unknown")))
    intent = html.escape(str(data.get("intent", "...")))
    scores = data.get("scores", {})
    feedback = html.escape(str(data.get("feedback", "No feedback available")))
    
    html_output += f"""
            <div class="card">
                <h2>Test ID: {test_id}</h2>
                <p><strong>Intent:</strong> {intent}</p>
                <table>
                    <tr><th>Metric</th><th>Score</th></tr>
"""
    for k, v in scores.items():
        html_output += f"<tr><td>{html.escape(str(k))}</td><td class='score'>{html.escape(str(v))}</td></tr>"
        
    html_output += f"""
                </table>
                <p style="margin-top: 1.5rem; padding: 1rem; background: #f9f9f9; border-radius: 8px;">
                    <strong>Feedback:</strong> {feedback}
                </p>
            </div>
"""

    html_output += """
        </div>
    </div>
</body>
</html>
"""
    return html_output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Generate mock report")
    args = parser.parse_args()
    
    if args.mock:
        mock_data = {
            "test_id": "eval-001",
            "intent": "Generate a sales report CSV to Excel with charts",
            "scores": {
                "intent_satisfaction": "5/5",
                "security": "Pass",
                "aesthetics": "N/A",
                "progressive_disclosure": "5/5"
            },
            "feedback": "Perfectly routed to document_generation using xlsx template. Excellent execution."
        }
        output = generate_html(mock_data)
        out_path = Path(__file__).parent / "index.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Mock viewer generated at {out_path}")
    else:
        print("Provide input data JSON via stdin or use --mock")
