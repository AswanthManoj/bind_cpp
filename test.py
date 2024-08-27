# test.py

from bind_cpp import create_element, render

def test_html_generation():
    div = create_element("div")
    span = create_element("span", closing_tag=False)

    html_elements = [
        div("Hello, World!", "This is a div", cls="greeting"),
        span("This is a span", id="unique-span")
    ]

    html_output = render(html_elements)
    print(html_output)


if __name__ == "__main__":
    test_html_generation()
