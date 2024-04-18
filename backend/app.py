# Bibliotecas padrão do Python
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

# Bibliotecas de terceiros
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from flask_cors import CORS
from flasgger import Swagger

# Módulos/aplicações locais
from logger import logger
from model import Session, CadastroAssociacao, FormularioComunidade
from schemas.cadastroAssociacao import CadastroAssociacaoSchema
from schemas.formularioComunidade import FormularioComunidadeSchema

app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template_file='swagger.yaml')

@app.route('/cadastrar', methods=['POST'])
def create_cadastro():
  # Obtém dados JSON do request
  data = request.get_json()
  schema = CadastroAssociacaoSchema()

  # Valida e desserializa os dados
  try:
      valid_data = schema.load(data)
      print(type(valid_data))
  except ValidationError as ve:
      logger.error(f"Erro de validação dos dados: {ve.messages}")
      return jsonify({"message": "Dados de entrada inválidos", "errors": ve.messages}), 400

  # Cria uma sessão do SQLAlchemy
  session = Session()
  try:
    # Verifica se já existe um cadastro com os mesmos dados únicos
    existing_cadastro = session.query(CadastroAssociacao).filter(
      (CadastroAssociacao.nome_assoc == valid_data.nome_assoc) |
      (CadastroAssociacao.endereco == valid_data.endereco) |
      (CadastroAssociacao.telefone == valid_data.telefone) |
      (CadastroAssociacao.nome_coord == valid_data.nome_coord)
    ).first()
  
    if existing_cadastro:
      logger.warning("Tentativa de criar um cadastro duplicado.")
      return jsonify({"message": "Um cadastro com os mesmos dados já existe."}), 409
  
    # Cria uma nova instância de CadastroAssociacao
    novo_cadastro = valid_data
    session.add(novo_cadastro)
    session.commit()
    logger.info(f"Cadastro criado com sucesso: {novo_cadastro.cod_assoc}")
    return jsonify(schema.dump(novo_cadastro)), 201
  except Exception as e:
    session.rollback()
    logger.error(f"Erro ao criar cadastro: {str(e)}", exc_info=True)
    return jsonify({"message": "Erro ao processar sua requisição"}), 500
  finally:
        session.close()

@app.route('/formularios', methods=['POST'])
def add_formulario():
  # Obtém dados JSON do request
  data = request.get_json()
  schema = FormularioComunidadeSchema()

  # Valida e desserializa os dados
  try:
    valid_data = schema.load(data)
  except ValidationError as ve:
    logger.error(f"Erro de validação dos dados: {ve.messages}")
    return jsonify({"message": "Dados de entrada inválidos", "errors": ve.messages}), 400
  
  # Cria uma sessão do SQLAlchemy
  session = Session()
  try:
    # Verifica se o CadastroAssociacao com cod_assoc fornecido existe
    cadastro = session.query(CadastroAssociacao).filter_by(cod_assoc=valid_data.cod_assoc).one()
  except NoResultFound:
    logger.warning(f"Cadastro com cod_assoc={valid_data.cod_assoc} não encontrado.")
    return jsonify({"message": "Cadastro associado não encontrado"}), 404
  
  try:
    # Cria uma nova instância de FormularioComunidade
    novo_formulario = FormularioComunidade(
      cod_assoc=valid_data.cod_assoc,
      pergunta=valid_data.pergunta,
      resposta=valid_data.resposta
    )
    session.add(novo_formulario)
    session.commit()
    logger.info(f"Formulário criado com sucesso para cadastro cod_assoc={valid_data.cod_assoc}")
    return jsonify(schema.dump(novo_formulario)), 201
  except Exception as e:
    session.rollback()
    logger.error(f"Erro ao criar formulário: {str(e)}", exc_info=True)
    return jsonify({"message": "Erro ao processar sua requisição"}), 500
  finally:
    session.close()

@app.route('/cadastros/<int:cod_assoc>', methods=['GET'])
def get_cadastro(cod_assoc):
  logger.info(f"Busca pelo cadastro com cod_assoc={cod_assoc} iniciada.")  # Log inicial
  session = Session()
  try:
    # Adicionando joinedload para carregar os formulários relacionados
    cadastro = session.query(CadastroAssociacao).options(joinedload(CadastroAssociacao.formularios)).filter_by(cod_assoc=cod_assoc).first()
    if not cadastro:
        logger.warning(f"Cadastro com cod_assoc={cod_assoc} não encontrado.")  # Log caso não encontre o cadastro
        return jsonify({"message": "Cadastro não encontrado"}), 404
    schema = CadastroAssociacaoSchema()
    result = schema.dump(cadastro)
    logger.info(f"Cadastro com cod_assoc={cod_assoc} encontrado e retornado com sucesso.")  # Log sucesso
    return jsonify(result), 200
  except Exception as e:
    logger.error(f"Erro ao buscar cadastro com cod_assoc={cod_assoc}: {str(e)}", exc_info=True)  # Log de erros
    return jsonify({"message": "Erro ao processar sua requisição"}), 500
  finally:
      session.close()  # Garantindo que a sessão seja fechada após a operação

@app.route('/cadastros', methods=['GET'])
def get_cadastros():
  nome_assoc = request.args.get('nome_assoc', default=None)
  page = request.args.get('page', default=1, type=int)
  per_page = request.args.get('per_page', default=10, type=int)

  logger.info(f"Busca por cadastros com nome similar a '{nome_assoc}' iniciada.")

  session = Session()

  try:
    query = session.query(CadastroAssociacao).options(joinedload(CadastroAssociacao.formularios))

    if nome_assoc:
      query = query.filter(func.lower(CadastroAssociacao.nome_assoc).like('%' + nome_assoc.lower() + '%'))

    # Aplicando paginação manualmente
    total = query.count()
    cadastros = query.offset((page - 1) * per_page).limit(per_page).all()

    if not cadastros:
      logger.info("Nenhum cadastro encontrado para os critérios fornecidos.")
      return jsonify({"message": "Nenhum cadastro encontrado"}), 404
    
    schema = CadastroAssociacaoSchema(many=True)
    result = schema.dump(cadastros)
    logger.info(f"{len(cadastros)} cadastros encontrados.")

    return jsonify({
      'cadastros': result,
      'total': total,
      'pages': (total + per_page - 1) // per_page,
      'current_page': page
    }), 200
  except Exception as e:
    logger.error(f"Erro ao buscar cadastros: {str(e)}", exc_info=True)
    return jsonify({"message": "Erro ao processar sua requisição"}), 500
  finally:
    session.close()

@app.route('/cadastro/<nome_assoc>', methods=['DELETE'])
def delete_cadastro(nome_assoc):
  session = Session()
  try:
    # Encontra o cadastro pelo nome_assoc
    cadastro = session.query(CadastroAssociacao).filter_by(nome_assoc=nome_assoc).first()
    if not cadastro:
      logger.warning(f"Cadastro com nome_assoc='{nome_assoc}' não encontrado.")
      return jsonify({"message": "Cadastro não encontrado"}), 404
    
    # Remove o cadastro e suas dependências
    session.delete(cadastro)
    session.commit()
    logger.info(f"Cadastro com nome_assoc='{nome_assoc}' e suas dependências foram removidos com sucesso.")
    return jsonify({"message": "Cadastro deletado com sucesso"}), 200
  except Exception as e:
    session.rollback()
    logger.error(f"Erro ao deletar cadastro: {str(e)}", exc_info=True)
    return jsonify({"message": "Erro ao processar sua requisição"}), 500
  finally:
    session.close()

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000)
     