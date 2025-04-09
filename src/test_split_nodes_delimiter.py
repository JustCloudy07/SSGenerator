from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import split_nodes_delimiter
import unittest


class TestSplitNodes(unittest.TestCase):
    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_split_node_italics(self):
        node = TextNode("This is text with a _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_split_node_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_split_node_normal(self):
        node = TextNode("This is just normal text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.NORMAL)
        self.assertEqual(new_nodes, [node])

    def test_invalid_texttype(self):
        node = TextNode("This is just normal text", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", "something")

    def test_multiple_delimiters(self):
        node = TextNode(
            "This is text with a **bold** word and a _italic_ word", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        final_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            final_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_consecutive_delimiters(self):
        node = TextNode("This is a ****bold**** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.NORMAL),
                TextNode("bold", TextType.NORMAL),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_consecutive_delimiters_two(self):
        node = TextNode("This is text with a ___italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
        )

    def test_connecting_delimiters(self):
        node = TextNode("A **bold**_italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        final_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            final_nodes,
            [
                TextNode("A ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.NORMAL),
            ],
        )

    def test_delimiter_at_beginning_and_end(self):
        node = TextNode("**This entire text is bold**", TextType.NORMAL)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, [TextNode("This entire text is bold", TextType.BOLD)]
        )


if __name__ == "__main__":
    unittest.main()
