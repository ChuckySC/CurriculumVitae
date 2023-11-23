from modules.reportlab import ReportLabConfiguration
from reportlab.platypus import Paragraph

def generate_pdf(user_data: dict):
    configuration = ReportLabConfiguration()
    contact = {
        'name': user_data['name'],
        'linkedin': user_data['linkedin'],
        'github': user_data['github'],
        'email': user_data['email'],
        'address': user_data['address'],
        'phone': user_data['phone']
    }
    data = {
        'summary': user_data['summary'],
        'experience': '<br/>'.join([
            f'<b>{experience.position}</b>, {experience.organization}<br/> {experience.work_period}'
            for experience in user_data['experience']
        ]),
        'education': '<br/>'.join([
            f'<b>{education.institution}</b>, {education.facility}<br/><b>{education.module}</b><br/>{education.study_period}'
            for education in user_data['education']
        ]),
        'courses': '<br/>'.join([
            f'<b>{course.institution}</b>, {course.facility}<br/><b>{course.module}</b><br/>{course.study_period}'
            for course in user_data['courses']
        ]),
        'skills': '<br/>'.join([
            f'<b>Skills</b>  {", ".join([skill for skill in user_data["skills"]])}',
            f'<b>Workflows</b>  {", ".join([workflow for workflow in user_data["workflows"]])}'
        ])
    }
    tblData = [
        ['SUMMARY', Paragraph(data['summary'], configuration.styles['Content'])],
        ['EXPERIENCE', Paragraph(data['experience'], configuration.styles['Content'])],
        ['EDUCATION', Paragraph(data['education'], configuration.styles['Content'])],
        ['COURSES', Paragraph(data['courses'], configuration.styles['Content'])],
        ['IT SKILLS', Paragraph(data['skills'], configuration.styles['Content'])]
    ]
    configuration.generate_print_pdf(tblData, contact)