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
        return render_template('user-create.html', context={'type': 'create'})
    except Exception as e:
        # logger for errors
        abort(500)

@app_views.route('/user/details/<int:id>', methods=['GET'])
def user_details(id):
    try:
        from app import User
        user = User.query.get(int(id))
        context = {
            'type': 'details',
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
            'type': 'edit',
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