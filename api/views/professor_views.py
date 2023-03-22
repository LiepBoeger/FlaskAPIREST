from flask_restful import Resource
from api import api
from ..schemas import professor_schema
from flask import request, make_response, jsonify
from ..entities import professor
from ..services import professor_service
from ..paginate import paginate
from ..models.professor_model import Professor
from flask_jwt_extended import jwt_required

class ProfessorList(Resource):

    @jwt_required()
    def get(self):
        ps = professor_schema.ProfessorSchema(many=True)
        return paginate(Professor, ps)

    @jwt_required()
    def post(self):
        ps = professor_schema.ProfessorSchema()
        validate = ps.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            idade = request.json['idade']

            novo_professor = professor.Professor(nome=nome, idade=idade)
            resultado = professor_service.cadastrar_professor(novo_professor)
            x = ps.jsonify(resultado)
            return make_response(x, 201)

class ProfessorDetail(Resource):

    @jwt_required()
    def get(self, id):
        professor = professor_service.listar_professor_id(id)
        if professor is None:
            return make_response(jsonify('Professor não encontrado'), 404)
        ps = professor_schema.ProfessorSchema()
        return make_response(ps.jsonify(professor), 200)

    @jwt_required()
    def put(self, id):
        professor_db = professor_service.listar_professor_id(id)
        if professor_db is None:
            return make_response(jsonify('Professor não encontrado'), 404)
        ps = professor_schema.ProfessorSchema()
        validate = ps.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            idade = request.json['idade']
            novo_professor = professor.Professor(nome=nome, idade=idade)
            professor_service.atualiza_professor(professor_db, novo_professor)
            professor_atualizado = professor_service.listar_professor_id(id)
            return make_response(ps.jsonify(professor_atualizado), 200)

    @jwt_required()
    def delete(self, id):
        professor_db = professor_service.listar_professor_id(id)
        if professor_db is None:
            return make_response(jsonify('Professor não encontrado'), 404)
        professor_service.remove_professor(professor_db)
        return make_response('Professor excluído com sucesso!', 204)


api.add_resource(ProfessorList, '/professores')
api.add_resource(ProfessorDetail, '/professores/<int:id>')