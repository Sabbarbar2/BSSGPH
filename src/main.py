import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # print("Generating page...")
    # generate_page(
    #     os.path.join(dir_path_content, "index.md"),
    #     template_path,
    #     os.path.join(dir_path_public, "index.html"),
    # )

    print("Generating pages recursively...")
    generate_pages_recursive(
    dir_path_content="content",
    template_path="template.html",
    dest_dir_path="public"
    )

main()


def process_csv_recursive(src_dir, dest_dir):
    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)
        if os.path.isfile(src_path) and entry.endswith('.csv'):
            # Imagine we "copy and rename" the file here
            new_dest_path = dest_path[:-4] + '.data'  # change extension to .data
            print(f"Would process: {src_path} -> {new_dest_path}")
        elif os.path.isdir(src_path):
            # Ensure the output directory exists
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            process_csv_recursive(src_path, dest_path)