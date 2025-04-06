
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
            html += f'  <details open>\n    <summary>📁 {section_title}</summary>\n    <ul>\n'
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
    mechanics_html = """
<h2>📂 Mechanics</h2>

<details>
  <summary style="color: #ffe600;">⚔️ Melee Damage Formula (Click to Expand)</summary>
  <div style="margin-top: 10px; padding: 10px; background-color: #1e1e1e; border-radius: 10px;">
    <table style="width: 100%; background-color: #1e1e1e; color: #e0e0e0; border-collapse: collapse; font-family: sans-serif;">
      <thead>
        <tr style="background-color: #2a2a2a; color: gold;">
          <th style="padding: 10px; border: 1px solid #333;">Component</th>
          <th style="padding: 10px; border: 1px solid #333;">Formula</th>
          <th style="padding: 10px; border: 1px solid #333;">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 10px; border: 1px solid #333;">Penetration Rate</td>
          <td style="padding: 10px; border: 1px solid #333;">
            max(1 - Armor / (Weapon AP × (Skill AP Coeff + Speed Coeff) + Extra Skill AP), 0.05)
          </td>
          <td style="padding: 10px; border: 1px solid #333;">
            Damage reduced by armor. Minimum 5% penetration guaranteed.<br>
            <strong>Note:</strong> If Skill AP Coeff = 0 → No damage dealt
          </td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #333;">Raw Damage</td>
          <td style="padding: 10px; border: 1px solid #333;">
            Weapon Damage × (1 + Weapon Buff)<br>
            × Skill Damage Coeff<br>
            × (1 + Crit Coeff + (Headshot OR Backattack))<br>
            + Speed Coeff + Skill Buff Coeff + Extra Skill Damage
          </td>
          <td style="padding: 10px; border: 1px solid #333;">
            Complete calculation before armor. Includes buffs, crits, position bonuses.<br>
            <strong>Note:</strong> If Skill Damage Coeff = 0 → No damage
          </td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #333;">Final Damage</td>
          <td style="padding: 10px; border: 1px solid #333;">
            Raw Damage × Penetration Rate
          </td>
          <td style="padding: 10px; border: 1px solid #333;">
            Resulting effective damage after armor mitigation.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</details>

<details>
  <summary style="color: #ffe600;">🧮 Melee Damage Calculator (Click to Expand)</summary>
  <div style="margin-top: 10px; padding: 10px; background-color: #1e1e1e; border-radius: 10px; color: #e0e0e0;">
    <form id="calcForm">
      <label>Armor: <input type="number" id="armor" value="200" /></label><br><br>
      <label>Weapon AP: <input type="number" id="weaponAp" value="250" /></label><br><br>
      <label>Skill AP Coeff: <input type="number" step="0.1" id="skillApCoeff" value="0.6" /></label><br><br>
      <label>Speed Coeff: <input type="number" step="0.1" id="speedCoeff" value="0.2" /></label><br><br>
      <label>Extra Skill AP: <input type="number" id="extraSkillAp" value="0" /></label><br><br>
      <label>Weapon Damage: <input type="number" id="weaponDmg" value="1000" /></label><br><br>
      <label>Weapon Buff (%): <input type="number" id="weaponBuff" value="0.2" /></label><br><br>
      <label>Skill Dmg Coeff: <input type="number" step="0.1" id="skillDmgCoeff" value="1.5" /></label><br><br>
      <label>Crit Coeff: <input type="number" id="critCoeff" value="0.5" /></label><br><br>
      <label>Positional Bonus: <input type="number" id="positional" value="0.2" /></label><br><br>
      <label>Extra Dmg (Speed + Buffs): <input type="number" id="extraDmg" value="100" /></label><br><br>
      <button type="button" onclick="calculateDamage()">Calculate</button>
    </form>
    <p id="result" style="margin-top: 1rem; font-weight: bold; color: gold;"></p>
    <script>
      function calculateDamage() {
        const armor = parseFloat(document.getElementById("armor").value);
        const weaponAp = parseFloat(document.getElementById("weaponAp").value);
        const skillApCoeff = parseFloat(document.getElementById("skillApCoeff").value);
        const speedCoeff = parseFloat(document.getElementById("speedCoeff").value);
        const extraSkillAp = parseFloat(document.getElementById("extraSkillAp").value);
        const weaponDmg = parseFloat(document.getElementById("weaponDmg").value);
        const weaponBuff = parseFloat(document.getElementById("weaponBuff").value);
        const skillDmgCoeff = parseFloat(document.getElementById("skillDmgCoeff").value);
        const critCoeff = parseFloat(document.getElementById("critCoeff").value);
        const positional = parseFloat(document.getElementById("positional").value);
        const extraDmg = parseFloat(document.getElementById("extraDmg").value);
        const denominator = weaponAp * (skillApCoeff + speedCoeff) + extraSkillAp;
        const penetrationRate = Math.max(1 - (armor / denominator), 0.05);
        const rawDmg = weaponDmg * (1 + weaponBuff) * skillDmgCoeff * (1 + critCoeff + positional) + extraDmg;
        const finalDmg = rawDmg * penetrationRate;
        document.getElementById("result").innerText = "Final Damage: " + finalDmg.toFixed(2);
      }
    </script>
  </div>
</details>
"""

    content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>CB-Wiki</title>
  <style>
    body {{ margin: 0; background-color: #2b2b2b; font-family: Arial, sans-serif; color: #f1f1f1; line-height: 1.6; }}
    .wrapper {{ display: flex; justify-content: center; align-items: flex-start; padding: 2rem; gap: 2rem; }}
    .content {{ flex: 2; max-width: 800px; }}
    .info {{ width: 300px; display: flex; flex-direction: column; gap: 1rem; }}
    .box {{ background-color: #333; border: 2px solid #ffe600; border-radius: 8px; padding: 1rem; box-shadow: 0 0 10px #111; }}
    .box h3 {{ color: #ffe600; margin-top: 0; }}
    .box ul {{ list-style-type: none; padding-left: 0; }}
    .box li {{ margin: 0.3rem 0; }}
    h1 {{ text-align: center; font-size: 2.5rem; margin-bottom: 1rem; color: #ffe600; }}
    details {{ background-color: #444; border-radius: 5px; margin: 1rem 0; padding: 0.5rem 1rem; }}
    summary {{ font-size: 1.1rem; font-weight: bold; cursor: pointer; }}
    ul {{ list-style-type: none; padding-left: 1rem; }}
    li {{ margin: 0.3rem 0; }}
    a {{ color: #66ccff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .footer {{ margin-top: 3rem; font-size: 0.85rem; text-align: center; color: #999; }}
  </style>
</head>
<body>
  <h1>📘 CB-Wiki</h1>
  <div class="wrapper">
    <div class="content">
"""

    for folder in sorted(os.listdir()):
        if os.path.isdir(folder) and not folder.startswith("."):
            content += f"<h2>📂 {folder}</h2>
"
            content += scan_directory(folder)

    content += mechanics_html
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
    print("✅ Neue index.html mit Formel und Calculator erfolgreich erstellt.")

if __name__ == "__main__":
    generate_index_html()
