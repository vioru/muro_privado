from flask import render_template, redirect, session, request, flash

from flask_app import app

from flask_app.models.users import User

from datetime import datetime, timedelta

#para usar las funciones de mensajes
from flask_app.models.messages import Message


from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

#1
@app.route('/')
def index():
    
    return render_template('index.html')




#2
@app.route('/registrate', methods = ['POST'])
def registrate():
    if not User.valid_user(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password']) #encripta la contraseña del usuario, ojo debes poner un buen espacio en la tabla cuando crees esta parte
    
    formulario={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pwd
        
    }
    

    id = User.save(formulario)

    session['user_id'] = id
    
    return redirect('/wall_user')




@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')
        
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Contraseña incorrecta', 'login')
        return redirect('/')
    
    
    
    session['user_id'] = user.id
    
    return redirect('/wall_user')



@app.route('/wall_user')
def wall():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Usuario que inicio sesión

    users = User.get_all() #Lista de TODOS los usuarios

    messages = Message.get_user_messages(formulario) #Lista con todos los mensajes de la persona que inició sesión

    return render_template('wall_user.html', user=user, users=users, messages=messages)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route ('/danger')
def danger():
    session.clear()
    return render_template('danger.html')
    