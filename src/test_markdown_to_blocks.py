from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import split_nodes_delimiter, split_nodes_image, split_nodes_link
from blocks_features import markdown_to_blocks
import unittest


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        block = markdown_to_blocks(md)
        self.assertEqual(
            block,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_consecutive_newlines(self):
        md = """
A paragraph.


Another paragraph.
    """
        block = markdown_to_blocks(md)
        self.assertEqual(block, ["A paragraph.", "Another paragraph."])

    def test_leading_and_trailing_newlines(self):
        md = """


Content with newlines.


        """
        block = markdown_to_blocks(md)
        self.assertEqual(block, ["Content with newlines."])

    def test_one_block(self):
        md = """
Just one block
        """
        block = markdown_to_blocks(md)
        self.assertEqual(block, ["Just one block"])

    def test_empty_string(self):
        md = ""
        block = markdown_to_blocks(md)
        self.assertEqual(block, [])

    def test_whitespace_blocks(self):
        md = """
Valid content.

    

More content.
        """
        block = markdown_to_blocks(md)
        self.assertEqual(block, ["Valid content.", "More content."])


if __name__ == "__main__":
    unittest.main()
