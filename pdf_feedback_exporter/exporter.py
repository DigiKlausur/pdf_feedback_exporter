import os
import shutil
import tempfile
from typing import Dict, List

from bs4 import BeautifulSoup as Soup
from e2xcore.api import E2xAPI
from nbgrader.apps import NbGrader
from traitlets.config import Config

from .preprocessors.html import (ChangeScoreColor, ChangeTotalScore,
                                 EmbedImages, FixMathLineBreaks,
                                 MakeColorsImportant, PrettifyTables)
from .preprocessors.html.base import HTMLPreprocessor
from .preprocessors.pdf import AddWatermark, ConvertHTML2PDF, CreateWatermark


def get_nbgrader_config() -> Config:
    """
    Get the NbGrader configuration.

    Returns:
        NbGraderConfig (Config): The initialized NbGrader configuration.
    """
    nbgrader = NbGrader()
    nbgrader.initialize([])
    return nbgrader.config


def get_name(student: Dict[str, str]) -> str:
    """
    Get the full name of a student based on the nbgrader student information.

    Args:
        student (Dict[str, str]): Dictionary containing student information with keys 'first_name' and 'last_name'.

    Returns:
        str: Full name of the student. If both first and last names are available, they are concatenated with a space.
             If only the first name is available, it is returned. If only the last name is available, it is returned.
    """
    if student["first_name"] is not None and student["last_name"] is not None:
        return f"{student['first_name']} {student['last_name']}"
    if student["first_name"] is not None:
        return student["first_name"]
    if student["last_name"] is not None:
        return student["last_name"]


def get_out_path(api: E2xAPI, student_id: str, assignment: str, notebook: str) -> str:
    """
    Get the output path for the PDF feedback file.

    Args:
        api (E2xAPI): An instance of the E2xAPI class.
        student_id (str): Identifier of the student.
        assignment (str): Identifier of the assignment.
        notebook (str): Name of the notebook.

    Returns:
        str: The full path for the PDF feedback file.
    """
    return os.path.join(
        api.coursedir.format_path("feedback_pdf", student_id, assignment),
        f"{student_id}_{notebook}.pdf",
    )


def process_notebook_html(
    html_path: str,
    resources: Dict,
    preprocessors: List[HTMLPreprocessor],
    config: Config,
) -> None:
    """
    Process the HTML content of a notebook using a series of HTML preprocessors.

    Args:
        html_path (str): Path to the HTML file of the notebook.
        resources (Dict): Dictionary containing information and resources for processing.
        preprocessors (List[HTMLPreprocessor]): List of HTML preprocessors to apply.
        config (Config): Configuration object.

    Returns:
        None: The function modifies the 'resources' dictionary in-place to include the processed HTML.
    """
    with open(html_path, "r") as file:
        soup = Soup(file, features="html.parser")

    for preprocessor in preprocessors:
        soup, resources = preprocessor(config=config).preprocess(soup, resources)

    notebook = resources["notebook"]

    feedback_html_path = os.path.join(resources["tmp_dir"], f"{notebook}.html")
    with open(feedback_html_path, "w") as file:
        file.write(soup.prettify())

    resources.update(dict(feedback_html=feedback_html_path))


def create_pdf_feedback(
    assignment: str,
    student: str,
    notebooks: List[str],
    language: str = "en",
    total_score: float = None,
) -> None:
    """
    Create PDF feedback for a given assignment, student, and notebooks.

    Args:
        assignment (str): Assignment identifier.
        student (str): Student identifier or "*" for all students.
        notebooks (List[str]): List of notebook names.
        language (Optional[str]): Language for watermark (en or de). Defaults to en.
        total_score (Optional[float]): Override total score. Defaults to None.
    """
    html_preprocessors = [
        EmbedImages,
        ChangeTotalScore,
        ChangeScoreColor,
        FixMathLineBreaks,
        MakeColorsImportant,
        PrettifyTables,
    ]
    pdf_preprocessors = [CreateWatermark, ConvertHTML2PDF, AddWatermark]
    config = get_nbgrader_config()
    config.CreateWatermark.language = language
    if total_score is not None:
        config.ChangeTotalScore.new_score = total_score
    api = E2xAPI(config=config)
    if student == "*":
        students = api.get_students()
    else:
        students = [api.get_student(student)]
    for student_info in students:
        student_id = student_info["id"]
        feedback_path = api.coursedir.format_path(
            api.coursedir.feedback_directory, student_id, assignment
        )
        for notebook in notebooks:
            with tempfile.TemporaryDirectory() as tmp:
                html = os.path.join(feedback_path, f"{notebook}.html")
                if not os.path.isfile(html):
                    print(f"No feedback found for {student_id}")
                    continue
                resources = dict(
                    assignment=assignment,
                    notebook=notebook,
                    student_id=student_id,
                    name=get_name(student_info),
                    tmp_dir=tmp,
                    out_path=get_out_path(api, student_id, assignment, notebook),
                )
                shutil.copytree(feedback_path, tmp, dirs_exist_ok=True)
                process_notebook_html(html, resources, html_preprocessors, config)

                for preprocessor in pdf_preprocessors:
                    resources = preprocessor(config=config).preprocess(resources)
