import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_no_prop(self):
        node = HTMLNode("p", "hello", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_one_prop(self):
        node = HTMLNode("p", "hello", None, {"class": "greeting"})
        result = node.props_to_html()
        node2 = HTMLNode("p", "hello", None, {"class": "greeting"})
        result2 = node2.props_to_html()
        self.assertEqual(result, result2)

    def test_two_props(self):
        node = HTMLNode("p", "hello", None, {"class": "greeting", "id": "main"})
        result = node.props_to_html()
        node2 = HTMLNode("p", "hello", None, {"class": "greeting", "id": "main"})
        result2 = node2.props_to_html()
        self.assertEqual(result, result2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_two_props(self):
        node = LeafNode("p", "hello", {"class": "greeting", "id": "main"})
        self.assertEqual(node.to_html(), '<p class="greeting" id="main">hello</p>')

if __name__ == "__main__":
    unittest.main()