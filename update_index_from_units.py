import os
from urllib.parse import quote

def generate_html_from_units(base_path="Units", output_file="index.html"):
    html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>CB-Wiki</title>
  <style>
    body {
      background-color: #1e1e1e;
      color: #f0f0f0;
      font-family: 'Segoe UI', sans-serif;
      margin: 2rem auto;
      max-width: 900px;
      padding: 1rem;
      line-height: 1.6;
    }
    h1 {
      text-align: center;
      font-size: 2.4rem;
      color: #ffcc00;
    }
    h2 {
      color: #66ccff;
      margin-top: 2rem;
      border-bottom: 1px solid #444;
      padding-bottom: 0.3rem;
    }
    summary {
      font-size: 1.1rem;
      font-weight: bold;
      cursor: pointer;
      padding: 6px;
    }
    details {
      margin-bottom: 1rem;
      border: 1px solid #444;
      border-radius: 6px;
      background-color: #2a2a2a;
    }
    ul {
      list-style-type: none;
      padding-left: 1.2rem;
    }
    li {
      margin: 0.4rem 0;
    }
    a {
      color: #66ccff;
      text-decoration: none;
    }
    a:hover {
      color: white;
      text-decoration: underline;
    }
    .footer {
      margin-top: 4rem;
      font-size: 0.85rem;
      text-align: center;
      color: #888;
    }
  </style>
</head>
<body>
  <h1>📘 CB-Wiki</h1>
  <h2>⚔️ Units</h2>
"""

    for folder in sorted(os.listdir(base_path)):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            html += f'  <details open>\n    <summary>📁 {folder}</summary>\n    <ul>\n'
            for file in sorted(os.listdir(folder_path)):
                if file.lower().endswith('.pdf'):
                    encoded_path = quote(f"{base_path}/{folder}/{file}".replace("\\", "/"))
                    display_name = file.replace(".pdf", "").replace("-", " ").replace("_", " ")
                    html += f'      <li><a href="{encoded_path}" target="_blank">{display_name}</a></li>\n'
            html += "    </ul>\n  </details>\n"

    html += """  <div class="footer">
    Created with ❤️ using GitHub Pages
  </div>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Neue index.html erfolgreich erstellt: {output_file}")

if __name__ == "__main__":
    generate_html_from_units()
