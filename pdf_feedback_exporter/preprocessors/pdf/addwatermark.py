import os
from typing import Dict

import PyPDF2

from .base import PDFPreprocessor


class AddWatermark(PDFPreprocessor):
    def preprocess(self, resources: Dict) -> Dict:
        with open(resources["watermark"], "rb") as watermark, open(
            resources["pdf"], "rb"
        ) as feedback:
            feedback_pdf = PyPDF2.PdfReader(feedback)
            watermark_pdf = PyPDF2.PdfReader(watermark)
            output_pdf = PyPDF2.PdfWriter()
            watermark_page = watermark_pdf.pages[0]

            for idx in range(len(feedback_pdf.pages)):
                pdf_page = feedback_pdf.pages[idx]
                pdf_page.merge_page(watermark_page)
                output_pdf.add_page(pdf_page)

            os.makedirs(os.path.split(resources["out_path"])[0], exist_ok=True)
            with open(resources["out_path"], "wb") as out:
                output_pdf.write(out)
        return resources
