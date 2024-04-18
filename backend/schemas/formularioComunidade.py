from marshmallow import Schema, fields, post_load
from model import FormularioComunidade

class FormularioComunidadeSchema(Schema):
    id = fields.Int(dump_only=True)
    cod_assoc = fields.Int(load_only=True)
    pergunta = fields.Str(required=True)
    resposta = fields.Str(required=True)
    data_formulario = fields.DateTime(dump_only=True)

    @post_load
    def make_formulario_comunidade(self, data, **kwargs):
        return FormularioComunidade(**data)
    