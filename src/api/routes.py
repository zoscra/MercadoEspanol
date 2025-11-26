"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Oferta
from api.utils import generate_sitemap, APIException
from api.schemas import (
    UserRegistrationSchema, UserLoginSchema, OfertaCreationSchema,
    PasswordResetSchema, PasswordUpdateSchema
)
from flask_cors import CORS
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message
from extension import mail
import os
import re
from flask_jwt_extended import decode_token
import jwt
from marshmallow import ValidationError



url_front = os.getenv('VITE_FRONT_URL')




api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)




@api.route('/', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Post para registrar un usuario
@api.route('/user/register', methods=['POST'])
def user_register():
    schema = UserRegistrationSchema()

    try:
        # Validar datos de entrada
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Verificar si el usuario ya existe
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "El email ya está registrado"}), 400

    # Hash de la contraseña
    new_pass = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    # Crear nuevo usuario
    new_user = User()
    new_user.name = data["name"]
    new_user.email = data["email"]
    new_user.password = new_pass.decode()
    new_user.vehicle = data.get("vehicle")
    new_user.vehicle_consume_km = data.get("vehicle_consume_km")
    new_user.coordenates = data["coordenates"]

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg": "Usuario creado exitosamente",
        "user": new_user.serialize()
    }), 201



@api.route('/user/resetPassword', methods=['PUT'])
def user_resetPassWord():
    body = request.get_json()
    token = body.get("token")
    if not token:
        return jsonify({"error": "Token de autenticación no proporcionado"}), 401
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token["sub"]
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify({"error": "Usuario no válido o token expirado"}), 401
        password_data = body.get("password")
        if password_data:
            new_password = password_data.get("nuevaContraseña")
        else:
            new_password = body.get("password")
        if not new_password:
            return jsonify({"error": "Nueva contraseña es requerida"}), 400
        hashed_password = bcrypt.hashpw(
            new_password.encode(), bcrypt.gensalt())
        user.password = hashed_password.decode()
        db.session.commit()
        return jsonify({"msg": "Contraseña actualizada exitosamente"})
    except Exception as e:
        db.session.rollback()
        print(f"error: {e}")
        return jsonify({"error": "Error al actualizar la contraseña"}), 500

# Post para logear un usuario
@api.route("/user/login", methods=["POST"])
def user_login():
    schema = UserLoginSchema()

    try:
        # Validar datos de entrada
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if user is None:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    if bcrypt.checkpw(data["password"].encode(), user.password.encode()):
        user_serialize = user.serialize()
        token = create_access_token(identity=str(user_serialize["id"]))
        return jsonify({"token": token, "user": user_serialize}), 200

    return jsonify({"error": "Credenciales incorrectas"}), 401

# GET pedir informacion sobre un usuario
@api.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user is None:
        return jsonify("Usuario no valido"),400
    return jsonify({"user":user.serialize()})


# GET pedir informacion sobre todas las ofertas disponibles de todos los usuarios
@api.route("/user/ofertas", methods=["GET"])

def get_ofertas():

    ofertas = Oferta.query.all()
    iterar_ofertas = [oferta.serialize() for oferta in ofertas]
    if ofertas is None:
        return jsonify("No hay ofertas disponibles"),404
    return jsonify({"ofertas": iterar_ofertas}),200

# GET pedir informacion sobre una oferta

@api.route("/user/oferta/info/<int:oferta_id>", methods=["GET"])
@jwt_required()
def get_oferta(oferta_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user is None:
        return jsonify("Usuario no valido"),400
    
    oferta = Oferta.query.get(oferta_id)

    if oferta is None:
        return jsonify("No existe esa oferta"),400
    oferta_serializada = oferta.serialize()
    print(oferta_serializada)
    print(oferta)
    print(oferta_id)

    return jsonify(oferta_serializada)


# POST crear una nueva oferta
@api.route("/user/ofertas", methods=["POST"])
@jwt_required()
def post_ofertas():
    schema = OfertaCreationSchema()

    try:
        # Validar datos de entrada
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if user is None:
        return jsonify({"error": "Usuario no válido"}), 400

    # Crear nueva oferta
    nueva_oferta = Oferta()
    nueva_oferta.id_comprador = None
    nueva_oferta.coordenates_comprador = None
    nueva_oferta.id_vendedor = user.id
    nueva_oferta.esta_realizada = False
    nueva_oferta.descripcion = data.get("descripcion")
    nueva_oferta.titulo = data["titulo"]
    nueva_oferta.coordenates_vendedor = user.coordenates
    nueva_oferta.precio_ud = data["precio_ud"]
    nueva_oferta.ud = data["ud"]
    nueva_oferta.img_cosecha = data.get("img_cosecha")

    db.session.add(nueva_oferta)
    db.session.commit()

    return jsonify({
        "msg": "Oferta creada exitosamente",
        "oferta": nueva_oferta.serialize()
    }), 201


# PUT comprar una oferta

@api.route("/user/oferta/comprar/<int:oferta_id>", methods=["PUT"])
@jwt_required()
def comprar_oferta(oferta_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user is None:
        return jsonify("Usuario no valido"),400
    
    oferta = Oferta.query.get(oferta_id)
    oferta.id_comprador = user.id
    oferta.coordenates_comprador = user.coordenates
    oferta.esta_realizada = True
    db.session.add(oferta)
    db.session.commit()


    if oferta is None:
        return jsonify("No existe esa oferta"),400
    oferta_serializada = oferta.serialize()
    print(oferta_serializada)
    print(oferta)
    print(oferta_id)

    return jsonify(oferta_serializada)


@api.route("/user/oferta/vendedor/borrar/<int:oferta_id>", methods=["DELETE"])
@jwt_required()
def BorrarOfertas(oferta_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user is None:
        return jsonify("Usuario no valido"),400
    
    oferta = Oferta.query.get(oferta_id)
    if oferta is None:
        return jsonify({"mensaje": "Oferta no encontrada"}), 404
    if user.id != oferta.id_vendedor:
        return jsonify({"mensaje": "No tienes permiso para borrar esta oferta"}), 403
    
    db.session.delete(oferta)
    db.session.commit()
    return jsonify({"mensaje":"Lo has borrado correctamente"}),200


@api.route("/resetPassword", methods=['POST'])
def resetPassword():
    schema = PasswordResetSchema()

    try:
        # Validar datos de entrada
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user_email = data["email"]
    user = User.query.filter_by(email=user_email).first()

    if not user:
        # Por seguridad, no revelar si el usuario existe o no
        return jsonify({"msg": "Si el email existe, recibirás un enlace de recuperación"}), 200

    user_serialize = user.serialize()
    token = create_access_token(identity=str(user_serialize["id"]))
    cadena_modificada = re.sub(r"\.", "_", token)
    reset_url_password = f"{url_front}resetPassword/{cadena_modificada}"

    try:
        msg = Message(
            "Recuperación de Contraseña - Mercado Español",
            html=f"<p>Para restablecer tu contraseña, haz click <a href={reset_url_password}>aquí</a></p>",
            recipients=[user_email],
        )
        mail.send(msg)
    except Exception as e:
        print(f"Error enviando email: {e}")
        return jsonify({"error": "Error al enviar el email"}), 500

    return jsonify({"msg": "Email de recuperación enviado exitosamente"}), 200