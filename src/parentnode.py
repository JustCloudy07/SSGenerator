from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode has no tag")
        if self.children is None:
            raise ValueError("ParentNode has no children")
        parent_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            parent_string += child.to_html()
        parent_string += f"</{self.tag}>"
        return parent_string

    def __repr__(self):
        return f"ParentNode({self.tag}, children = {self.children}, {self.props})"
