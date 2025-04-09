import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is an example of a paragraph", None, None)
        self.assertEqual(
            str(node), "HTMLNode(p, This is an example of a paragraph, None, None)"
        )

    def test_eq2(self):
        node = HTMLNode(
            "a",
            "This a link node",
            [HTMLNode("p", "Example node", None, None)],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            str(node),
            "HTMLNode(a, This a link node, [HTMLNode(p, Example node, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "This a link node",
            [HTMLNode("p", "Example node", None, None)],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_None(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")

    def test_empty_props(self):
        node = HTMLNode("p", "This is an example of a paragraph", None, {})
        self.assertEqual(
            str(node), "HTMLNode(p, This is an example of a paragraph, None, {})"
        )


if __name__ == "__main__":
    unittest.main()
