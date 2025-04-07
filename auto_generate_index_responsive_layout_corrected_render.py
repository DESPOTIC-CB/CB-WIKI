
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

def generate_index_html(output_file="index.html"):
    content = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>CB-Wiki</title>
  
<style>
  body {
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #1e1e1e;
    color: #e0e0e0;
  }
  .wrapper {
    display: flex;
    flex-direction: row;
    min-height: 100vh;
  }
  .sidebar {
    width: 260px;
    padding: 1rem;
    background-color: #1e1e1e;
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    overflow-y: auto;
    border-right: 1px solid #333;
  }
  .content {
    margin-left: 280px;
    padding: 2rem;
    max-width: 1000px;
    flex: 1;
  }
  h1 {
    color: #ffe600;
  }
  .card {
    background-color: #2a2a2a;
    border: 2px solid #ffe600;
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 1rem;
  }
  .card h3 {
    margin: 0 0 10px 0;
    color: #ffe600;
  }
  .card ul {
    padding-left: 20px;
    margin: 0;
  }
  .card ul li {
    margin-bottom: 4px;
  }
  .info {
    margin-top: 2rem;
  }
</style>

</head>
<body>
<div class="wrapper">

<div class="sidebar">
  <div class="card"><h3>Current Active Codes</h3><p>Coming soon...</p></div>
  <div class="card"><h3>Featured Creator(S)</h3><p>Coming soon...</p></div>
  <div class="card"><h3>Featured Discord Server(S)</h3><p>Coming soon...</p></div>
  <div class="card"><h3>S Tier Hero Classes</h3>
    <ul>
      <li>Poleaxe (Epic Set)</li>
      <li>Dualblade</li>
      <li>Nodachi</li>
      <li>Spear & Shield</li>
    </ul>
  </div>
  <div class="card"><h3>S Tier Unit(S)</h3>
    <ul>
      <li>Spartan Chosen</li>
      <li>Phallanx (after nerf)</li>
      <li>Yanyuedao Cav</li>
      <li>Lion Roar Crew (Team Unit)</li>
    </ul>
  </div>
</div>

  <h1>📘 CB-Wiki</h1>
  <div class="wrapper">
    <div class="content">
"""

    for folder in sorted([f for f in os.listdir() if f.lower() != "mechanics"]):
        if os.path.isdir(folder) and not folder.startswith("."):
            content += f"<h2>📂 {folder}</h2>\n"
            content += scan_directory(folder)

    # Melee Damage Formula – hinzugefügt
    content += """
<script>
  function cbCalculate() {
    const dmg = parseFloat(document.getElementById("weaponDamage").value);
    const pen = parseFloat(document.getElementById("penetration").value);
    const armor = parseFloat(document.getElementById("enemyArmor").value);
    const critMult = parseFloat(document.getElementById("critPercent").value) / 100;
    const mod = parseFloat(document.getElementById("modifier").value);

    const penRate = 1 - (armor / (pen + 1));
    const realPen = Math.max(penRate, 0.05);
    const raw = dmg * critMult * mod;
    const final = raw * realPen;

    document.getElementById("result").innerText = "Final Damage: " + final.toFixed(2);
  }
</script>

    <div class="info">
{create_sidebar_boxes()}
    </div>
  </div>
  <div class="footer">Created with ❤️ using GitHub Pages</div>
</div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Neue index.html erfolgreich erstellt mit Mechanics-Sektion.")

if __name__ == "__main__":
    generate_index_html()
