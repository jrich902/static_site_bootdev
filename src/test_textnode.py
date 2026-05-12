import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_link_no_url(self):
        node = TextNode("Link Text", TextType.LINK, None)
        node2 = TextNode("Link Text", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()