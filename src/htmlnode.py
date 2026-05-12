
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"      

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            result = f""
            for prop, prop_val in self.props.items():
                result += f' {prop}="{prop_val}"'
            return result                
        else: 
            return ""

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No Value found!")
        
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No Tag set!")
        
        if self.children is None:
            raise ValueError("No children found!")

        child_string = ""
        for child in self.children:
            child_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
