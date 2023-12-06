from abc import abstractmethod
from typing import Dict

from traitlets.config import LoggingConfigurable


class PDFPreprocessor(LoggingConfigurable):
    @abstractmethod
    def preprocess(self, resources: Dict) -> Dict:
        pass
