import unittest
from markdown_blocks import block_to_block_type, BlockType, markdown_to_blocks, markdown_to_html_node
class TestBlockNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # test heading detection
    def test_heading_block(self):
        markdown = "# This is a heading"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.HEADING)

    # test quote block detection
    def test_quote_block(self):
        markdown = "> this is a quote\n> second line"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.QUOTE)

    # test code block detection
    def test_code_block(self):
        markdown = "```\nprint('hello')\n```"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.CODE)

    # test unordered list detection
    def test_unordered_list_block(self):
        markdown = "- item one\n- item two\n- item three"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.UNORDERED_LIST)

    # test ordered list detection
    def test_ordered_list_block(self):
        markdown = "1. first item\n2. second item\n3. third item"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.ORDERED_LIST)

    # test paragraph detection
    def test_paragraph_block(self):
        markdown = "this is just a normal paragraph"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.PARAGRAPH)

    # test that broken ordered lists are NOT treated as ordered lists
    def test_invalid_ordered_list_becomes_paragraph(self):
        markdown = "1. first item\n3. skipped number"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.PARAGRAPH)

    # test that mixed quote/non-quote lines become paragraph
    def test_invalid_quote_becomes_paragraph(self):
        markdown = "> quoted line\nnormal line"

        result = block_to_block_type(markdown)

        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
# this allows the tests to run when the file is executed directly
if __name__ == "__main__":
    unittest.main()