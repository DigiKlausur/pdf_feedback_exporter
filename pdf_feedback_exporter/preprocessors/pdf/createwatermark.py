import os
from typing import Dict

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from traitlets import Unicode

from .base import PDFPreprocessor


class CreateWatermark(PDFPreprocessor):
    language = Unicode("en", help="The language used for the watermark").tag(
        config=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = {
            "user": {"en": "Username", "de": "Benutzername"},
            "copy": {"en": "Copy", "de": "Kopie"},
            "copy_msg": {
                "en": "This is a copy of your exam",
                "de": "Dies ist eine Kopie Ihrer Klausur",
            },
            "distribution_warning": {
                "en": "Distributing this copy is not permitted!",
                "de": "Die Weitergabe ist nicht gestattet",
            },
        }

    def preprocess(self, resources: Dict) -> Dict:
        plt.ioff()
        student_id = resources["student_id"]
        name = resources["name"]
        watermark_path = os.path.join(resources["tmp_dir"], "watermark.pdf")
        watermark = PdfPages(watermark_path)
        alpha = 0.1
        color = "blue"
        fig, ax = plt.subplots(1, 1, figsize=(8.3, 11.7))

        fig.patch.set_alpha(0.1)

        ax.axis("off")

        if name is not None:
            msg = f'{self.messages["copy"][self.language]} {name}\n{self.messages["user"][self.language]}: {student_id}'
        else:
            msg = f'{self.messages["user"][self.language]}: {student_id}'
        ax.text(0.7, 0, msg, c=color, alpha=0.4)
        ax.text(
            0,
            0,
            self.messages["copy_msg"][self.language],
            fontsize=40,
            rotation=54.73,
            c=color,
            alpha=alpha,
        )

        ax.text(
            0.4,
            0.3,
            self.messages["distribution_warning"][self.language],
            fontsize=20,
            rotation=54.73,
            c=color,
            alpha=alpha,
        )
        watermark.savefig(fig)
        plt.close(fig)

        watermark.close()

        resources.update(dict(watermark=watermark_path))

        return resources
