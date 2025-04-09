from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
import unittest


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [])

    def test_only_link(self):
        text = "[cool](www.microsoft.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes, [TextNode("cool", TextType.LINK, "www.microsoft.com")]
        )


if __name__ == "__main__":
    unittest.main()
