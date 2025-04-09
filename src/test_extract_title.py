from copy_static import extract_title
import unittest


class Test_title_extraction(unittest.TestCase):
    def test_basic_title(self):
        assert extract_title("# Hello World") == "Hello World"

    def test_title_with_spaces(self):
        assert extract_title("#    Spaced Title    ") == "Spaced Title"

    def test_title_in_content(self):
        content = """Some text here
# The Real Title
        More text here"""
        assert extract_title(content) == "The Real Title"

    def test_no_title(self):
        import pytest

        with pytest.raises(Exception):
            extract_title("Just some text without a heading")

    def test_multiple_headings(self):
        content = """# First Heading
        ## Second heading
        # Another H1 Heading"""
        assert extract_title(content) == "First Heading"

    def test_different_heading_levels(self):
        content = """## Not an H1
        ### Also not an H1
        # This is the H1"""
        assert extract_title(content) == "This is the H1"


if __name__ == "__main__":
    unittest.main()
