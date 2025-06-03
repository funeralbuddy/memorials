import os
import shutil
from string import Template

def ask(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter something.")

# Load the HTML template
with open("template.html", "r", encoding="utf-8") as f:
    template_content = f.read()

# Collect data from user
data = {
    "name": ask("Full name of the person: "),
    "birth_year": ask("Year of birth: "),
    "death_year": ask("Year of passing: "),
    "photo_filename": ask("Photo filename (e.g. meiling.jpg): "),
    "biography": ask("Short biography: "),
    "condolence1": ask("Condolence message 1: "),
    "condolence2": ask("Condolence message 2: "),
    "quote": ask("Memorial quote: ")
}

# Generate safe filename (e.g. tan_mei_ling)
slug = data["name"].lower().replace(" ", "_")
output_folder = os.path.join("memorials", slug)
os.makedirs(output_folder, exist_ok=True)

# Copy the photo to the output folder
photo_src = data["photo_filename"]
if not photo_src.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
    print("⚠️ Warning: File does not appear to be an image.")
photo_dst = os.path.join(output_folder, os.path.basename(photo_src))
try:
    shutil.copy(photo_src, photo_dst)
    print(f"Copied photo to: {photo_dst}")
except FileNotFoundError:
    print(f"⚠️ Warning: Photo file not found: {photo_src}. You may need to copy it manually.")

# Update the photo filename to match the new path
data["photo_filename"] = os.path.basename(photo_dst)

# If the user leaves condolence messages blank, supply defaults
if not data["condolence1"]:
    data["condolence1"] = "Our deepest condolences to the family."

# Fill in the template
html = Template(template_content).safe_substitute(data)

# Write the HTML file into the output folder
output_file = os.path.join(output_folder, "index.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Memorial page created: {output_file}")

# Ensure memorials folder exists
os.makedirs("memorials", exist_ok=True)

# Track this entry in a central log file
log_path = os.path.join("memorials", "memorial_list.txt")
with open(log_path, "a", encoding="utf-8") as log:
    log.write(f"{data['name']}|{slug}\n")

def generate_index_page():
    log_path = os.path.join("memorials", "memorial_list.txt")
    index_path = os.path.join("memorials", "index.html")
    if not os.path.exists(log_path):
        print("No memorials yet, skipping index generation.")
        return

    with open(log_path, "r", encoding="utf-8") as log:
        lines = [line.strip() for line in log if line.strip()]

    entries = []
    for line in lines:
        try:
            name, slug = line.split("|")
            entries.append(f'<li><a href="{slug}/">{name}</a></li>')
        except ValueError:
            continue  # skip malformed lines

    html = f"""<html>
<head><title>Memorials</title></head>
<body>
<h1>Memorials</h1>
<ul>
{chr(10).join(entries)}
</ul>
</body>
</html>"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🗂 Index page updated: {index_path}")

generate_index_page()
