import os
import shutil
import sys
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
    
def generate_page(from_path, template_path, dest_path, basepath):
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
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as output_file:
        output_file.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path, basepath)

        elif os.path.isfile(source_path):
            if not source_path.endswith(".md"):
                continue

            dest_path = dest_path[:-3] + ".html"
            generate_page(source_path, template_path, dest_path, basepath)
            
def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    source_dir = "static"
    dest_dir = "public"
    content_dir = "content"
    template_path = "template.html"
    copy_static_to_public(source_dir, dest_dir)
    generate_pages_recursive(content_dir, template_path, "docs", basepath)
    
    
    
if __name__ == '__main__':
    main()
