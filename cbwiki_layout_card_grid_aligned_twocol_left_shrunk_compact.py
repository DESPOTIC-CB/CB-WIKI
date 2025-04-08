
import os
from urllib.parse import quote

def scan_directory(base_path):
    html = ""
    for root, dirs, files in os.walk(base_path):
        rel_root = os.path.relpath(root, base_path).replace("\\", "/")
        section_title = rel_root if rel_root != "." else base_path

        pdf_links = []
        for file in sorted(files):
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file).replace('\\', '/')
                web_path = quote(file_path)
                display_name = file.replace(".pdf", "").replace("-", " ").replace("_", " ")
                pdf_links.append(f'      <li><a href="{web_path}" target="_blank">{display_name}</a></li>')

        if pdf_links:
            html += f'  <details>\n    <summary>📁 {section_title}</summary>\n    <ul>\n'
            html += "\n".join(pdf_links)
            html += "\n    </ul>\n  </details>\n"
    return html

def parse_textbox_file(filepath):
    lines = []
    title = None
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("## "):
                    title = line[3:].strip()
                elif line:
                    lines.append(line)
    except:
        pass
    return title, lines

def create_sidebar_boxes():
    html = ""
    for file in sorted(os.listdir()):
        if file.endswith(".txt"):
            title, lines = parse_textbox_file(file)
            if not title:
                title = os.path.splitext(file)[0].replace("_", " ").title()
            html += f'<div class="box">\n<h3>{title}</h3>\n<ul>\n'
            for line in lines:
                if "|" in line:
                    name, url = line.split("|", 1)
                    html += f'<li><a href="{url.strip()}" target="_blank">{name.strip()}</a></li>\n'
                else:
                    html += f"<li>{line}</li>\n"
            html += "</ul>\n</div>\n"
    return html

    html += """
    <div class="box">
      <h3>Visitors</h3>
      <a href="https://hits.sh/despotic-cb.github.io/CB-WIKI/">
        <img alt="Hits" src="https://hits.sh/despotic-cb.github.io/CB-WIKI.svg?style=flat-square&label=visits&color=ffcc00&labelColor=1a1a1a" style="margin-top: 5px;">
      </a>
    </div>
    """

def generate_index_html(output_file="index.html"):
    content = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>CB-Wiki</title>
  <style>
    body {
      margin: 0;

    .info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      justify-items: start;
      gap: 16px;
      background-color: rgba(0, 0, 0, 0.5);
      padding: 20px 60px 60px 60px;
      border-radius: 16px;
      max-width: 1100px;
      margin: 40px auto 60px auto;
    }

    .box {
      background-color: rgba(20, 20, 20, 0.85);
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 0 6px rgba(0, 0, 0, 0.5);
      width: 100%;
      max-width: 360px;
    }

    h3 {
      margin-top: 0;
      font-size: 1.3rem;
    }

    body {
      display: flex;
      justify-content: flex-start;
      flex-direction: column;
      align-items: flex-start;
    }


    .info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      justify-items: stretch;
      gap: 24px;
      background-color: rgba(0, 0, 0, 0.5);
      padding: 20px 40px;
      border-radius: 16px;
      max-width: 1200px;
      margin: 40px 40px 60px 40px;
    }

    .box {
      background-color: rgba(20, 20, 20, 0.85);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 8px rgba(0, 0, 0, 0.6);
    }

    h3 {
      margin-top: 0;
      font-size: 1.4rem;
    }

    body {
      display: flex;
      justify-content: center;
      flex-direction: column;
      align-items: flex-start;
    }


    .info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
      background-color: rgba(0, 0, 0, 0.5);
      padding: 20px 40px;
      border-radius: 16px;
      max-width: 1600px;
      margin: 40px 40px 60px 40px;
    }

    .box {
      background-color: rgba(20, 20, 20, 0.85);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 8px rgba(0, 0, 0, 0.6);
    }

    h3 {
      margin-top: 0;
      font-size: 1.4rem;
    }

    body {
      display: flex;
      justify-content: center;
      flex-direction: column;
      align-items: flex-start;
    }


    .info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      background-color: rgba(0, 0, 0, 0.6);
      padding: 20px;
      border-radius: 12px;
    }
    .box {
      background-color: rgba(20, 20, 20, 0.8);
      border-radius: 6px;
      padding: 10px;
      font-size: 0.85rem;
      box-shadow: 0 0 6px rgba(0, 0, 0, 0.4);
      border-radius: 10px;
      padding: 15px;
    }

      background-image: url('Background.jpg');
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
      background-repeat: no-repeat;
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
      background-color: rgba(20, 20, 20, 0.8);
      border-radius: 6px;
      padding: 10px;
      font-size: 0.85rem;
      box-shadow: 0 0 6px rgba(0, 0, 0, 0.4);
      border: 2px solid #ffe600;
      border-radius: 8px;
      padding: 1rem;
      box-shadow: 0 0 10px #111;
    }
    .box h3 {
      font-size: 1.1rem;
      color: #ffe600;
      margin-top: 0;
    }
    .box ul {
      list-style-type: none;
      padding-left: 0;
    }
    .box li {
      font-size: 0.85rem;
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

    # Melee Damage Formula – hinzugefügt

    content += f"""    </div>
    <div class="info">
{create_sidebar_boxes()}
    </div>
  </div>
  <div class="footer">Created with ❤️ using GitHub Pages</div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Neue index.html erfolgreich erstellt mit Mechanics-Sektion.")

if __name__ == "__main__":
    generate_index_html()
