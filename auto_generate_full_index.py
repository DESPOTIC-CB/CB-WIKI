import os
from urllib.parse import quote

def scan_directory(base_path):
    html = ""
    for root, dirs, files in os.walk(base_path):
        rel_root = os.path.relpath(root, base_path).replace("\\", "/")
        if rel_root == ".":
            section_title = base_path
        else:
            section_title = rel_root

        pdf_links = []
        for file in sorted(files):
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file).replace('\\', '/')
                web_path = quote(file_path)
                display_name = file.replace(".pdf", "").replace("-", " ").replace("_", " ")
                pdf_links.append(f'      <li><a href="{web_path}" target="_blank">{display_name}</a></li>')

        if pdf_links:
            html += f'  <details open>\n    <summary>📁 {section_title}</summary>\n    <ul>\n'
            html += "\n".join(pdf_links)
            html += "\n    </ul>\n  </details>\n"
    return html

def generate_index_html(output_file="index.html"):
    content = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>CB-Wiki</title>
  <style>
    body {
      background-color: #1e1e1e;
      color: #f0f0f0;
      font-family: 'Segoe UI', sans-serif;
      max-width: 900px;
      margin: 2rem auto;
      padding: 1rem;
    }
    h1 {
      text-align: center;
      color: #ffcc00;
      font-size: 2.4rem;
    }
    details {
      background-color: #2a2a2a;
      border: 1px solid #444;
      border-radius: 5px;
      margin-bottom: 1rem;
      padding: 0.5rem;
    }
    summary {
      font-weight: bold;
      font-size: 1.1rem;
      cursor: pointer;
    }
    a {
      color: #66ccff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    ul {
      list-style-type: none;
      padding-left: 1.2rem;
    }
    .footer {
      margin-top: 3rem;
      font-size: 0.85rem;
      color: #888;
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>📘 CB-Wiki</h1>
"""
    # Scanne alle Top-Level-Ordner (außer .git)
    for folder in sorted(os.listdir()):
        if os.path.isdir(folder) and not folder.startswith("."):
            content += f"<h2>📂 {folder}</h2>\n"
            content += scan_directory(folder)

    content += """
  <div class="footer">Created with ❤️ using GitHub Pages</div>
</body>
</html>"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Neue index.html erfolgreich erstellt: {output_file}")

if __name__ == "__main__":
    generate_index_html()
