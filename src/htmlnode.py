
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
    
