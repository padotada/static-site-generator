from enum import Enum

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
    