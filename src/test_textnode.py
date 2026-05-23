import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.LINK, "https://test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href" : "https://test.com"})
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://test.com/test.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, { "src" : "https://test.com/test.jpg", "alt" : "This is a text node"})

    def test_split_one_italic(self):
        node = TextNode("This is _XXX_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("XXX", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])
    def test_split_one_bold(self):
        node = TextNode("This is **XXX** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("XXX", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])
    def test_split_one_bold(self):
        node = TextNode("This is `XXX` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("XXX", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_split_two(self):
        node = TextNode("This is **bold** text and **more bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ])

    def test_split_fail(self):
        node = TextNode("This is **bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_fail(self):
        node = TextNode("this wont work", TextType.IMAGE)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("this wont work", TextType.IMAGE),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([
            ('to boot dev', 'https://www.boot.dev'), 
            ('to youtube', 'https://www.youtube.com/@bootdotdev'),
            ], 
            matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://text.com/text1) and another [second link](https://text.com/text2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://text.com/text1"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://text.com/text2"),
            ],
            new_nodes,
        )         

    def test_everything_at_once(self):
        test_string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(test_string)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )




    if __name__ == "__main__":
        unittest.main()

