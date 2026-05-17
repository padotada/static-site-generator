from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str)->BlockType:
    lines = block.split("\n")
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(lines):
        return BlockType.QUOTE
    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def is_heading(block: str)->bool:
    count = 0
    for char in block:
        if char == "#":
            count+=1
        else:
            break
    return count >= 1 and count <= 6 and len(block) > count and block[count] == " "

def is_code(block: str)->bool:
    return block.startswith("```\n") and block.endswith("```")

def is_quote(lines: list[str])->bool:
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(lines: list[str])->bool:
    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(lines: list[str])->bool:
    expected_num = 1
    for line in lines:
        if not line.startswith(f"{expected_num}. "):
            return False
        expected_num += 1
    return True
def markdown_to_blocks(markdown: str)->list:
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        new_blocks.append(block)
    return new_blocks

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block_nodes.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            block_nodes.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            block_nodes.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(ordered_list_to_html_node(block))
        else:
            raise ValueError("Invalid block type")
    return ParentNode("div", block_nodes)
        
def paragraph_to_html_node(block):
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    heading_level = 0

    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break

    text = block[heading_level + 1:]
    children = text_to_children(text)

    return ParentNode(f"h{heading_level}", children)

def code_to_html_node(block):
    text = block[4:-3]

    code_node = text_node_to_html_node(
        TextNode(text, TextType.CODE)
    )

    return ParentNode("pre", [code_node]) 
    
def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []

    for line in lines:
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        elif line.startswith(">"):
            cleaned_lines.append(line[1:])

    text = "\n".join(cleaned_lines)
    children = text_to_children(text)

    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        item_text = line[2:]
        children = text_to_children(item_text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        parts = line.split(". ", 1)
        item_text = parts[1]

        children = text_to_children(item_text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ol", list_items)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes