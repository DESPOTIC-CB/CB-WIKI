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
      margin: 0;
      background-color: #2b2b2b;
      font-family: Arial, sans-serif;
      color: #f1f1f1;
      line-height: 1.6;
    }
    .wrapper {
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 2rem;
      gap: 2rem;
    }
    .content {
      flex: 2;
      max-width: 800px;
    }
    .info {
      width: 300px;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .box {
      background-color: #333;
      border: 2px solid #ffe600;
      border-radius: 8px;
      padding: 1rem;
      box-shadow: 0 0 10px #111;
    }
    .box h3 {
      color: #ffe600;
      margin-top: 0;
    }
    .box ul {
      list-style-type: none;
      padding-left: 0;
    }
    .box li {
      margin: 0.3rem 0;
    }
    h1 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: #ffe600;
    }
    details {
      background-color: #444;
      border-radius: 5px;
      margin: 1rem 0;
      padding: 0.5rem 1rem;
    }
    summary {
      font-size: 1.1rem;
      font-weight: bold;
      cursor: pointer;
    }
    ul {
      list-style-type: none;
      padding-left: 1rem;
    }
    li {
      margin: 0.3rem 0;
    }
    a {
      color: #66ccff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .footer {
      margin-top: 3rem;
      font-size: 0.85rem;
      text-align: center;
      color: #999;
    }
  </style>
</head>
<body>
  <h1>📘 CB-Wiki</h1>
  <div class="wrapper">
    <div class="content">
"""
    for folder in sorted(os.listdir()):
        if os.path.isdir(folder) and not folder.startswith("."):
            content += f"<h2>📂 {folder}</h2>\n"
            content += scan_directory(folder)

    content += """    </div>
    <div class="info">
      <div class="box">
        <h3>🎁 Current In-Game Codes</h3>
        <ul>
          <li>CBSPRING2025</li>
          <li>BLADEGOLD</li>
          <li>HERO2025</li>
        </ul>
      </div>
      <div class="box">
        <h3>📺 Recommended Creators</h3>
        <ul>
          <li><a href="https://twitch.tv/example1" target="_blank">StreamerOne</a></li>
          <li><a href="https://youtube.com/@example2" target="_blank">YT Channel Two</a></li>
        </ul>
      </div>
      <div class="box">
        <h3>💬 Discord Servers</h3>
        <ul>
          <li><a href="https://discord.gg/example1" target="_blank">Main CB Discord</a></li>
          <li><a href="https://discord.gg/example2" target="_blank">House Community</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer">Created with ❤️ using GitHub Pages</div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Neue index.html erfolgreich erstellt: {output_file}")

if __name__ == "__main__":
    generate_index_html()
