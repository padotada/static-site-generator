import os
import shutil
from textnode import *
from inline_markdown import *
from block_markdown import *


def copy_static_to_public(source: str, dest: str)->None:
    source_dir = None
    dest_dir = None
    if not os.path.exists(source):
        raise FileNotFoundError("Source file is invalid")
    
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_dir_contents(source, dest)
    
def copy_dir_contents(source, dest):
    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)

        elif os.path.isdir(source_path):
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)

            copy_dir_contents(source_path, dest_path)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()
        
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as output_file:
        output_file.write(full_html)

def main():
    source_dir = "static"
    dest_dir = "public"
    copy_static_to_public(source_dir, dest_dir)
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    
    
    
if __name__ == '__main__':
    main()
