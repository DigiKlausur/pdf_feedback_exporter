from .base import HTMLPreprocessor
from typing import Tuple, Dict
from bs4 import BeautifulSoup as Soup
import re


class MakeColorsImportant(HTMLPreprocessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p_color = re.compile(r"(color\s*:\s*)([#\w]+)")

    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        elems = soup.find_all()
        for elem in elems:
            if "style" in elem.attrs:
                elem.attrs["style"] = self.p_color.sub(
                    r"\1\2 !important", elem.attrs["style"]
                )
        return soup, resources
