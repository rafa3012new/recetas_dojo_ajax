from flask_recetas_dojo_ajax import app
#importas el archivo de controlador
from flask_recetas_dojo_ajax.controllers import core
#importas el blueprrint
from flask_recetas_dojo_ajax.controllers.recetas import recetas

app.register_blueprint(recetas, url_prefix='/recetas')

if __name__ == "__main__":
    app.run(debug=True)