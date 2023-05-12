import os
from flask import redirect, render_template, request, session, jsonify, Blueprint
from flask_recetas_dojo_ajax import app
# from flask_bcrypt import Bcrypt
# from flask_recetas_dojo_ajax.models.usuarios import Usuario
from flask_recetas_dojo_ajax.models.recetas import Receta
from datetime import datetime

recetas = Blueprint('recetas', __name__)

# bcrypt = Bcrypt(app)

@recetas.route("/procesar_receta", methods=["POST"])
def procesar_receta():

    fecha = datetime.date
    date_format = '%Y-%m-%d %H:%M:%S'

    data_json = request.json



    if type(data_json['date_made_receta']) is str and (data_json['date_made_receta'] != ''):
        fecha = datetime.strptime(data_json['date_made_receta'] + " 00:00:00",date_format)
    if data_json['date_made_receta'] == '': fecha = ''


    data ={
            'autor':session['idusuario'],
            'nombre':data_json['nombre_receta'],
            'descripcion':data_json['descripcion_receta'],
            'instrucciones':data_json['instrucciones_receta'],
            'under30':int(data_json['under30']),
            'date_made':fecha
           }



    validar, mensaje_validar = Receta.validar(data)



    if not validar :
        mensaje = [{"mensaje_validar":mensaje_validar}]
        if data_json['operacion_receta'] == 'Editar Receta':
            mensaje = mensaje[0]
        return jsonify(data_respuesta_json=mensaje)



    try:
        if data_json['operacion_receta'] == 'Nueva Receta':
            id_receta = Receta.save(data)
            datos_recetas = []
            datos_recetas = Receta.get_by_id_extra(id_receta,False)
            return jsonify(data_respuesta_json = datos_recetas)
        if  data_json['operacion_receta'] == 'Editar Receta':
            data['id'] = int(data_json['id'])
            Receta.update_recetas(data)
            datos_recetas = Receta.get_by_id_extra(data_json['id'])[0]
            print("receta guardado con exito!",flush=True)
            return jsonify(data_respuesta_json = datos_recetas)
    except Exception as error:
        print(f"error al guardar la receta, muy extrano, valor del error : {error}",flush=True)
        return redirect('/')

    return redirect('/')


@recetas.route("/eliminar_receta", methods=["POST"])
def eliminar_receta():

    data_json = request.json

    try:
        Receta.delete(int(data_json['id']))
        print(f"Eliminacion de receta con exito {id}",flush=True)
        data = {"type":"warning",
                "message":"Se elimino la receta correctamente"}
    except Exception as error:
        print("error al eliminar la receta",flush=True)
        data = {"type":"danger",
                "message":"No se elimino la receta correctamente"}


    return jsonify(data_respuesta_json = data)


@recetas.route("/detalle_receta/<id>")
def detalle_receta(id):
    datos_receta = Receta.get_by_id_extra(int(id))[0]
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    operacion = "Ver Receta"
    return render_template('detail.html',receta=datos_receta,sistema=nombre_sistema, operacion =operacion)


@recetas.route("/editar_receta/<id>")
def editar_receta(id):
    datos_receta = Receta.get_by_id_extra(int(id))[0]
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    operacion = "Editar Receta"
    return render_template('detail.html',receta=datos_receta,sistema=nombre_sistema, operacion = operacion)