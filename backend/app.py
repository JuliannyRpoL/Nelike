from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, request, jsonify
from flask_cors import CORS

from models import Series

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Inicializar Firestore DB
cred = credentials.Certificate('key/key.json')
default_app = initialize_app(cred)
db = firestore.client()
series_ref = db.collection('series')

# Métodos de series

@app.route("/api/series",methods=['POST'])
def agregar_serie():
    data = request.json
    serie_id = str(request.json["nombre"])
    series_doc = series_ref.document(serie_id)

    if(series_doc.get().exists):
        error_message = {"error":f"Ya existe una serie registrada con el nombre {serie_id}"}
        return jsonify(error_message),400
    try:  
        nueva_serie = Series(data["nombre"], float(data["puntuacion"]), data["descripcion"], bool(data["vista"]), data["link"]).to_dict()
        series_doc.set(nueva_serie)
        return jsonify(nueva_serie),201
    except:
        error_message={"error":"Los datos de la serie no están completos o son incorrectos"}
        return jsonify(error_message),400


@app.route("/api/series", methods=['GET'])
def obtener_lista_series():
    results = series_ref.where(u"vista", u"==", True).stream()
    lista_series = [item.to_dict() for item in results]

    return jsonify({"data":lista_series}),200


@app.route("/api/guardadas", methods=['GET'])
def obtener_lista_seriesGuardadas():
    results = series_ref.where(u"vista", u"==", False).stream()
    lista_series = [item.to_dict() for item in results]

    return jsonify({"data":lista_series}),200


@app.route("/api/series/totalVistas", methods=['GET'])
def obtener_total_vistas():
    results = series_ref.where(u"vista", u"==", True).stream()
    num = 0
    for i in results:
        num += 1

    return jsonify({"data":num}),200


@app.route("/api/series/totalPorVer", methods=['GET'])
def obtener_total_por_ver():
    results = series_ref.where(u"vista", u"==", False).stream()
    num = 0
    for i in results:
        num += 1

    return jsonify({"data":num}),200


@app.route("/api/series/<string:nombre>",methods=['PUT'])
def editar_serie(nombre):
    data = request.json
    serie_id = nombre
    series_doc = series_ref.document(serie_id)

    if(series_doc.get().exists == False):
        error_message = {"error":f"No existe una serie registrada con el nombre {serie_id}"}
        return jsonify(error_message),400
    try:  
        serie_info = series_doc.get().to_dict()
        if("descripcion" in data):
            descripcion = data["descripcion"]           
        else:
            descripcion = serie_info["descripcion"]

        if("puntuacion" in data):
            puntuacion = float(data["puntuacion"])
        else:
            puntuacion = serie_info["puntuacion"]
            
        if("vista" in data):
            vista = bool(data["vista"])
        else:
            vista = serie_info["vista"] 

        if("link" in data):
            link = data["link"]
        else:
            link = serie_info["link"]           
                 
        serie_act = Series(nombre, puntuacion, descripcion, vista, link).to_dict()
        series_doc.update(serie_act)
        return jsonify(serie_act),200
    except:
        error_message={
            "error":"Los datos de la serie no están completos o son incorrectos",
            "status": 400
        }
        return jsonify(error_message),400


@app.route("/api/series/<string:nombre>",methods=['DELETE'])
def eliminar_serie(nombre):
    serie_id = nombre
    serie_doc = series_ref.document(serie_id)

    if(serie_doc.get().exists):
        serie_doc.delete()
        result={"nombre":nombre,"borrado":True}
        return jsonify(result),200
    else:
        error_message={"error":f"No se encontró ninguna serie con el nombre {nombre}"}
        return jsonify(error_message),400


if __name__ == '__main__':
    app.run(debug=True)