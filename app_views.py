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

@app_views.route('/user/<id>', methods=['GET'])
def user_details(id):
    try:
        from app import User
        user = User.query.get(int(id))
        context = {
            'type': 'user_details',
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
        return render_template('user-details.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/create/', methods=('GET', 'POST'))
def create():
    try:
        from app import User
        if request.method == 'POST':
            User(
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
            return redirect(url_for('app_views.index'))
        return render_template('create.html', context={'type': 'create'})
    except Exception as e:
        # logger for errors
        abort(500)