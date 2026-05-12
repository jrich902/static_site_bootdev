from textnode import *

def main():
    test_text = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test_text)

main()