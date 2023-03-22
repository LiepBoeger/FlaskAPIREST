from flask_restful import Resource
from api import api
from ..schemas import curso_schema
from flask import request, make_response, jsonify
from ..entities import curso
from ..services import curso_service, formacao_service
from ..paginate import paginate
from ..models.curso_model import Curso
from flask_jwt_extended import jwt_required

class CursoList(Resource):
    @jwt_required()
    def get(self):
        cs = curso_schema.CursoSchema(many=True)
        return paginate(Curso, cs)

    @jwt_required()
    def post(self):
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            descricao = request.json['descricao']
            data_publicacao = request.json['data_publicacao']
            formacao = request.json['formacao']
            formacao_curso = formacao_service.listar_formacao_id(formacao)

            if formacao_curso is None:
                return make_response(jsonify('Formação não encontrada'), 404)

            novo_curso = curso.Curso(nome=nome,
                                     descricao=descricao,
                                     data_publicacao=data_publicacao,
                                     formacao=formacao_curso)
            resultado = curso_service.cadastrar_curso(novo_curso)
            x = cs.jsonify(resultado)
            return make_response(x, 201)

class CursoDetail(Resource):
    @jwt_required()
    def get(self, id):
        curso = curso_service.listar_curso_id(id)
        if curso is None:
            return make_response(jsonify('Curso não foi encontrado'), 404)
        cs = curso_schema.CursoSchema()
        return make_response(cs.jsonify(curso), 200)

    @jwt_required()
    def put(self, id):
        curso_db = curso_service.listar_curso_id(id)
        if curso_db is None:
            return make_response(jsonify('Curso não foi encontrado'), 404)
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            descricao = request.json['descricao']
            data_publicacao = request.json['data_publicacao']
            formacao = request.json['formacao']
            formacao_curso = formacao_service.listar_formacao_id(formacao)

            if formacao_curso is None:
                return make_response(jsonify('Formação não encontrada'), 404)

            novo_curso = curso.Curso(nome=nome,
                                     descricao=descricao,
                                     data_publicacao=data_publicacao,
                                     formacao=formacao_curso)
            curso_service.atualiza_curso(curso_db, novo_curso)
            curso_atualizado = curso_service.listar_curso_id(id)
            return make_response(cs.jsonify(curso_atualizado), 200)

    @jwt_required()
    def delete(self, id):
        curso_db = curso_service.listar_curso_id(id)
        if curso_db is None:
            return make_response(jsonify('Curso não encontrado'), 404)
        curso_service.remove_curso(curso_db)
        return make_response('Curso excluído com sucesso!', 204)


api.add_resource(CursoList, '/cursos')
api.add_resource(CursoDetail, '/cursos/<int:id>')