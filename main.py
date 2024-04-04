import datetime
from flask import Flask, Response, json,make_response,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'





db = SQLAlchemy(app)

token = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    
    def __init__(self,username,email,senha):
        username = username
        email=email
        senha= pbkdf2_sha256.hash(senha)
        

    
    

    def to_json_Usuario(self):
        return {"id":self.id,"username":self.username,"email":self.email}

   
class Empregado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    cpf = db.Column(db.String(14))
    data_admissao = db.Column(db.DateTime,default=datetime.datetime)

    def to_json_Empregado(self):
        return {"id":self.id,"nome":self.nome,"cargo":self.cargo, "cpf":self.cpf , "data_admissao":self.data_admissao}




@app.route('/empregados', methods=['GET'])
def get_empregado():
    empregados_objetos = Empregado.query.all()
    empregado_json = [empregado.to_json_Empregado() for empregado in empregados_objetos]
    return Response(json.dumps(empregado_json))
    
    

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json_Usuario() for usuario in usuarios_objetos]
    print(usuarios_json)
    
    return Response(json.dumps(usuarios_json))
    

@app.route('/criar_empregado', methods=['POST'])
def cria_empregado():    
    nome= request.json['nome']
    cargo = request.json['cargo']
    cpf = request.json['cpf']
    data_admissao = request.json['data_admissao']
    token = request.json['token']
   

    try:
        
        empregado = Empregado(nome=nome,cargo=cargo,cpf=cpf, data_admissao=data_admissao)
        if token == token: #apenas usuários com esse token podem criar empregado
            db.session.add(empregado)
            db.session.commit()
            return Response(empregado)
        else:
            return Response('Usuário não autorizado.') #melhor usar validation
    except Exception as e:
        print(e)
        return Response("")
    

@app.route('/criar_usuario', methods=['POST'])
def cria_usuario():
    username = request.json['username']
    email = request.json['email']
    senha = request.json['senha']
    print(username)
    usuario = Usuario(username=username, email=email, senha=senha)
    db.session.add(usuario)
    db.session.commit()
    return Response("foi")

    # try:
        
    # except Exception as e:
    #     print(e)
    #     return Response("não foi")

app.run()