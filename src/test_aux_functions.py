import unittest
from aux_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_on_one_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT)])
        
    def test_multiple_delimiters(self):
        node = TextNode("This has `code` and `more code`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
        ])

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    def test_mixed_nodes(self):
        nodes = [
            TextNode("Start `code` here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("Start ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ])

    def test_empty_segments_removed(self):
        node = TextNode("`code`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
        ])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is `broken text", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("This is `code`", TextType.TEXT),
            TextNode(" and `more`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more", TextType.CODE),
        ])

    def test_chain_calls(self):
        node = TextNode("This is **bold** and `code`", TextType.TEXT)

        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![img1](url1.png) some text ![img2](url2.jpg)"
        )
        self.assertListEqual(
            [("img1", "url1.png"), ("img2", "url2.jpg")],
            matches
        )

    def test_extract_no_images(self):
        matches = extract_markdown_images("This has no images")
        self.assertListEqual([], matches)

    def test_image_with_empty_alt(self):
        matches = extract_markdown_images(
            "![](image.png)"
        )
        self.assertListEqual(
            [("", "image.png")],
            matches
        )

    def test_image_with_special_characters(self):
        matches = extract_markdown_images(
            "![my image 123!](https://example.com/img.png)"
        )
        self.assertListEqual(
            [("my image 123!", "https://example.com/img.png")],
            matches
        )

    def test_ignore_links(self):
        matches = extract_markdown_images(
            "[link](https://example.com)"
        )
        self.assertListEqual([], matches)

    def test_mixed_content(self):
        matches = extract_markdown_images(
            "Text ![img](url.png) and [link](url.com)"
        )
        self.assertListEqual(
            [("img", "url.png")],
            matches
        )


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_one_link(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[one](url1.com) and [two](url2.com)"
        )
        self.assertListEqual(
            [("one", "url1.com"), ("two", "url2.com")],
            matches
        )

    def test_extract_no_links(self):
        matches = extract_markdown_links("No links here")
        self.assertListEqual([], matches)

    def test_link_with_empty_text(self):
        matches = extract_markdown_links(
            "[](https://example.com)"
        )
        self.assertListEqual(
            [("", "https://example.com")],
            matches
        )

    def test_link_with_special_characters(self):
        matches = extract_markdown_links(
            "[click here! 123](https://example.com/page)"
        )
        self.assertListEqual(
            [("click here! 123", "https://example.com/page")],
            matches
        )

    def test_ignore_images(self):
        matches = extract_markdown_links(
            "![image](img.png)"
        )
        self.assertListEqual([], matches)

    def test_mixed_content(self):
        matches = extract_markdown_links(
            "Text [link](url.com) and ![img](img.png)"
        )
        self.assertListEqual(
            [("link", "url.com")],
            matches
        )
        
class TestSplitImagesAndLinks(unittest.TestCase):
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
            new_nodes
        )
if __name__ == '__main__':
    unittest.main()
