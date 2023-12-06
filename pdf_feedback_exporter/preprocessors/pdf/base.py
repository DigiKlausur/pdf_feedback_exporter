from traitlets.config import LoggingConfigurable
from abc import abstractmethod
from typing import Dict


class PDFPreprocessor(LoggingConfigurable):
    @abstractmethod
    def preprocess(self, resources: Dict) -> Dict:
        pass
