from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_features import split_nodes_delimiter, split_nodes_image, split_nodes_link
import unittest


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_image(self):
        node = TextNode("This is just text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_no_link(self):
        node = TextNode("This is just text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_image_at_beginning(self):
        node = TextNode("![beginning](https://nike.com/logo.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("beginning", TextType.IMAGES, "https://nike.com/logo.jpg")],
        )

    def test_link_at_beginning(self):
        node = TextNode("[beginning](https://nike.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("beginning", TextType.LINK, "https://nike.com")],
        )

    def test_consecutive_images(self):
        node = TextNode("![one](one.jpg)![two](two.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.IMAGES, "one.jpg"),
                TextNode("two", TextType.IMAGES, "two.jpg"),
            ],
        )

    def test_consecutive_links(self):
        node = TextNode("[one](one.com)[two](two.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("one", TextType.LINK, "one.com"),
                TextNode("two", TextType.LINK, "two.com"),
            ],
        )

    def test_empty_images(self):
        node = TextNode("![]()", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [])

    def test_empty_links(self):
        node = TextNode("[]()", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [])


if __name__ == "__main__":
    unittest.main()
