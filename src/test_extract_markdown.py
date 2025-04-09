from inline_features import (
    extract_markdown_images,
    extract_markdown_links,
)
import unittest


class TestSplitNodes(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.com)"
        )
        self.assertListEqual(matches, [("link", "https://google.com")])

    def test_improper_method_links(self):
        matches = extract_markdown_links(
            "This is text with ![something](https://youtube.com)"
        )
        self.assertListEqual([], matches)

    def test_improper_method_images(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://google.com)"
        )
        self.assertListEqual(matches, [])

    def test_no_string(self):
        matches = extract_markdown_images("")
        matches_two = extract_markdown_links("")
        self.assertEqual(matches, matches_two)

    def test_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "Here's one image ![image](https://image.com) and here's another WOW! ![another image](https://coolerimage.com)"
        )
        self.assertListEqual(
            matches,
            [
                ("image", "https://image.com"),
                ("another image", "https://coolerimage.com"),
            ],
        )

    def test_mixed_images_and_links(self):
        matches = extract_markdown_images(
            "Check out ![this image](pic.jpg) and [this site](site.com)! Also, ![another one](caf.jpg)"
        )
        self.assertListEqual(
            matches, [("this image", "pic.jpg"), ("another one", "caf.jpg")]
        )


if __name__ == "__main__":
    unittest.main()
