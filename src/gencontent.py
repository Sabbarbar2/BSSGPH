import os
import shutil
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages from Markdown files while:
    - Preserving directory structure
    - Keeping non-Markdown files intact
    - Creating clean URLs (e.g., /blog/glorfindel/)
    """
    os.makedirs(dest_dir_path, exist_ok=True)

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if not file.endswith('.md'):
                continue  

            
            rel_path = os.path.relpath(os.path.join(root, file), dir_path_content)
            
            
            if file == 'index.md':
                dest_path = os.path.join(dest_dir_path, os.path.dirname(rel_path), 'index.html')
            else:
                file_base = os.path.splitext(file)[0]
                dest_path = os.path.join(dest_dir_path, os.path.dirname(rel_path), file_base, 'index.html')
            
           
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
           
            if os.path.exists(dest_path):
                os.remove(dest_path)
            
           
            generate_page(
                os.path.join(root, file),
                template_path,
                dest_path
            )

    for static_file in ['index.css', 'favicon.ico']: 
        src = os.path.join(os.path.dirname(dir_path_content), static_file)
        dst = os.path.join(dest_dir_path, static_file)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            
            

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
