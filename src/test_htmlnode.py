import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_obj_repr(self):
        node = HTMLNode("h1","Hello World")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(repr(node), "HTMLNode(h1, Hello World, None, None)")
    
    def test_obj_with_dict(self):
        node = HTMLNode("body", None, ["h2"], {"class": "some_class"})
        self.assertEqual(node.tag, "body")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, ["h2"])
        self.assertEqual(node.props, {"class": "some_class"})
    
    def test_props_to_html(self):
        node = HTMLNode("body", None, ["h2"], {"class": "some_class"})
        self.assertEqual(node.props_to_html(), ' class="some_class"')

if __name__ == "__main__":
    unittest.main()