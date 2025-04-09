from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import split_nodes_delimiter, split_nodes_image, split_nodes_link
from blocks_features import *
import unittest


class TestMarkdownToBlocks(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- Item 1
- Item 2
- Item 3

1. First
2. Second
3. Third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines</blockquote></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )

    def test_mixed_content(self):
        md = """
# Title

Paragraph with **bold** and _italic_.

- List item 1
- List item 2

> A quote here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Paragraph with <b>bold</b> and <i>italic</i>.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>A quote here</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
