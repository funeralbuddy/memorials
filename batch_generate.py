import csv
import os
import shutil
from string import Template

TEMPLATE_FILE = "template.html"
OUTPUT_BASE = "memorials"
LOG_FILE = os.path.join(OUTPUT_BASE, "memorial_list.txt")

def generate_page(data):
    slug = data["name"].lower().replace(" ", "_")
    output_folder = os.path.join(OUTPUT_BASE, slug)
    os.makedirs(output_folder, exist_ok=True)

    # Copy photo
    photo_src = data["photo_filename"]
    photo_dst = os.path.join(output_folder, os.path.basename(photo_src))
    try:
        shutil.copy(photo_src, photo_dst)
        data["photo_filename"] = os.path.basename(photo_dst)
    except FileNotFoundError:
        print(f"⚠️ Warning: Photo not found: {photo_src}")
        data["photo_filename"] = ""  # Avoid broken link

    # Load template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = Template(f.read())
    html = template.safe_substitute(data)

    # Write page
    output_file = os.path.join(output_folder, "index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    # Append to log
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{data['name']}|{slug}\n")

    print(f"✅ Created memorial for: {data['name']}")

def generate_index_page():
    if not os.path.exists(LOG_FILE):
        return
    with open(LOG_FILE, "r", encoding="utf-8") as log:
        lines = [line.strip() for line in log if line.strip()]

    entries = []
    for line in lines:
        try:
            name, slug = line.split("|")
            entries.append(f'<li><a href="{slug}/">{name}</a></li>')
        except ValueError:
            continue

    html = f"""<html>
<head><title>Memorials</title></head>
<body>
<h1>Memorials</h1>
<ul>
{chr(10).join(entries)}
</ul>
</body>
</html>"""

    with open(os.path.join(OUTPUT_BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 Index updated with {len(entries)} entries.")

def main():
    with open("memorials.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            generate_page(row)

    generate_index_page()

if __name__ == "__main__":
    main()