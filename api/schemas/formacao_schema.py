from api import ma
from ..models import formacao_model
from marshmallow import fields
from ..schemas import curso_schema, professor_schema

class FormacaoSchema(ma.SQLAlchemyAutoSchema):
    professores = ma.Nested(professor_schema.ProfessorSchema, many=True, only=('id', 'nome'))
    class Meta:
        model = formacao_model.Formacao
        load_instance = True
        fields = ("id", "nome", "descricao", "cursos", "professores", "_links")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    cursos = fields.List(fields.Nested(curso_schema.CursoSchema, only=('id', 'nome')))

    _links = ma.Hyperlinks(
        {
            "get":ma.URLFor("formacaodetail", id="<id>"),
            "put": ma.URLFor("formacaodetail", id="<id>"),
            "delete": ma.URLFor("formacaodetail", id="<id>")
        }
    )