from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Criação do engine de conexão com o banco de dados
engine = create_engine('sqlite:///banco.db')

# Criação da sessão

Session = sessionmaker(bind=engine)

# Criação da classe base para as tabelas do banco de dados
Base = declarative_base()

# Definição da classe Usuario, que representa a tabela "usuario"
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Criação de uma sessão para realizar as operações no banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Inserção de um novo usuário
usuario = Usuario(nome='João', idade=30)
session.add(usuario)
session.commit()

# Consulta de todos os usuários
usuarios = session.query(Usuario).all()
for usuario in usuarios:
    print(usuario.nome, usuario.idade)

# Atualização de um usuário
usuario = session.query(Usuario).filter(Usuario.id == 1).first()
usuario.idade = 35
session.commit()

# Exclusão de um usuário
usuario = session.query(Usuario).filter(Usuario.id == 1).first()
session.delete(usuario)
session.commit()

# Fechamento da sessão
session.close()