from .base import HTMLPreprocessor
from typing import Tuple, Dict
from bs4 import BeautifulSoup as Soup


class PrettifyTables(HTMLPreprocessor):
    def preprocess(self, soup: Soup, resources: Dict) -> Tuple[Soup, Dict]:
        style = soup.new_tag("style", attrs=dict(type="text/css"))
        style.string = """
        td, th {
            padding: .75em;
        }

        tbody, thead {
            border: 1px solid black;
        }

        thead {
            background-color: #ddd !important;
        }

        @media print {
            .class {
                 background-color: #1a4567 !important;
                 -webkit-print-color-adjust: exact;
            }
        }
        """
        soup.head.append(style)
        return soup, resources
