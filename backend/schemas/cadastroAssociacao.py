from marshmallow import Schema, fields, validate, post_load
from model import CadastroAssociacao

class CadastroAssociacaoSchema(Schema):
    cod_assoc = fields.Int(dump_only=True)
    nome_assoc = fields.Str(required=True)
    endereco = fields.Str(required=True)
    telefone = fields.Str(required=True, validate=validate.Regexp(r'^\(\d{2}\)\s?\d{4,5}-\d{4}$'))
    nome_coord = fields.Str(required=True)
    data_cadastro = fields.DateTime(dump_only=True)
    formularios = fields.Nested('FormularioComunidadeSchema', many=True, only=['id', 'pergunta', 'resposta'])

    @post_load
    def make_cadastro_associacao(self, data, **kwargs):
        return CadastroAssociacao(**data)

class BuscaAssociacaoSchema(Schema):
    cod_assoc = fields.Int(required=False, missing=None)
    nome_assoc = fields.Str(required=False, missing=None)

class CadastroAssociacaoDeleteSchema(Schema):
    nome_assoc = fields.Str(required=True)
    