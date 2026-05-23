import re
from enum import Enum
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    stirpped_markdown = markdown.strip()
    block_list = stirpped_markdown.split("\n\n")
    block_list = [block for block in block_list if block.strip()]
    return block_list

def block_to_block_type(markdown_block):
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    lines = markdown_block.split("\n")
    expected_number = 1
    is_quote = True
    is_code = False
    is_unordered_lst = True
    is_ordered_list  = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("- "):
            is_unordered_lst = False
        if not line.startswith(f"{expected_number}. "):
            is_ordered_list = False
        if line.startswith(f"{expected_number}. "):
            expected_number += 1
    if lines[0] == "```" and lines[-1] == "```" and len(lines) >= 3:
        is_code = True

    if is_quote:
        return BlockType.QUOTE
    elif is_code:
        return BlockType.CODE
    elif is_unordered_lst:
        return BlockType.UNORDERED_LIST
    elif is_ordered_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")

def paragraph_to_html_node(block):
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else: 
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    
    text = block[level + 1 :]

    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    clean_block = block[4:-3]
    raw_text_node = TextNode(clean_block, TextType.TEXT)
    html_node = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [html_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        stripped = line.lstrip(">").strip()
        new_lines.append(stripped)
    
    content = " ".join(new_lines)
    children = text_to_children(content)
    
    return ParentNode("blockquote", children)

def olist_to_html_node(block):
    items = []
    lines = block.split("\n")
    for line in lines:
        content = line.split(". ", 1)[1]
        children = text_to_children(content)
        items.append(ParentNode("li", children))
    
    return ParentNode("ol", items)

def ulist_to_html_node(block):
    items = []
    lines = block.split("\n")
    for line in lines:
        content = line[2:]
        children = text_to_children(content)
        items.append(ParentNode("li", children))

    return ParentNode("ul", items)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    
    return children
