from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, { "href" : text_node.url })

    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", { "src" : text_node.url , "alt" : text_node.text})
    
    raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue        
        
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("unmatched delimiter, invalid markdown")
        
        split_nodes = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))

        new_nodes.extend(split_nodes)


    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        link_matches = extract_markdown_images(old_node.text)
        if len(link_matches) == 0:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        for image_alt, image_link in link_matches:
            sections = remaining.split(f"![{image_alt}]({image_link})", maxsplit=1)
            remaining = sections[1]
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        link_matches = extract_markdown_links(old_node.text)
        if len(link_matches) == 0:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        for link_text, link_href in link_matches:
            sections = remaining.split(f"[{link_text}]({link_href})", maxsplit=1)
            remaining = sections[1]
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_href))
        
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]  # start with one node
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # bold
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # code
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    stirpped_markdown = markdown.strip()
    block_list = stirpped_markdown.split("\n\n")
    block_list = [block for block in block_list if block.strip()]
    return block_list




