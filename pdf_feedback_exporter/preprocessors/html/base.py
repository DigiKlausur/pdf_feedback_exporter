from traitlets.config import LoggingConfigurable
from abc import abstractmethod
from typing import Tuple, Dict
from bs4 import BeautifulSoup as Soup


class HTMLPreprocessor(LoggingConfigurable):
    @abstractmethod
    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        pass
