from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
from pathlib import Path

output_path = Path('AI_Data_Quality_Assistant_Document.docx')

paragraphs = [
    'AI Data Quality Assistant - End-to-End Build and SOP Document',
    'Purpose',
    'This document explains the complete journey of building the AI Data Quality Assistant from the initial planning stage to the final working solution, including the technology choices, solution design, local execution, Docker packaging, and GitHub publishing.',
    'Business Problem',
    'Data engineers often struggle to detect and report data quality issues such as missing values, duplicate records, inconsistent values, and low-quality fields that may break analytics and reporting.',
    'Project Goal',
    'The application accepts CSV data, detects common quality problems, displays findings in a simple web interface, generates a readable issue report, and can be run locally or with Docker.',
    'Planning Phase',
    'The first task was to define the scope as a practical prototype for data quality monitoring. The focus was on keeping the solution simple, useful, and easy to demonstrate.',
    'Solution Design Flow',
    'User -> Web UI -> Backend API -> Data Analysis Engine -> Issue Detection -> Report Generation -> UI Output',
    'Technology Stack',
    'Backend: Python, FastAPI, Pandas, Uvicorn. Frontend: HTML, CSS, JavaScript. Deployment: Docker, Git, GitHub.',
    'Implementation SOP',
    '1. Create the project structure. 2. Define the backend API. 3. Implement the analysis logic. 4. Build the frontend UI. 5. Connect the frontend and backend. 6. Add sample data. 7. Test locally. 8. Dockerize the application. 9. Push to GitHub.',
    'Local Run Instructions',
    'Install dependencies with pip install -r requirements.txt. Start the app with python -m uvicorn app:app --host 127.0.0.1 --port 8000.',
    'Docker Deployment Instructions',
    'Build the image with docker build -t ai-data-quality-assistant . and run it with docker run -p 8000:8000 ai-data-quality-assistant.',
    'GitHub Publishing SOP',
    'Initialize Git, add files, commit, create the main branch, add the remote repository, and push with git push -u origin main.',
    'Future Enhancements',
    'Possible upgrades include database connectivity, real-time monitoring, AI-based root cause analysis, alerts, and richer dashboards.',
    'Conclusion',
    'This document captures the complete build story of the AI Data Quality Assistant from planning to implementation, solution design, Docker packaging, and GitHub deployment.'
]

content_xml = []
for paragraph in paragraphs:
    if paragraph.endswith(':'):
        content_xml.append(f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>{escape(paragraph)}</w:t></w:r></w:p>')
    elif paragraph in {'Purpose', 'Business Problem', 'Project Goal', 'Planning Phase', 'Solution Design Flow', 'Technology Stack', 'Implementation SOP', 'Local Run Instructions', 'Docker Deployment Instructions', 'GitHub Publishing SOP', 'Future Enhancements', 'Conclusion'}:
        content_xml.append(f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>{escape(paragraph)}</w:t></w:r></w:p>')
    else:
        content_xml.append(f'<w:p><w:r><w:t>{escape(paragraph)}</w:t></w:r></w:p>')

main_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(content_xml)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''

rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

with ZipFile(output_path, 'w', ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types_xml)
    zf.writestr('_rels/.rels', rels_xml)
    zf.writestr('word/document.xml', main_xml)

print(f'Created {output_path}')
