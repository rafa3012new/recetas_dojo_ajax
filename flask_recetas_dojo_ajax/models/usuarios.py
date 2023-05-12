import os
# from re import T
# from tkinter import ttk
from flask import flash
from datetime import datetime
from flask_recetas_dojo_ajax.config.mysqlconnection import connectToMySQL
from flask_recetas_dojo_ajax.config.myfunctions import diferencia_tiempo
from flask_recetas_dojo_ajax.models import modelo_base
from flask_recetas_dojo_ajax.models import recetas
from flask_recetas_dojo_ajax.utils.regex import REGEX_CORREO_VALIDO

class Usuario(modelo_base.ModeloBase):

    modelo = 'usuarios'
    campos = ['usuario', 'nombre','apellido','email','password']

    def __init__(self, data):
        self.id = data['id']
        self.usuario = data['usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.recetas = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def buscar(cls, dato):
        query = "select * from usuarios where usuario = %(dato)s OR email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_usuarios_enviar(cls, dato):

        query = "select * from usuarios where id <> %(id)s"

        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, dato)


        all_data = []

        if results:
            #convertimos la lista de json (diccionarios) en una lista de objetos python
            for data in results:
                all_data.append(cls(data))

        return all_data


    @staticmethod
    def validar_requerido(data, campo, nombre_campo_alt=''):
        is_valid = True
        message_error = ""
        if len(data[campo]) == 0:
            nombre_campo = campo if (nombre_campo_alt == '') else nombre_campo_alt
            message_error = f'El campo {nombre_campo} es requerido, no debe quedar en blanco'
            is_valid = False
        return is_valid, message_error

    @staticmethod
    def validar_largo(data, campo, largo,nombre_campo_alt=''):
        is_valid = True
        message_error = ""
        if len(data[campo]) <= largo:
            nombre_campo = campo if (nombre_campo_alt == '') else nombre_campo_alt
            message_error = f'El largo del {nombre_campo} no puede ser menor o igual {largo}'
            is_valid = False
        return is_valid, message_error

    @classmethod
    def validar(cls, data):

        message_error = []
        cad = ""


        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid

        if 'user' in data:

            cad = ""
            cond = False
            validar_usuario, cad = cls.validar_requerido(data, 'user','Usuario')
            is_valid = validar_usuario
            cond = is_valid
            if cad != "":
                message_error.append(cad)

            if validar_usuario:
                 cad = ""
                 if is_valid == False: no_create = False
                 is_valid, cad = cls.validar_largo(data, 'user', 3,'Usuario')
                 if cad != "":
                     message_error.append(cad)

                 cad = ""
                 if is_valid == False: no_create = False
                 if cls.validar_existe('usuario', data['user']):
                     cad = 'el usuario ya esta ingresado'
                     message_error.append(cad)
                     is_valid = False

            if is_valid == False: no_create = False


        if 'firstname' in data:
            cad = ""
            validar_nombre, cad = cls.validar_requerido(data, 'firstname','Nombre')
            is_valid = validar_nombre
            if cad != "":
                message_error.append(cad)

            if validar_nombre:
                cad = ""
                is_valid, cad = cls.validar_largo(data, 'firstname', 1,'Nombre')
                if cad != "":
                    message_error.append(cad)

            if is_valid == False: no_create = False

        if 'lastname' in data:
            cad = ""
            validar_apellido, cad = cls.validar_requerido(data, 'lastname','Apellido')
            is_valid = validar_apellido
            if cad != "":
                message_error.append(cad)

            if validar_apellido:
                cad = ""
                is_valid, cad = cls.validar_largo(data, 'lastname', 1,'Apellido')
                if cad != "":
                    message_error.append(cad)

            if is_valid == False: no_create = False

        if 'password_reg' in data:
            cad = ""
            validar_password, cad = cls.validar_requerido(data, 'password_reg','Password')
            is_valid = validar_password
            if cad != "":
                 message_error.append(cad)

            if validar_password:
                cad = ""
                is_valid, cad = cls.validar_largo(data, 'password_reg', 7,'Password')
                if cad != "":
                    message_error.append(cad)

            if is_valid == False: no_create = False

            if 'cpassword_reg' in data:
                cad = ""
                validar_passwordc, cad = cls.validar_requerido(data, 'cpassword_reg','Password de Confirmacion')
                is_valid = validar_passwordc
                if cad != "":
                    message_error.append(cad)

                if validar_passwordc:
                    cad = ""
                    if data['password_reg'] != data['cpassword_reg']:
                        cad = 'la contraseña de confirmacion no concide con la contraseña'
                        message_error.append(cad)
                        is_valid = False

                if is_valid == False: no_create = False

        if 'email' in data:
            cad = ""
            validar_email, cad = cls.validar_requerido(data, 'email','correo electronico')
            is_valid = validar_email
            if cad != "":
                message_error.append(cad)

            if validar_email:
                cad = ""
                if not REGEX_CORREO_VALIDO.match(data['email']):
                    cad = 'El correo electronico no es válido'
                    message_error.append(cad)
                    is_valid = False

                cad = ""
                if cls.validar_existe('email', data['email']):
                    cad = 'el correo electronico ya fue ingresado'
                    message_error.append(cad)
                    is_valid = False

                if is_valid == False: no_create = False


        return no_create, message_error



    #relacion uno (1) a muchos
    #Metodo de clase de 1 a muchos = 1 usuario es autor de varias mensajes
    #Este metodo obtiene todos las recetas de las que un usuario es autor
    #Se obtinene los datos del usuario consultado...
    #Y luego se le agregan las recetas de las que el usuario es autor
    #La propiedad recetas, alamcenaran una lista de objetos...
    @classmethod
    def get_recetas_de_usuario( cls , dato):

        #Se obtienen los datos del usuario que consultamos
        query = 'SELECT * FROM usuarios where id = %(id)s'
        results = []
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db( query , dato)

        usuario = cls(results[0])


        #Se obtienen las recetas de las que el usuario es autor
        query = 'SELECT r.id, r.nombre,, r.descripcion, r.instrucciones, CONCAT(u.nombre, " ", u.apellido) as autor, r.created_at, r.updated_at FROM recetas r LEFT JOIN usuarios u ON r.autor = u.id WHERE u.id = %(id)s'
        results = []
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db( query , dato)

        #Almacenamos los datos de los mensajes de usuarios en la propiedad 
        if results:
            for row_from_db in results:
                # ahora parseamos los datos de los mensajes para crear instancias de usuarios y agregarlas a nuestra lista

                receta_data = {
                    "id" : row_from_db["id"],
                    "autor" : row_from_db["autor"],
                    "nombre" : row_from_db["nombre"],
                    "descripcion" : row_from_db["descripcion"],
                    "instrucciones" : row_from_db["instrucciones"],
                    "under30" : row_from_db["under30"],
                    "date_made" : row_from_db["date_made"],
                    "created_at": row_from_db["created_at"],
                    "updated_at": row_from_db["updated_at"]
                }

                usuario.recetas.append( recetas.Receta( receta_data ) )

        return usuario