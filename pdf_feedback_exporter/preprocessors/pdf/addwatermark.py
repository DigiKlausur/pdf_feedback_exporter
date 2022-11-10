import os
from typing import Dict

import PyPDF2

from .base import PDFPreprocessor


class AddWatermark(PDFPreprocessor):
    def preprocess(self, resources: Dict) -> Dict:
        with open(resources["watermark"], "rb") as watermark, open(
            resources["pdf"], "rb"
        ) as feedback:
            feedback_pdf = PyPDF2.PdfFileReader(feedback)
            watermark_pdf = PyPDF2.PdfFileReader(watermark)
            output_pdf = PyPDF2.PdfFileWriter()
            watermark_page = watermark_pdf.getPage(0)

            for idx in range(feedback_pdf.getNumPages()):
                pdf_page = feedback_pdf.getPage(idx)
                pdf_page.mergePage(watermark_page)
                output_pdf.addPage(pdf_page)

            os.makedirs(os.path.split(resources["out_path"])[0], exist_ok=True)
            with open(resources["out_path"], "wb") as out:
                output_pdf.write(out)
        return resources
