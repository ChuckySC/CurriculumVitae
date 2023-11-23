from flask import Blueprint, render_template, abort, request, url_for, redirect, send_from_directory
from datetime import datetime

from functions.reportlab import generate_pdf

app_views = Blueprint('app_views', __name__)

# @app.route('/')
# def home():
#     return f"I'm alive. Move on..."

@app_views.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app_views.route('/', methods=['GET'])
def index():
    try:
        from app import User
        context = {
            'type': 'index',
            'users': User.query.all()
        }
        return render_template('index.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/create/', methods=('GET', 'POST'))
def user_create():
    try:
        from app import User, UserEducation, UserExperience, Skill, UserSkill

        if request.method == 'POST':
            user_id = User(
                firstname=request.form['firstname'],
                lastname=request.form['lastname'],
                street=request.form['street'],
                city=request.form['city'],
                postcode=request.form['postcode'],
                phone=request.form['phone'],
                email=request.form['email'],
                bio=request.form['bio'],
                li=request.form['li'],
                gh=request.form['gh']
            ).save()
            
            # save education
            counter = 0
            while f'institution-{counter}' in request.form:
                if request.form[f'institution-{counter}'] != '':
                    UserEducation(
                        user_id = user_id,
                        institution = request.form[f'institution-{counter}'],
                        facility = request.form[f'facility-{counter}'],
                        module = request.form[f'module-{counter}'],
                        study_period = request.form[f'studyperiod-{counter}'],
                        is_education = False if f'course-{counter}' in request.form else True
                    ).save()
                counter += 1

            # save experience
            counter = 0
            while f'position-{counter}' in request.form:
                if request.form[f'position-{counter}'] != '':
                    UserExperience(
                        user_id = user_id,
                        position = request.form[f'position-{counter}'],
                        organization = request.form[f'organization-{counter}'],
                        work_period = request.form[f'workperiod-{counter}']
                    ).save()
                counter += 1
            
            # save skills
            skills = Skill.query.all()
            for skill in skills:
                if f'skill-{skill.id}' in request.form:
                    UserSkill(
                        user_id=user_id,
                        skill_id=skill.id
                    ).save()

            return redirect(url_for('app_views.index'))
        
        context = {
            'type': 'user-create',
            'skills': Skill.query.filter_by(is_skill=True).order_by(Skill.name),
            'workflows': Skill.query.filter_by(is_skill=False).order_by(Skill.name)
        }
        return render_template('user-create.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/download/<int:id>', methods=['GET', 'POST'])
def user_download(id):
    try:
        from app import User, UserEducation, UserExperience, UserSkill, Skill

        user = User.query.get(int(id))
        user_experience = UserExperience.query.filter_by(user_id=id)
        user_education = UserEducation.query.filter_by(user_id=id, is_education=True)
        user_course = UserEducation.query.filter_by(user_id=id, is_education=False)
        user_skills = UserSkill.query.filter_by(user_id=id)

        skills = []
        workflows = []
        for element in user_skills:
            skill = Skill.query.get(int(element.skill_id))
            if skill.is_skill:
                skills.append(skill.name)
            else:
                workflows.append(skill.name)
        
        user_data = {
            'name': f'{user.firstname} {user.lastname}',
            'linkedin': user.li,
            'github': user.gh,
            'email': user.email,
            'address': f'{user.street}, {user.postcode} {user.city}',
            'phone': user.phone,
            'summary': user.bio,
            'experience': user_experience,
            'education': user_education,
            'courses': user_course,
            'skills': skills,
            'workflows': workflows
        }

        generate_pdf(user_data=user_data)
        return redirect(url_for('app_views.index'))
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/details/<int:id>', methods=['GET'])
def user_details(id):
    try:
        from app import User, UserEducation, UserExperience, UserSkill, Skill

        user = User.query.get(int(id))
        user_skills = UserSkill.query.filter_by(user_id=id)
        
        skills = []
        workflows = []
        for element in user_skills:
            skill = Skill.query.get(int(element.skill_id))
            if skill.is_skill:
                skills.append(skill.name)
            else:
                workflows.append(skill.name)
            
        context = {
            'type': 'user-details',
            'general': {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'street': user.street,
                'city': user.city,
                'postcode': user.postcode,
                'phone': user.phone,
                'email': user.email,
                'bio': user.bio,
                'linkedin': user.li,
                'github': user.gh
            },
            'experience': UserExperience.query.filter_by(user_id=id),
            'education': {
                'education': UserEducation.query.filter_by(user_id=id, is_education=True),
                'course': UserEducation.query.filter_by(user_id=id, is_education=False)
            },
            'skills': {
                'skills': skills,
                'workflows': workflows
            }
        }
        return render_template('user-details.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/edit/<int:id>', methods=('GET', 'POST'))
