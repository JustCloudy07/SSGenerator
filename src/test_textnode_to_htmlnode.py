import unittest

import htmlnode
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from leafnode import LeafNode


class Test_TextNode_to_HTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://nike.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://nike.com"})
        self.assertEqual(
            html_node.to_html(), '<a href="https://nike.com">This is a text node</a>'
        )

    def test_image(self):
        node = TextNode(
            "This is a text node", TextType.IMAGES, "https://nike.com/bruh.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://nike.com/bruh.jpg", "alt": "This is a text node"},
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://nike.com/bruh.jpg" alt="This is a text node" />',
        )

    def test_no_texttype(self):
        node = TextNode("This is a text node", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node((node))

    def test_no_value(self):
        node = TextNode(None, TextType.BOLD)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_empty_string(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")

    def test_link_with_special_chars(self):
        url = "https://example.com/search?q=test&page=1"
        text = "Search Results"
        node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Search Results")
        self.assertEqual(html_node.props["href"], url)

    def test_textnode_with_unicode_characters(self):
        node = TextNode("😜😜😜😜😜😜LMAOOOOO😜😜😜😜", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "😜😜😜😜😜😜LMAOOOOO😜😜😜😜")

    def test_special_text_values(self):
        node = TextNode("<b>Whateva</b>", TextType.NORMAL)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, "&lt;b&gt;Whateva&lt;/b&gt;")


if __name__ == "__main__":
    unittest.main()
