import unittest
from src.block_markdown import *
from src.htmlnode import *
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

class TestMarkdownToHtmlNode(unittest.TestCase):
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
        
    def test_headings(self):
        md = """
# Heading 1

## Heading 2

###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h6>Heading 6</h6></div>",
        )
        
    def test_heading_with_inline_markdown(self):
        md = """
# This is **bold** heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is <b>bold</b> heading</h1></div>",
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
        
    def test_quote_block(self):
        md = """
> This is a quote
> with multiple lines
> and **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith multiple lines\nand <b>bold</b> text</blockquote></div>",
        )
        
    def test_quote_block_without_space_after_greater_than(self):
        md = """
>This is a quote
>with no spaces after the marker
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith no spaces after the marker</blockquote></div>",
        )    
        
    def test_unordered_list(self):
        md = """
- First item
- Second item
- Third item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
    )
        
    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
    )
    
    def test_links_and_images_in_paragraph(self):
        md = """
This paragraph has a [link](https://example.com) and an ![image alt](image.png)
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This paragraph has a <a href="https://example.com">link</a> and an <img src="image.png" alt="image alt"></p></div>',
        )
    
    def test_multiple_block_types(self):
        md = """
# My Page

This is a paragraph with **bold** text.

- One item
- Two item

1. First
2. Second

> A quote here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>My Page</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>One item</li><li>Two item</li></ul><ol><li>First</li><li>Second</li></ol><blockquote>A quote here</blockquote></div>",
        )
    

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_extra_spaces(self):
        markdown = "#    Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_multiline(self):
        markdown = """
Some paragraph text

# My Page Title

More text here
"""
        self.assertEqual(extract_title(markdown), "My Page Title")

    def test_extract_title_ignores_h2(self):
        markdown = """
## This is not h1

# This is h1
"""
        self.assertEqual(extract_title(markdown), "This is h1")

    def test_extract_title_no_h1_raises_exception(self):
        markdown = """
This is a paragraph

## This is only h2
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_no_space_after_hash_is_not_h1(self):
        markdown = "#Hello"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
if __name__ == '__main__':
    unittest.main()