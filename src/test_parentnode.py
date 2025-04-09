import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_multiple_grandchildren_and_children(self):
        grandchild_one = LeafNode("b", "Bold text")
        grandchild_one_two = LeafNode("i", "italic text")
        child_one = ParentNode("span", [grandchild_one, grandchild_one_two])
        grandchild_two = LeafNode("p", "paragraph text")
        grandchild_two_two = LeafNode("code", "code text")
        child_two = ParentNode("div", [grandchild_two, grandchild_two_two])
        parent_node = ParentNode("div", [child_one, child_two])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>Bold text</b><i>italic text</i></span><div><p>paragraph text</p><code>code text</code></div></div>",
        )

    def test_to_html_no_tag(self):
        node = ParentNode(None, LeafNode("p", "Some text"))
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_child_exception(self):
        node = ParentNode("div", [LeafNode(None, None)])
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
