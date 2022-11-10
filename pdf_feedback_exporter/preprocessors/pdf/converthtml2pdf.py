import os
from typing import Dict

import pdfkit

from .base import PDFPreprocessor


class ConvertHTML2PDF(PDFPreprocessor):
    def preprocess(self, resources: Dict) -> Dict:
        pdf_path = os.path.join(resources["tmp_dir"], f'{resources["notebook"]}.pdf')
        pdfkit.from_file(
            resources["feedback_html"],
            pdf_path,
            options={"javascript-delay": 2000, "no-stop-slow-scripts": None},
        )
        resources.update(dict(pdf=pdf_path))
        return resources
