import re
from .base import HTMLPreprocessor
from typing import Tuple, Dict
from bs4 import BeautifulSoup as Soup
from traitlets import Float


class ChangeTotalScore(HTMLPreprocessor):
    new_score = Float(default_value=None, allow_none=True).tag(config=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p_total_score = re.compile(r"Score: (\d+\.\d{1,2})\s*/\s*(\d+\.\d{1,2})")

    def find_score_tag(self, soup: Soup):
        for tag in soup.find_all("div"):
            if tag.has_attr("class") and "panel-heading" in tag["class"]:
                return tag.find("h4")

    def replace_score(self, string: str):
        return self.p_total_score.sub(f"Score: \\1 / {self.new_score}", string)

    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        score_tag = self.find_score_tag(soup)
        if self.new_score is not None and score_tag is not None:
            score_tag.string = self.replace_score(score_tag.string)

        return soup, resources
