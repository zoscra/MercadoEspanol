"""
Validation schemas using Marshmallow
"""
from marshmallow import Schema, fields, validate, ValidationError
import re


class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El email es requerido",
            "invalid": "Formato de email inválido"
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={
            "required": "La contraseña es requerida"
        }
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={
            "required": "El nombre es requerido"
        }
    )
    vehicle = fields.Str(
        validate=validate.Length(max=100)
    )
    vehicle_consume_km = fields.Float(
        validate=validate.Range(min=0, min_inclusive=True)
    )
    coordenates = fields.Str(
        required=True,
        error_messages={
            "required": "Las coordenadas son requeridas"
        }
    )


class UserLoginSchema(Schema):
    """Schema for user login validation"""
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El email es requerido",
            "invalid": "Formato de email inválido"
        }
    )
    password = fields.Str(
        required=True,
        error_messages={
            "required": "La contraseña es requerida"
        }
    )


class OfertaCreationSchema(Schema):
    """Schema for offer creation validation"""
    titulo = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200),
        error_messages={
            "required": "El título es requerido"
        }
    )
    descripcion = fields.Str(
        validate=validate.Length(max=2000)
    )
    precio_ud = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, min_inclusive=True),
        error_messages={
            "required": "El precio es requerido"
        }
    )
    ud = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={
            "required": "La unidad es requerida"
        }
    )
    img_cosecha = fields.Str(
        validate=validate.Length(max=500)
    )


class PasswordResetSchema(Schema):
    """Schema for password reset validation"""
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El email es requerido",
            "invalid": "Formato de email inválido"
        }
    )


class PasswordUpdateSchema(Schema):
    """Schema for password update validation"""
    token = fields.Str(
        required=True,
        error_messages={
            "required": "El token es requerido"
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={
            "required": "La nueva contraseña es requerida"
        }
    )
