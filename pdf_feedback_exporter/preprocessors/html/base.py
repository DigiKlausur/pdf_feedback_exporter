from abc import abstractmethod
from typing import Dict, Tuple

from bs4 import BeautifulSoup as Soup
from traitlets.config import LoggingConfigurable


class HTMLPreprocessor(LoggingConfigurable):
    @abstractmethod
    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        pass
