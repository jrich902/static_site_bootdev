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

    def test_to_html_with_children_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "greeting", "id": "main"})
        self.assertEqual(
            parent_node.to_html(), 
            '<div class="greeting" id="main"><span>child</span></div>',
            )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child</span></div>",
            )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
