import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node, node2)
        
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
        
    def test_eq_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)
    
    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)
        
    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "boot.dev")
        self.assertEqual(node, node2)

            
    def test_neq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is the second text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_with_diff_text_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()