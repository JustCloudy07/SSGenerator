from pathlib import Path
import os
import shutil
import re

from blocks_features import markdown_to_html_node


def Copy_Static(
    parent_directory=Path(__file__).parent.parent / "static",
    destination_path=Path(__file__).parent.parent / "docs",
    isClean=False,
):
    if (os.path.exists(Path(__file__).parent.parent / "docs")) and isClean == False:
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)
        isClean = True
    if isClean == True:
        for item in os.listdir(parent_directory):
            if os.path.isfile(parent_directory / item):
                shutil.copy((parent_directory / item), destination_path)
                print("Copying file...")
                print(f"File {item} is now in {destination_path}")
            else:
                os.mkdir(destination_path / item)
                Copy_Static(parent_directory / item, destination_path / item, isClean)
                print("Copying directory")
                print(f"Directory {item} is now in {destination_path}")


def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip(" ")
        if re.fullmatch(r"^# (.*)$", line) is not None:
            return re.findall(r"^# (.*)$", line)[0].strip(" ")
    raise Exception("Title not found")


def generate_page(from_path, template_path, dest_path, base):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(Path(__file__).parent.parent / from_path) as f:
        markdown_content = f.read()
        f.close()
    with open(Path(__file__).parent.parent / template_path) as f:
        template_content = f.read()
        f.close()
    html_string = markdown_to_html_node(markdown_content)
    page_title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", html_string.to_html())
    template_content = template_content.replace('href="/', f'href="{base}')
    template_content = template_content.replace('src="/', f'src="{base}')
    if (
        os.path.exists(Path(__file__).parent.parent / os.path.dirname(dest_path))
        == False
    ):
        os.makedirs(Path(__file__).parent.parent / os.path.dirname(dest_path))
    stripped_md = dest_path.rstrip(".md") + ".html"
    with open(Path(__file__).parent.parent / stripped_md, "w") as f:
        f.write(template_content)
        f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base):
    for item in os.listdir(Path(__file__).parent.parent / dir_path_content):
        if os.path.isfile(Path(__file__).parent.parent / dir_path_content / item):
            generate_page(
                f"{dir_path_content}/{item}",
                template_path,
                f"{dest_dir_path}/{item}",
                base,
            )
        else:
            generate_pages_recursive(
                f"{dir_path_content}/{item}",
                template_path,
                f"{dest_dir_path}/{item}",
                base,
            )
