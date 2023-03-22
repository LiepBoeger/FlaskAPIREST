from ..models import curso_model
from api import db

def cadastrar_curso(curso):
    curso_db = curso_model.Curso(nome=curso.nome, descricao=curso.descricao, data_publicacao=curso.data_publicacao, formacao=curso.formacao)
    db.session.add(curso_db)
    db.session.commit()
    return curso_db

def listar_cursos():
    cursos = curso_model.Curso.query.all()
    return cursos

def listar_curso_id(id):
    curso = curso_model.Curso.query.filter_by(id=id).first()
    return curso

def atualiza_curso(curso_anterior, curso_novo):
    curso_anterior.nome = curso_novo.nome
    curso_anterior.descricao = curso_novo.descricao
    curso_anterior.data_publicacao = curso_novo.data_publicacao
    curso_anterior.formacao = curso_novo.formacao
    db.session.commit()

def remove_curso(curso):
    db.session.delete(curso)
    db.session.commit()