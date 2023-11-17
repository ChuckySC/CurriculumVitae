from flask import Blueprint, render_template, abort, request, url_for, redirect
from datetime import datetime

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
        from app import User, Skill, UserSkill
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
            
            # TODO save education
            # TODO save experience
            
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
            'skills': Skill.query.filter_by(isSkill=True).order_by(Skill.name),
            'workflows': Skill.query.filter_by(isSkill=False).order_by(Skill.name)
        }
        return render_template('user-create.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/details/<int:id>', methods=['GET'])
def user_details(id):
    try:
        from app import User, UserSkill, Skill
        user = User.query.get(int(id))
        user_skills = UserSkill.query.filter_by(user_id=id)
        
        skills = []
        workflows = []
        for element in user_skills:
            skill = Skill.query.get(int(element.skill_id))
            if skill.isSkill:
                skills.append(skill.name)
            else:
                workflows.append(skill.name)
            
        context = {
            'type': 'user-details',
            'about': {
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
        from app import User
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
            return redirect(url_for('app_views.index'))
        
        context = {
            'type': 'user-edit',
            'about': {
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
            }
        }
        return render_template('user-edit.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.post('/user/remove/<int:id>')
def user_remove(id):
    try:
        from app import User
        user = User.query.get_or_404(id)
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
                    isSkill=True
                ).save()
            else:
                Skill(
                    name=request.form['workflowname'],
                    isSkill=False
                ).save()

        context = {
            'type': 'skill-create',
            'skills': Skill.query.filter_by(isSkill=True).order_by(Skill.name),
            'workflows': Skill.query.filter_by(isSkill=False).order_by(Skill.name)
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
            'skills': Skill.query.filter_by(isSkill=True).order_by(Skill.name),
            'workflows': Skill.query.filter_by(isSkill=False).order_by(Skill.name)
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