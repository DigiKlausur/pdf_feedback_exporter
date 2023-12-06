from typing import Dict, Tuple

from bs4 import BeautifulSoup as Soup

from .base import HTMLPreprocessor


class FixMathLineBreaks(HTMLPreprocessor):
    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        mathjax_configs = soup.find_all(
            "script", attrs={"type": "text/x-mathjax-config"}
        )
        if len(mathjax_configs) > 0:
            config = mathjax_configs[0]
            mathjax_configs[0].string = config.text.replace(
                "automatic: true", "automatic: false"
            )
        return soup, resources
