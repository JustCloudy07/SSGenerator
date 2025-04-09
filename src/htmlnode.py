class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Method has not been implemented yet.")

    def props_to_html(self):
        if self.props is None:
            return ""
        string = ""
        for value in self.props:
            string += f' {value}="{self.props[value]}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
