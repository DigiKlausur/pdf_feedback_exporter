import os
import shutil
import tempfile

from bs4 import BeautifulSoup as Soup
from nbgrader.apps import NbGrader, NbGraderAPI
from traitlets.config import LoggingConfigurable

from .preprocessors.html import (
    ChangeScoreColor,
    FixMathLineBreaks,
    MakeColorsImportant,
    PrettifyTables,
)
from .preprocessors.pdf import AddWatermark, ConvertHTML2PDF, CreateWatermark


def get_nbgrader_config():
    nbgrader = NbGrader()
    nbgrader.initialize([])
    return nbgrader.config


def get_name(student):
    if student["first_name"] is not None and student["last_name"] is not None:
        return f"{student['first_name']} {student['last_name']}"
    if student["first_name"] is not None:
        return student["first_name"]
    if student["last_name"] is not None:
        return student["last_name"]


def create_pdf_feedback(assignment, student, notebooks):
    html_preprocessors = [
        ChangeScoreColor,
        FixMathLineBreaks,
        MakeColorsImportant,
        PrettifyTables,
    ]
    pdf_preprocessors = [CreateWatermark, ConvertHTML2PDF, AddWatermark]
    api = NbGraderAPI(config=get_nbgrader_config())
    if student == "*":
        students = api.get_students()
    else:
        students = [api.get_student(student)]
    for student in students:
        feedback_path = api.coursedir.format_path(
            api.coursedir.feedback_directory, student["id"], assignment
        )
        for notebook in notebooks:
            with tempfile.TemporaryDirectory() as tmp:
                html = os.path.join(feedback_path, f"{notebook}.html")
                if not os.path.isfile(html):
                    print(f'No feedback found for {student["id"]}')
                    continue
                resources = dict(
                    assignment=assignment,
                    notebook=notebook,
                    student_id=student["id"],
                    name=get_name(student),
                    tmp_dir=tmp,
                    out_path=os.path.join(
                        api.coursedir.format_path(
                            "feedback_pdf", student["id"], assignment
                        ),
                        f"{student['id']}_{notebook}.pdf",
                    ),
                )
                shutil.copytree(feedback_path, tmp, dirs_exist_ok=True)
                with open(html, "r") as f:
                    soup = Soup(f, features="html.parser")
                for preprocessor in html_preprocessors:
                    soup, resources = preprocessor(config=api.config).preprocess(
                        soup, resources
                    )
                feedback_html_path = os.path.join(tmp, f"{notebook}.html")
                with open(feedback_html_path, "w") as f:
                    f.write(soup.prettify())
                resources.update(dict(feedback_html=feedback_html_path))
                for preprocessor in pdf_preprocessors:
                    resources = preprocessor(config=api.config).preprocess(resources)
