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
        print(node.props_to_html)
        node2 = HTMLNode("p", "hello", None, {"class": "greeting"})
        result2 = node2.props_to_html()
        self.assertEqual(result, result2)
        
    def test_two_prop(self):
        node = HTMLNode("p", "hello", None, {"class": "greeting", "id": "main"})
        result = node.props_to_html()
        print(node.props_to_html)
        node2 = HTMLNode("p", "hello", None, {"class": "greeting", "id": "main"})
        result2 = node2.props_to_html()
        self.assertEqual(result, result2)

if __name__ == "__main__":
    unittest.main()