import re
from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class markdownBlocks(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED = "Unordered_List"
    ORDERED = "Ordered_List"


def markdown_to_blocks(markdown):
    return [
        x for x in list(map(lambda x: x.strip(), re.split("\n{2,}", markdown))) if x
    ]


def block_to_block_type(block):
    if re.fullmatch(r"^#{1,6} [\w\W]*", block) is not None:
        return markdownBlocks.HEADING
    if re.fullmatch(r"^`{3}[\w\W]*`{3}$", block) is not None:
        return markdownBlocks.CODE

    split_block = block.split("\n")

    if all(re.fullmatch(r"^>{1}.*", x) is not None for x in split_block):
        return markdownBlocks.QUOTE

    if all(re.fullmatch(r"^-{1} .*", x) is not None for x in split_block):
        return markdownBlocks.UNORDERED

    count = 1

    for i in range(len(split_block)):
        if (
            (re.fullmatch(rf"^{count}\. .*", split_block[i]) is not None)
            and (count == i + 1)
            and i == len(split_block) - 1
        ):
            return markdownBlocks.ORDERED

        if (
            re.fullmatch(rf"^{count}\. .*", split_block[i]) is not None
        ) and count == i + 1:
            count += 1
        else:
            break

    return markdownBlocks.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []

    for block in blocks:
        a_block_type = block_to_block_type(block)
        parent_node = block_to_parent_node(a_block_type, block)
        parent_nodes.append(parent_node)

    return ParentNode("div", parent_nodes)


def strip_block_markers(text, block_type):
    new_text = ""
    match block_type:
        case markdownBlocks.PARAGRAPH:
            new_text = text.strip("\n").replace("\n", " ")
        case markdownBlocks.HEADING:
            new_text = (
                re.findall(r"^#{1,6} ([\w\W]*)", text)[0].strip("\n").replace("\n", " ")
            )
        case markdownBlocks.CODE:
            new_text = re.findall(r"^`{3}([\w\W]*)`{3}$", text)[0].lstrip("\n")
        case markdownBlocks.QUOTE:
            new_text_array = text.split("\n")
            stripped_text_array = list(map(lambda x: x.lstrip("> "), new_text_array))
            new_text = " ".join(stripped_text_array)
        case markdownBlocks.UNORDERED:
            new_text_array = text.split("\n")
            stripped_text_array = list(map(lambda x: x.lstrip("- "), new_text_array))
            new_text = "\n".join(stripped_text_array)
        case markdownBlocks.ORDERED:
            new_text_array = text.split("\n")
            stripped_text_array = []

            for line in new_text_array:
                stripped_text_array.append(re.findall(r"^\d\. (.*)", line)[0])
            new_text = "\n".join(stripped_text_array)

    return new_text


def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))


def determine_header(text):
    for i in range(6):
        if text[i + 1] == " ":
            return "h" + str(i + 1)
    return "h1"


def list_to_list_items(text):
    html_list = []
    for list_item in text.split("\n"):
        html_list.append(ParentNode("li", text_to_children(list_item)))
    return html_list


def block_to_parent_node(block_type, block_content):
    stripped_block_content = strip_block_markers(block_content, block_type)

    match block_type:
        case markdownBlocks.HEADING:
            return ParentNode(
                determine_header(block_content),
                text_to_children(stripped_block_content),
            )
        case markdownBlocks.CODE:
            return ParentNode(
                "pre",
                [
                    ParentNode(
                        "code",
                        [
                            text_node_to_html_node(
                                TextNode(stripped_block_content, TextType.NORMAL)
                            )
                        ],
                    ),
                ],
            )
        case markdownBlocks.QUOTE:
            return ParentNode("blockquote", text_to_children(stripped_block_content))

        case markdownBlocks.UNORDERED:
            return ParentNode("ul", list_to_list_items(stripped_block_content))

        case markdownBlocks.ORDERED:
            return ParentNode("ol", list_to_list_items(stripped_block_content))

        case markdownBlocks.PARAGRAPH:
            return ParentNode("p", text_to_children(stripped_block_content))

        case _:
            return None
