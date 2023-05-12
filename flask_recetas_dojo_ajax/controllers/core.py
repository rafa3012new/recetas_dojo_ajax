import os
from flask import redirect, render_template, request, flash, session, jsonify
from flask_recetas_dojo_ajax import app
from flask_bcrypt import Bcrypt
from flask_recetas_dojo_ajax.models.usuarios import Usuario
from flask_recetas_dojo_ajax.models.recetas import Receta
from datetime import datetime


bcrypt = Bcrypt(app)

@app.route("/")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    datos_recetas = []

    if 'idusuario' in session:
        datos_recetas = Receta.get_all_extra(True)

    return render_template("main.html", sistema=nombre_sistema, recetas=datos_recetas)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    data_json = request.json

    validar, mensaje_validar =  Usuario.validar(data_json)

    #validaciones del objeto usuario
    if not validar:
        mensaje = [{"mensaje_validar":mensaje_validar}]
        return jsonify(data_respuesta_json=mensaje)



    pass_hash = bcrypt.generate_password_hash(data_json['password_reg'])

    data = {
        'usuario' : data_json['user'],
        'nombre' : data_json['firstname'],
        'apellido' : data_json['lastname'],
        'email' : data_json['email'],
        'password' : pass_hash,
    }

    resulta = Usuario.save(data)


    if not resulta:
        mensaje = [{"mensaje_validar":['error al crear la cuenta de usuario']}]
        return jsonify(data_respuesta_json=mensaje)


    resultado = Usuario.get_by_id(resulta)


    return jsonify(data_respuesta_json = resultado)


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    data = request.form

    #print(data,flush=True)

    usuario = Usuario.buscar(data['identification'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, data['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['idusuario'] = usuario.id
    session['usuario'] = usuario.nombre + " " + usuario.apellido


    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')