from textnode import *
import shutil
import os
from markdown_blocks import markdown_to_html_node


def clean_up_public():
    path = "public"
    if os.path.exists(path):
        print(f"deleting {path}")
        shutil.rmtree(path)
        print(f"creating new empty {path}")
        os.mkdir(path)

def copy_from_static():
    src = "static"
    dst = "public"
    clean_up_public()
    recursive_copy(src, dst)

def recursive_copy(src, dst):
    if not os.path.exists(dst):
        print(f"creating folder {dst}")
        os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path}")

        elif os.path.isdir(src_path):
            recursive_copy(src_path, dst_path)

def extract_title(markdown):
    with open(markdown, "r") as file:
        for line in file:
            if line.startswith("#"):
               return line.strip("# ")
    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        from_file_content = file.read()

    with open(template_path, "r") as file:
        template_path_content = file.read()

    title = extract_title(from_path)
    print(f"Extraced title: {title}")

    page_content = markdown_to_html_node(from_file_content)
    page_html = page_content.to_html()
    page = template_path_content.replace("{{ Title }}", title)
    
    print(f"page_content:\n{page_html}")
    page = page.replace("{{ Content }}", page_html)
   
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(page)

def find_markdown(path):
    path_list = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        if os.path.isfile(full_path):

            if full_path.endswith(".md"):
                path_list.append(full_path)
        
        elif os.path.isdir(full_path):
            sub_path = find_markdown(full_path)

            path_list.extend(sub_path)
  
    
    return path_list

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # okay so we got the files to work on in a list with find markdown.
    content_files = find_markdown(dir_path_content)
    for item in content_files:
        #this is for debugging, it shows the path.
        print(f"Processing: {item}")
        #this strips the .md off and appends .html
        dst_file = f"{item[:-3]}.html"
        #this update path to be public/.../file.html
        dst_file = dst_file.replace(dir_path_content, dest_dir_path)
        generate_page(item, template_path, dst_file)
        print(f"generated page: {dst_file}")

def main():
    copy_from_static()
    generate_pages_recursive("content", "template.html", "public")

main()
