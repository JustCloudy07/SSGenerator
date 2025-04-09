from contextlib import AbstractAsyncContextManager
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import split_nodes_delimiter, split_nodes_image, split_nodes_link
from blocks_features import markdown_to_blocks, block_to_block_type, markdownBlocks
import unittest


class TestMarkdownToBlocks(unittest.TestCase):
    def test_heading(self):
        assert block_to_block_type("# Heading 1") == markdownBlocks.HEADING
        assert block_to_block_type("## Heading 2") == markdownBlocks.HEADING
        assert block_to_block_type("###### Heading 6") == markdownBlocks.HEADING
        # Edge cases
        assert (
            block_to_block_type("####### Not a valid heading")
            == markdownBlocks.PARAGRAPH
        )
        assert (
            block_to_block_type("#Not a heading without space")
            == markdownBlocks.PARAGRAPH
        )
        assert (
            block_to_block_type("## Heading\nWith a newline") == markdownBlocks.HEADING
        )

    def test_code_block(self):
        assert block_to_block_type("```\ncode here\n```") == markdownBlocks.CODE
        assert (
            block_to_block_type("```python\ndef hello():\n    print('world')\n```")
            == markdownBlocks.CODE
        )
        assert (
            block_to_block_type("`````This should work```````") == markdownBlocks.CODE
        )
        # Edge cases
        assert (
            block_to_block_type("``\nNot enough backticks\n``")
            == markdownBlocks.PARAGRAPH
        )
        assert (
            block_to_block_type("```\nIncomplete code block")
            == markdownBlocks.PARAGRAPH
        )

    def test_quote_block(self):
        assert block_to_block_type("> This is a quote") == markdownBlocks.QUOTE
        assert block_to_block_type("> Line 1\n> Line 2") == markdownBlocks.QUOTE
        assert (
            block_to_block_type(">This is not a quote without space")
            == markdownBlocks.QUOTE
        )
        # Edge case
        assert (
            block_to_block_type("Some text\n> Mixed content")
            == markdownBlocks.PARAGRAPH
        )

    def test_unordered_list(self):
        assert block_to_block_type("- Item 1") == markdownBlocks.UNORDERED
        assert block_to_block_type("- Item 1\n- Item 2") == markdownBlocks.UNORDERED
        # Edge case
        assert block_to_block_type("-Item 1") == markdownBlocks.PARAGRAPH

    def test_ordered_list(self):
        assert block_to_block_type("1. Item 1") == markdownBlocks.ORDERED
        assert block_to_block_type("1. Item 1\n2. Item 2") == markdownBlocks.ORDERED
        assert block_to_block_type("1. Item 1\n3. Item 3") == markdownBlocks.PARAGRAPH
        assert block_to_block_type("1.Item 1") == markdownBlocks.PARAGRAPH

    def test_mixed_block_types(self):
        assert (
            block_to_block_type(
                "> This starts like a quote\n- But ends like an unordered list"
            )
            == markdownBlocks.PARAGRAPH
        )
        assert (
            block_to_block_type(
                "# This looks like a heading\n> But continues as a quote"
            )
            == markdownBlocks.HEADING
        )

        assert (
            block_to_block_type("1. First item\n2. Second item\n- Suddenly unordered")
            == markdownBlocks.PARAGRAPH
        )
        
        assert block_to_block_type("> First quote line\nThis isn't a quote line\n> Back to normal.") == markdownBlocks.PARAGRAPH

if __name__ == "__main__":
    unittest.main()
