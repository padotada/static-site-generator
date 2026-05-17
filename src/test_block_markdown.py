import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        block = "This is a paragraph.\nIt continues on another line."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_one(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_six(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_no_space_is_paragraph(self):
        block = "#Heading without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes_is_paragraph(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_must_start_with_backticks_newline(self):
        block = "```print('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_must_end_with_backticks(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_without_space_after_greater_than(self):
        block = ">This is also a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiple_lines(self):
        block = "> Quote line one\n> Quote line two\n> Quote line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_one_bad_line_is_paragraph(self):
        block = "> Quote line one\nThis line is missing greater-than"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_single_item(self):
        block = "- item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_paragraph(self):
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_one_bad_line_is_paragraph(self):
        block = "- item one\nitem two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = "1. item one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        block = "2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        block = "1. item one\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space_is_paragraph(self):
        block = "1.item one\n2.item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_one_bad_line_is_paragraph(self):
        block = "1. item one\nnot an ordered list line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
class TestMarkdownToBlocks(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()