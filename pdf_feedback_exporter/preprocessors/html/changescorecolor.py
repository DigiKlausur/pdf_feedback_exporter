from typing import Dict, Tuple

from bs4 import BeautifulSoup as Soup

from .base import HTMLPreprocessor


class ChangeScoreColor(HTMLPreprocessor):
    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        style = soup.new_tag("style", type="text/css")
        style.append("\n.panel-primary > .panel-heading {\n    color: #000\n}\n")
        soup.body.append(style)

        # Remove all fontawesome images
        for data in soup.find_all(attrs={"class": "fa"}):
            data.decompose()

        return soup, resources
