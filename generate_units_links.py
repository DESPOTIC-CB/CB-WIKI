import os
from urllib.parse import quote

def generate_full_units_html(base_path="Units"):
    html = "<h2>⚔️ Units</h2>\n"
    
    for folder in sorted(os.listdir(base_path)):
        subfolder_path = os.path.join(base_path, folder)
        if os.path.isdir(subfolder_path):
            html += f'<h3>📁 {folder}</h3>\n<ul>\n'
            for file in sorted(os.listdir(subfolder_path)):
                if file.endswith(".pdf"):
                    file_path = os.path.join(base_path, folder, file).replace('\\', '/')
                    display_name = file.replace(".pdf", "").replace("-", " ").replace("_", " ")
                    html += f'  <li><a href="{quote(file_path)}" target="_blank">{display_name}</a></li>\n'
            html += "</ul>\n"
    
    return html

# Ergebnis speichern
if __name__ == "__main__":
    html_code = generate_full_units_html("Units")
    with open("units_links_output.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("✅ HTML-Datei 'units_links_output.html' wurde erfolgreich erstellt.")
