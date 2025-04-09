import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_is_none_on_default(self):
        node = TextNode(
            "Here's a text node with url value set to None", TextType.NORMAL, None
        )
        node2 = TextNode(
            "Here's a text node with url value set to None", TextType.NORMAL
        )
        self.assertEqual(node, node2)

    def test_textnode_is_different_on_properties_1(self):
        node = TextNode("This is a cool node", TextType.BOLD)
        node2 = TextNode("This is also a cool node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_textnode_is_different_on_properties_2(self):
        node = TextNode("This is a cool node", TextType.BOLD)
        node2 = TextNode("This is a cool node", TextType.NORMAL)
        self.assertNotEqual


if __name__ == "__main__":
    unittest.main()
