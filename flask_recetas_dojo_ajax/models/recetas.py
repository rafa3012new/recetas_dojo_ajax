import os
from flask import flash
from flask_recetas_dojo_ajax.config.mysqlconnection import connectToMySQL
from flask_recetas_dojo_ajax.models import modelo_base
from flask_recetas_dojo_ajax.models import usuarios
from flask_recetas_dojo_ajax.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Receta(modelo_base.ModeloBase):

    modelo = 'recetas'
    campos = ['autor', 'nombre', 'descripcion','instrucciones','under30','date_made']

    def __init__(self, data):
        self.id = data['id']
        self.autor = data['autor']
        self.nombre_autor = data['nombre_autor']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def buscar(cls, dato):
        query = "select * from recetas where id = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update_recetas(cls,data):
        print("data antes de actualizar",data,flush=True)
        query = 'UPDATE recetas SET nombre = %(nombre)s, descripcion = %(descripcion)s, instrucciones = %(instrucciones)s, under30 = %(under30)s, date_made = %(date_made)s WHERE id = %(id)s;'
        print("query antes de actualizar",query,flush=True)
        resultadox = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("resultadox de actualizar",resultadox,flush=True)
        return resultadox


    @staticmethod
    def validar_requerido(data, campo, nombre_campo_alt=''):
      print(f"entro a validar requerido con el campo {campo}",flush=True)
      try:  
        is_valid = True
        message_error = ""
        if data[campo] is None:
            nombre_campo = campo if (nombre_campo_alt == '') else nombre_campo_alt
            message_error = f'El campo {nombre_campo} es requerido, no debe quedar en blanco'
            is_valid = False
      
      except Exception as error:
        print(f"error validando requerido, error: {error}",flush=True)
      finally:
        print("fin de la vaidacion de requerido",flush=True)    
      return is_valid, message_error

    @staticmethod
    def validar_largo(data, campo, largo, nombre_campo_alt=''):

        is_valid = True
        error_message = ""

        if len(data[campo]) <= largo:
            nombre_campo = campo if (nombre_campo_alt == '') else nombre_campo_alt
            error_message +=  f'El largo del campo {nombre_campo} no puede ser menor o igual a {largo} error'
            print("error mensaje ",error_message,flush=True)
            is_valid = False
        return is_valid, error_message

    @classmethod
    def validar(cls, data):


        print("entro a validar receta",flush=True)

        error_message = []
        cad= ""


        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid

        if 'nombre' in data:
            cad = ""
            validar_requerido, cad = cls.validar_requerido(data, 'nombre', 'Nombre')
            is_valid = validar_requerido
            if cad!= "": error_message.append(cad)
            if is_valid == False: no_create = False

            if validar_requerido:
                cad = ""
                is_valid, cad = cls.validar_largo(data, 'nombre', 1)
                if cad!= "": error_message.append(cad)
                if is_valid == False: no_create = False


        if 'descripcion' in data:
            cad = ""
            validar_descripcion, cad = cls.validar_requerido(data, 'descripcion')
            is_valid = validar_descripcion
            if cad!= "": error_message.append(cad)
            if is_valid == False: no_create = False

            if validar_descripcion:
                cad = ""
                is_valid, cad = cls.validar_largo(data, 'descripcion', 3)
                if cad!= "": error_message.append(cad)
                if is_valid == False: no_create = False


        if 'instrucciones' in data:
            cad=""
            validar_instrucciones, cad = cls.validar_requerido(data, 'instrucciones')
            is_valid = validar_instrucciones
            if cad!= "": error_message.append(cad)
            if is_valid == False: no_create = False

            if validar_instrucciones:
                cad=""
                is_valid, cad = cls.validar_largo(data, 'instrucciones', 3)
                if cad!= "": error_message.append(cad)
                if is_valid == False: no_create = False



        if 'date_made' in data:
            cad = ""
            # fecha = data['date_made']
            # date_format = '%Y-%m-%d %H:%M:%S'

            # try:
            #     fecha_str = datetime.strftime(fecha,date_format)
            # except Exception as error:
            #     print(f"Error de conversion de fechas error es {error}",flush =True)

            # print("antes de validar requerido",flush=True)
            validar_date_made, cad = cls.validar_requerido(data, 'date_made','fecha de creacion')
            is_valid = validar_date_made
            if cad!= "": error_message.append(cad)
            if is_valid == False: no_create = False

        return no_create, error_message

    @classmethod
    def get_all_extra(cls,no_objeto=False):
        query = 'SELECT r.id, r.nombre, r.descripcion, r.instrucciones, r.under30, r.date_made, r.autor, r.created_at, r.updated_at, CONCAT(u.nombre, " ", u.apellido) as nombre_autor FROM recetas r left join usuarios u on r.autor = u.id'
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        # print("query get_all_extra ",results,flush=True)
        if no_objeto == False:
            #se devuelve como diccionario
            return results
        else:
            #se devuelve como obejto python
            all_data = []
            for data in results:
                all_data.append(cls(data))
            return all_data


    @classmethod
    def get_by_id_extra(cls, id, not_object=False):
        query = 'SELECT r.id, r.nombre, r.descripcion, r.instrucciones, r.under30, r.date_made, r.autor, r.created_at, r.updated_at, CONCAT(u.nombre, " ", u.apellido) as nombre_autor FROM recetas r left join usuarios u on r.autor = u.id where r.id = %(id)s'
        # print(query,flush=True)
        data = { 'id' : id }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        cadena = (results[0]['date_made']).strftime("%Y-%m-%d")
        #print("la cadena es ", cadena, flush=True)
        results[0]['date_made'] = cadena
        if not_object == True:
            return cls(results[0])
        else:
            return results