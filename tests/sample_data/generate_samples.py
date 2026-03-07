import sys
from pathlib import Path

base_dir = Path(__file__).parent

# Create dummy CSV
with open(base_dir / "test_data.csv", "w", encoding="utf-8") as f:
    f.write("date,sales,region\n")
    f.write("2024-01-01,100,North\n")
    f.write("2024-01-02,150,South\n")
    f.write("2024-01-03,200,North\n")

# Create dummy JSON
with open(base_dir / "test_config.json", "w", encoding="utf-8") as f:
    f.write('{"api_key": "dummy", "threshold": 100}\n')

# Create dummy Markdown
with open(base_dir / "test_slide.md", "w", encoding="utf-8") as f:
    f.write("---\nmarp: true\ntheme: default\n---\n# Slide 1\nHello World\n---\n# Slide 2\nTest Data.\n")

print("Created sample test data files in tests/sample_data/")
