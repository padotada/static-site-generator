from textnode import TextNode, TextType
import os
import shutil

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
    
def main():
    # tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(tn)
    source_dir = "static"
    dest_dir = "public"
    copy_static_to_public(source_dir, dest_dir)
    
if __name__ == '__main__':
    main()
