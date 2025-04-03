
https://github.com/user-attachments/assets/76d6c5f3-e07f-4a1d-881a-a7aee7206efe
Uploading Resume Tailoring.mp4…

# Resume Matcher and Tailoring Application

This project is a web application built using the Flask framework to help users analyze their resumes against job descriptions and receive tailored suggestions for improvement.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [How to Use](#how-to-use)
- [Features](#features)
- [Technologies Used](#technologies-used)

## Requirements

Before you can run this application, you need to have the following installed on your system:

* **Python 3.x:** The application is written in Python. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **pip:** The Python package installer, which usually comes bundled with Python.

## Setup

Follow these steps to set up the application locally:

1.  **Clone the Repository (if applicable):** If you have the project in a version control system like Git, clone the repository to your local machine:
    ```bash
    git clone <https://github.com/krakken190/Resume-Scorer-against-JD-and-Tailoring>
    cd <your_project_directory>
    ```
    *(Replace `<your_project_directory>` with the name of your project folder.)*

2.  **Install Dependencies:** Navigate to the project directory in your terminal and install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    *(Make sure you have a `requirements.txt` file in your project root.)*

3.  **Set Up OpenAI API Key:**
    * You will need an OpenAI API key to use the resume analysis and tailoring features.
    * Create a file named `api_key.txt` in the root directory of your project.
    * Paste your OpenAI API key into this file.
    * Alternatively, you can set the API key as an environment variable.

4.  **Run the Application:** Execute the Flask application using the following command in your terminal:
    ```bash
    python app.py
    ```
    The application will typically run on `http://127.0.0.1:5000/` (check the terminal output for the exact address).

## How to Use

1.  **Access the Application:** Open your web browser and navigate to the URL provided in the terminal when you run `app.py` (usually `http://127.0.0.1:5000/`).
2.  **Paste Job Description:** In the designated text area, paste the job description you want to analyze your resume against.
3.  **Upload Resume:** Click the "Choose File" button and select your resume file (in DOCX, TXT, or PDF format).
4.  **Analyze Resume:** Click the "Analyze Resume" button.
5.  **View Results:** The application will display the analysis results, including a match percentage and tailored suggestions for improving your resume.

## Features

* **Resume Analysis:** Calculates a match percentage between the provided resume and job description.
* **Tailoring Suggestions:** Provides specific, section-based recommendations (Skills, Experience, Keywords, Soft Skills, Other) to enhance your resume.
* **Supports Multiple File Formats:** Accepts resumes in DOCX, TXT, and PDF formats.
* **User-Friendly Interface:** Built with Flask and styled with CSS for an intuitive user experience.

## Technologies Used

* **Python:** Programming language for the backend.
* **Flask:** A micro web framework for building the application.
* **OpenAI API:** For natural language processing and generating analysis and suggestions.
* **PyPDF2:** For reading PDF files.
* **python-docx:** For reading DOCX files.
