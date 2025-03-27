from flask import Flask, render_template, request, send_from_directory
import os
import openai
import PyPDF2
import docx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['ALLOWED_EXTENSIONS'] = {'docx', 'txt', 'pdf'}

# --- Read API Key from File ---
api_key_file = "api_key.txt"
api_key = None
try:
    with open(api_key_file, "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    print(f"Warning: API key file '{api_key_file}' not found. Please create it and add your OpenAI API key.")
except Exception as e:
    print(f"Error reading API key file: {e}")

# --- Text Extraction Functions (Adapted for Flask) ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX file: {e}"

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except Exception as e:
        return f"Error reading TXT file: {e}"

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

def extract_text_from_file(file_path):
    if not file_path:
        return ""
    if file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    elif file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        return "Unsupported file format."

# --- OpenAI Analysis Function ---
def analyze_with_gpt(jd_text, resume_text):
    if not jd_text or not resume_text:
        return "Please provide both the job description and your resume.", ""

    if not api_key:
        return "OpenAI API key not configured.", ""

    try:
        client = openai.Client(api_key=api_key)
        prompt = f"""You are a helpful career advisor. Your task is to analyze a job description and a resume and provide a match percentage and resume improvement suggestions.

        Step 1: Determine the percentage match (0-100%) between the provided Job Description and Resume.

        Step 2: If the match percentage is less than 80%, provide specific and actionable suggestions for improving the resume to better align with the job requirements. Categorize these suggestions under the following headings:
        - Skills
        - Experience
        - Keywords
        - Soft Skills
        - Other

        Format the response precisely as follows:
        Match Percentage: [percentage]%
        Suggestions:
        # Skills
        - [skill suggestion 1]
        - [skill suggestion 2]
        # Experience
        - [experience suggestion 1]
        ...
        # Keywords
        - [keyword suggestion 1]
        ...
        # Soft Skills
        - [soft skill suggestion 1]
        ...
        # Other
        - [other suggestion 1]
        ...
        If the match percentage is 80% or higher, respond with:
        Match Percentage: [percentage]%
        Suggestions: Your resume seems to be a good match for the job description!

        Job Description:
        '''
        {jd_text}
        '''

        Resume:
        '''
        {resume_text}
        '''
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful career advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        print(f"GPT Response Content:\n{content}") # Keep this for debugging

        match_percentage_str = ""
        suggestions_output = ""

        if "Match Percentage:" in content:
            parts = content.split("Match Percentage:")
            if len(parts) > 1:
                match_part = parts[1].split("%")[0].strip()
                match_percentage_str = match_part + "%"
                if "Suggestions:" in content:
                    suggestions_part = content.split("Suggestions:")
                    if len(suggestions_part) > 1:
                        suggestions_output = suggestions_part[1].strip()
                elif "good match" in content.lower():
                    suggestions_output = "Your resume seems to be a good match for the job description!"
                else:
                    suggestions_output = "Could not extract suggestions from the response."
            else:
                match_percentage_str = "Could not determine percentage."
                suggestions_output = "Could not extract suggestions from the response."
        else:
            match_percentage_str = "Could not determine percentage."
            suggestions_output = "Could not extract suggestions from the response."

        return match_percentage_str, suggestions_output

    except openai.OpenAIError as e:
        # Replace st.error with a Flask-friendly way to handle errors
        print(f"OpenAI API error: {e}")
        return f"OpenAI API error: {e}", ""

# --- Main Analysis Function (Flask) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    match_percentage = None
    suggestions = None

    if request.method == 'POST':
        jd_text = request.form.get('job_description')
        resume_file = request.files.get('resume_file')

        if jd_text and resume_file and allowed_file(resume_file.filename):
            try:
                # Save the uploaded file temporarily
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
                resume_file.save(filepath)
                resume_text = extract_text_from_file(filepath)
                os.remove(filepath) # Remove the temporary file

                if "Error reading" in resume_text or "Unsupported file format." in resume_text:
                    match_percentage = "Error"
                    suggestions = resume_text
                else:
                    match_percentage, suggestions = analyze_with_gpt(jd_text, resume_text)
            except Exception as e:
                match_percentage = "Error"
                suggestions = f"An error occurred: {e}"
        elif request.form.get('job_description') and not request.files.get('resume_file'):
            match_percentage = "Error"
            suggestions = "Please upload a resume file."
        elif not request.form.get('job_description') and request.files.get('resume_file'):
            match_percentage = "Error"
            suggestions = "Please paste the job description."
        else:
            match_percentage = "Error"
            suggestions = "Please provide both the job description and upload a resume."

    return render_template('index.html', match_percentage=match_percentage, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)