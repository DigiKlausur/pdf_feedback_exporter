import os
import base64

from .base import HTMLPreprocessor
from typing import Tuple, Dict
from bs4 import BeautifulSoup as Soup


class EmbedImages(HTMLPreprocessor):
    def to_base64(self, img_path):
        with open(img_path, "rb") as f:
            img = f.read()
        b64 = base64.b64encode(img).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        for tag in soup.find_all("img"):
            img_src = tag["src"]
            img_path = os.path.join(resources["tmp_dir"], img_src)
            if os.path.exists(img_path):
                tag["src"] = self.to_base64(img_path)
        return soup, resources
