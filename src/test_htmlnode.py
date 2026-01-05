import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a_with_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), """<a href="https://www.google.com">Click me!</a>""")
    
    def test_leaf_to_html_link(self):
        node = LeafNode("label", "Last name:", {"for":"lname"})
        self.assertEqual(node.to_html(), """<label for="lname">Last name:</label>""")
if __name__ == "__main__":
    unittest.main()