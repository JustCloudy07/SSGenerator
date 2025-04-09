from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type == TextType.NORMAL:
        return old_nodes
    if text_type not in TextType:
        raise ValueError(
            f"Invalid text type: {text_type}. Must be a member of TextType."
        )
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            split_nodes.append(old_node)
            continue
        if len(old_node.text.split(delimiter)) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        split_old_node_text = old_node.text.split(delimiter)
        text_node_list = []
        for i in range(len(split_old_node_text)):
            if split_old_node_text[i] == "":
                continue
            if i % 2 == 0:
                text_node_list.append(TextNode(split_old_node_text[i], TextType.NORMAL))
            else:
                text_node_list.append(TextNode(split_old_node_text[i], text_type))
        split_nodes.extend(text_node_list)
    return split_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\[\]]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\[\]]*)\)", text)


def split_nodes_image(old_nodes):
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            split_nodes.append(old_node)
            continue

        split_text = re.split(r"!\[([^\[\]]*)\]\(([^\[\]]*)\)", old_node.text)
        counter = 0
        split_text_list = []
        for i in range(len(split_text)):
            if split_text[i] == "":
                counter += 1
                continue
            match counter:
                case 0:
                    split_text_list.append(TextNode(split_text[i], TextType.NORMAL))
                    counter += 1
                case 1:
                    split_text_list.append(
                        TextNode(split_text[i], TextType.IMAGES, split_text[i + 1])
                    )
                    counter += 1
                case 2:
                    counter = 0
                    continue
                case _:
                    break
        split_nodes.extend(split_text_list)
    return split_nodes


def split_nodes_link(old_nodes):
    split_nodes = []
    for old_node in old_nodes:
        if len(extract_markdown_links(old_node.text)) == 0:
            split_nodes.append(old_node)
            continue
        split_text = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\[\]]*)\)", old_node.text)
        counter = 0
        split_text_list = []
        for i in range(len(split_text)):
            if split_text[i] == "":
                counter += 1
                continue
            match counter:
                case 0:
                    split_text_list.append(TextNode(split_text[i], TextType.NORMAL))
                    counter += 1
                case 1:
                    split_text_list.append(
                        TextNode(split_text[i], TextType.LINK, split_text[i + 1])
                    )
                    counter += 1
                case 2:
                    counter = 0
                    continue
                case _:
                    break
        split_nodes.extend(split_text_list)
    return split_nodes


def text_to_textnodes(text):
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_image(split_nodes_link([TextNode(text, TextType.NORMAL)])),
                "`",
                TextType.CODE,
            ),
            "**",
            TextType.BOLD,
        ),
        "_",
        TextType.ITALIC,
    )
