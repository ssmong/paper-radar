import unittest
from html.parser import HTMLParser

import build


class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class RenderingTests(unittest.TestCase):
    def test_external_review_and_paper_text_cannot_create_active_html(self):
        attack = '<img src=x onerror="alert(1)">'
        review = build.render_review_section({
            "found": True, "url": 'javascript:alert(1)', "venue": attack,
            "avg_rating": attack, "reviews": [{"summary": attack, "rating": attack}],
        })
        markdown = build.render_inline(attack + ' [link](javascript:evil) **bold**')
        table = build.render_table([attack], [[f'**{attack}**']], "7",
                                   {build.norm(attack): "section7/test"}, "Search")
        for html in (review, markdown, table):
            parsed = Tags(html)
            self.assertFalse(any(tag in {"img", "script"} for tag, _ in parsed.tags))
            for _, attrs in parsed.tags:
                self.assertFalse(any(name.startswith("on") for name in attrs))
                self.assertFalse(attrs.get("href", "").startswith("javascript:"))
        self.assertIn("<strong>bold</strong>", markdown)

    def test_markdown_links_keep_query_parameters(self):
        rendered = build.render_inline('[**Paper**](https://example.org/?a=1&b=2)')
        self.assertIn(("a", {"href": "https://example.org/?a=1&b=2",
                                 "target": "_blank", "rel": "noopener"}), Tags(rendered).tags)
        self.assertIn("<strong>Paper</strong>", rendered)


if __name__ == "__main__":
    unittest.main()
