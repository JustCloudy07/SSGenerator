from copy_static import Copy_Static, generate_page, generate_pages_recursive
from pathlib import Path
import sys


def main():
    if sys.argv[0] != None:
        basepath = sys.argv[0]
    else:
        basepath = "/"
    Copy_Static()
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
