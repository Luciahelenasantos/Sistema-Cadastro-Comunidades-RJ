from marshmallow import Schema, fields

class ErrorSchema(Schema):
    """ Define como uma mensagem de erro será representada. """
    message = fields.Str(required=True)
    code = fields.Int()  # Código de status HTTP ou código de erro interno
    details = fields.Str()  # Detalhes adicionais sobre o erro
    