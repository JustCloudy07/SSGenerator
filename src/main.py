from copy_static import Copy_Static, generate_page, generate_pages_recursive
from pathlib import Path


def main():
    Copy_Static()
    generate_pages_recursive("content", "template.html", "docs")


main()