def user_edit(id):
    try:
        from app import User, UserEducation, UserExperience, Skill, UserSkill

        user = User.query.get_or_404(id)
        
        if request.method == 'POST':
            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            user.street = request.form['street']
            user.city = request.form['city']
            user.postcode = request.form['postcode']
            user.phone = request.form['phone']
            user.email = request.form['email']
            user.bio = request.form['bio']
            user.li = request.form['li']
            user.gh = request.form['gh']
            user.save()
            
            # remove all current user education & save new education
            UserEducation.removeAll(id)
            counter = 0
            while f'institution-{counter}' in request.form:
                if request.form[f'institution-{counter}'] != '':
                    UserEducation(
                        user_id = id,
                        institution = request.form[f'institution-{counter}'],
                        facility = request.form[f'facility-{counter}'],
                        module = request.form[f'module-{counter}'],
                        study_period = request.form[f'studyperiod-{counter}'],
                        is_education = False if f'course-{counter}' in request.form else True
                    ).save()
                counter += 1

            # remove all current user experience & save new experience
            UserExperience.removeAll(id)
            counter = 0
            while f'position-{counter}' in request.form:
                if request.form[f'position-{counter}'] != '':
                    UserExperience(
                        user_id = id,
                        position = request.form[f'position-{counter}'],
                        organization = request.form[f'organization-{counter}'],
                        work_period = request.form[f'workperiod-{counter}']
                    ).save()
                counter += 1

            # remove all current skills & save new skills
            UserSkill.removeAll(id)
            skills = Skill.query.all()
            for skill in skills:
                if f'skill-{skill.id}' in request.form:
                    UserSkill(
                        user_id=id,
                        skill_id=skill.id
                    ).save()

            return redirect(url_for('app_views.index'))

        context = {
            'type': 'user-edit',
            'skills': Skill.query.filter_by(is_skill=True),
            'workflows': Skill.query.filter_by(is_skill=False),
            'user': {
                'general': {
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'street': user.street,
                    'city': user.city,
                    'postcode': user.postcode,
                    'phone': user.phone,
                    'email': user.email,
                    'bio': user.bio,
                    'linkedin': user.li,
                    'github': user.gh
                },
                'experience': UserExperience.query.filter_by(user_id=id),
                'education': UserEducation.query.filter_by(user_id=id),
                'skill': [ skill.skill_id
                    for skill in UserSkill.query.filter_by(user_id=id)
                ]
            }
        }
        return render_template('user-edit.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.post('/user/remove/<int:id>')
def user_remove(id):
    try:
        from app import User, UserEducation, UserExperience, UserSkill

        user = User.query.get_or_404(id)
        UserEducation.removeAll(id)
        UserExperience.removeAll(id)
        UserSkill.removeAll(id)
        user.remove()
        return redirect(url_for('app_views.index'))
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/skill/create/<type>', methods=['GET', 'POST'])
def skill_create(type='skill'):
    try:
        from app import Skill

        if request.method == 'POST':
            if type == 'skill':
                Skill(
                    name=request.form['skillname'],
                    is_skill=True
                ).save()
            else:
                Skill(
                    name=request.form['workflowname'],
                    is_skill=False
                ).save()

        context = {
            'type': 'skill-create',
            'skills': Skill.query.filter_by(is_skill=True).order_by(Skill.name),
            'workflows': Skill.query.filter_by(is_skill=False).order_by(Skill.name)
        }
        return render_template('skill-create.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/skill/edit/<int:id>', methods=('GET', 'POST'))
def skill_edit(id):
    try:
        from app import Skill

        skill = Skill.query.get_or_404(id)
        
        if request.method == 'POST':
            skill.name = request.form['skillname']
            skill.save()
            return redirect(url_for('app_views.skill_create', type='skill'))
        
        context = {
            'type': 'skill-create',
            'skills': Skill.query.filter_by(is_skill=True).order_by(Skill.name),
            'workflows': Skill.query.filter_by(is_skill=False).order_by(Skill.name)
        }
        return render_template('skill-create.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.post('/skill/remove/<int:id>')
def skill_remove(id):
    try:
        from app import Skill

        skill = Skill.query.get_or_404(id)
        skill.remove()
        return redirect(url_for('app_views.skill_create', type='skill'))
    except Exception as e:
        # logger for errors
        abort(500)