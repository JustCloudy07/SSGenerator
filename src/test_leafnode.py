import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "Hello, world!")
        self.assertEqual(node.to_html(), "<code>Hello, world!</code>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://google.com">Hello, world!</a>'
        )

    def test_leaf_to_html_img(self):
        node = LeafNode(
            "img", "", {"src": "https://google.com", "alt": "Just Google Man"}
        )
        self.assertEqual(
            node.to_html(), '<img src="https://google.com" alt="Just Google Man" />'
        )

    def test_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), "Some text")

    def test_no_values(self):
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
