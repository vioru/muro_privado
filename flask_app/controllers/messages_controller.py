from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.messages import Message

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    print (request.form)
    Message.save(request.form) #diccionario con campos de formulario
    return redirect('/wall_user')

@app.route('/eliminar/mensaje/<int:id>')
def eliminar_mensaje(id):

    formulario = {'id': id}

    message = Message.get_messages_id(formulario) 

    if not int(session['user_id']) == message.receiver_id :
        return redirect('/danger')

    Message.eliminate(formulario)
    return redirect('/wall_user')