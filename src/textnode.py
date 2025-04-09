from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGES = "images"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text_node_to_html_node(textnode):
    if textnode.text is None:
        raise ValueError("No values for textnode available")
    textnode.text = escape_html(textnode.text)
    match textnode.text_type:
        case TextType.NORMAL:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode(
                "a",
                textnode.text,
                {
                    "href": textnode.url,
                },
            )
        case TextType.IMAGES:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
        case _:
            raise ValueError("Invalid text type.")
