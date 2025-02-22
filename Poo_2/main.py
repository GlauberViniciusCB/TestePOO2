#Iniciar servidor uvicorn main:app --reload

import mysql.connector
from mysql.connector import Error
from db import conexaoComBanco
import logging
from fastapi.responses import RedirectResponse
from fastapi import FastAPI,Form,HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from pydantic import BaseModel
from datetime import date, time
from datetime import datetime
from datetime import timedelta



app = FastAPI()



class Veterinario(BaseModel):
    nome: str
    email: str
    senha: str



# Função para inserir o veterinário no banco de dados
def inserir_veterinario(nome, email, senha):
    try:
        # Conectando ao banco de dados
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            query = "INSERT INTO Veterinario (nome, email, senha) VALUES (%s, %s, %s)"
            dados = (nome, email, senha)
            cursor.execute(query, dados)
            
            # Confirmar a transação
            conexao.commit()
            print("Veterinário inserido com sucesso!")
        else:
            print("Erro na conexão com o banco de dados.")
    except Error as e:
        print(f"Erro ao inserir veterinário: {e}")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Rota para registrar o veterinário (esperando JSON)
@app.post("/registrarVeterinario")
async def registrar_veterinario(veterinario: Veterinario):
    try:
        nome = veterinario.nome
        email = veterinario.email
        senha = veterinario.senha
        
        # Validando a senha
        if len(senha) < 4:
            raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 4 caracteres.")
        
        # Inserir o veterinário no banco de dados
        inserir_veterinario(nome, email, senha)
        return {"message": "Veterinário registrado com sucesso!"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Erro ao registrar veterinário: {e}")
        raise HTTPException(status_code=500, detail="Erro no servidor ao registrar veterinário")


# Rota para login (esperando JSON)


class LoginData(BaseModel):
    email: str
    senha: str

@app.post("/loginVeterinario")
async def login_veterinario(login_data: LoginData):
    try:
        email = login_data.email
        senha = login_data.senha
        
        # Conexão com o banco de dados e validação
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Veterinario WHERE email = %s AND senha = %s", (email, senha))
        veterinario = cursor.fetchone()

        if not veterinario:
            raise HTTPException(status_code=400, detail="Credenciais inválidas.")

        nome_veterinario = veterinario[0]
        return {"message": "Login bem-sucedido!", "nome": nome_veterinario}

    except Exception as e:
        logging.error(f"Erro ao realizar login: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro no servidor")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()


def inserirCliente(nome,endereco,telefone,email):
    try:
        conexao =mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            query ="INSERT INTO Cliente (nome,endereco,telefone,email) VALUES (%s,%s,%s,%s)" 
            dados = (nome,endereco,telefone,email)
            cursor.execute(query,dados)
            conexao.commit()
            print("Cliente Inserindo Com Sucesso!")
        else:
            print("Erro Na Conexão Com O Banco De Dados.")
    except Error as e:
        print(f"Erro Ao Inserir Cliente: {e}")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def inserirPaciente(tutor,nome,especie,raca,idade,sexo):
    try:
        conexao =mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            query ="INSERT INTO Animal (id_cliente,nome_animal,especie,raca,idade,sexo) VALUES (%s,%s,%s,%s,%s,%s)" 
            dados = (tutor,nome,especie,raca,idade,sexo)
            cursor.execute(query,dados)
            conexao.commit()
            print("Paciente Inserindo Com Sucesso!")
        else:
            print("Erro Na Conexão Com O Banco De Dados.")
    except Error as e:
        print(f"Erro Ao Inserir Paciente: {e}")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()




templates = Jinja2Templates(directory="templates") 

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html",{"request": request})

def get_db():
    db = conexaoComBanco()
    if db is None:
        raise HTTPException(status_code= 500, detail="Erro ao conectar com o banco de dados")
    return db



# rotas para cliente 

class Cliente(BaseModel):
    nome: str
    email: str
    endereco: str
    telefone: str

@app.post("/registrarCliente")
async def registrar_cliente(cliente: Cliente):
    try:
        
        inserirCliente(cliente.nome, cliente.endereco, cliente.telefone, cliente.email)
        return {"message": "Cliente Registrado Com Sucesso!"}
    except Exception as e:
        logging.error(f"Erro ao Registrar Cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro no Servidor")
    
@app.get("/clientes")
async def obterClientes(db: mysql.connector.connect = Depends(get_db)):
    try: 
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        return{"clientes":clientes}
    except Exception as e:
        logging.error(f"Erro Ao Obter Clientes {e}")
        raise HTTPException(status_code= 500, detail="Erro Ao Obter Clientes")
    finally:
        cursor.close()


 #rotas para paciente

class Paciente(BaseModel):
    tutor: int 
    nome: str
    especie : str 
    raca : str 
    idade : int 
    sexo : str 

@app.post("/registrarPaciente")
async def registrar_paciente(paciente: Paciente):
    try:
        inserirPaciente(paciente.tutor,paciente.nome, paciente.especie, paciente.raca,paciente.idade, paciente.sexo)
        return{"message": "Paciente Registrado Com Sucesso!"}
    except Exception as e:
        logging.error(f'Erro ao Registrar Pacienete: {e}')
        raise HTTPException(status_code=500, detail="Erro no servidor")
    

@app.get("/listarPacientes")
async def listar_Pacientes(db: mysql.connector.connect = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id_animal, nome_animal FROM Animal")
        pacientes = cursor.fetchall()
        
        # Retornando os dados no formato correto
        return {"pacientes": [{"id_animal": nome[0], "nome": nome[1]} for nome in pacientes]}
        
    except Exception as e:
        logging.error(f"Erro Ao Obter Pacientes: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter pacientes")
    finally:
        cursor.close()

@app.get("/pacientes")
async def obterPacientes(db: mysql.connector.connect = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Animal")
        pacientes = cursor.fetchall()
        return {"pacientes": pacientes}
    except Exception as e:
        logging.error(f'Erro ao Obter Paciente: {e}')
        raise HTTPException(status_code=500, detail="Erro ao Obter Pacientes")
    finally:
        cursor.close()

@app.get("/tutores")
async def obter_tutores(db: mysql.connector.connect = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id_cliente, nome FROM Cliente")
        tutores = cursor.fetchall()
        return {"tutores": [{"id_cliente": tutor[0], "nome": tutor[1]} for tutor in tutores]}
    except Exception as e:
        logging.error(f"Erro ao Obter Tutores: {e}")
        raise HTTPException(status_code=500, detail="Erro ao Obter Tutores")
    finally:
        cursor.close()


class Consulta(BaseModel):
    animal: int 
    veterinario : int 
    data : date
    hora : time 
    status: str


def inserir_consulta(animal, veterinario, data, hora, status):
    conexao = None  # Inicializando como None para garantir que não haja acesso a uma variável não atribuída
    cursor = None    # Inicializando como None também

    try:
        print(f"Recebido dados para inserir: animal={animal}, veterinario={veterinario}, data={data}, hora={hora}, status={status}")
        
        # Verificando se 'data' já é um objeto datetime.date
        if isinstance(data, str):  # Se for uma string, converta para datetime.date
            data_formatada = datetime.strptime(data, "%Y-%m-%d").date()  # Transformando para 'DATE'
        else:
            data_formatada = data  # Caso 'data' já seja do tipo datetime.date, apenas atribui
        
        print(f"Data formatada: {data_formatada}")
        
        # Verificando se 'hora' já é um objeto datetime.time
        if isinstance(hora, str):  # Se for uma string, converta para datetime.time
            hora_formatada = datetime.strptime(hora, "%H:%M").time()  # Corrigido para hora sem segundos
        else:
            hora_formatada = hora  # Caso 'hora' já seja do tipo datetime.time, apenas atribui
        
        print(f"Hora formatada: {hora_formatada}")
        
        # Criando a conexão com o banco de dados
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        
        # Verificando se a conexão foi bem-sucedida
        if conexao.is_connected():
            cursor = conexao.cursor()
            query = """
                INSERT INTO CONSULTA (id_animal, id_veterinario, data_consulta, hora_consulta, status_consulta) 
                VALUES (%s, %s, %s, %s, %s)
            """
            dados = (animal, veterinario, data_formatada, hora_formatada, status)
            
            # Executando a consulta
            cursor.execute(query, dados)
            conexao.commit()
            print("Consulta Inserida Com Sucesso!")
        else:
            print("Erro na Conexão Com o Banco de Dados.")
    
    except Error as e:
        print(f"Erro Ao Inserir Consulta: {e}")  # Exibe a mensagem de erro detalhada
        raise Exception(f"Erro ao inserir consulta: {e}")
    
    finally:
        # Verificando se a conexão e o cursor foram criados antes de fechar
        if conexao and conexao.is_connected():
            if cursor:
                cursor.close()
            conexao.close()



@app.post("/registrarConsulta")
async def registrar_consulta(consulta: Consulta):
    try:
        inserir_consulta(consulta.animal, consulta.veterinario, consulta.data, consulta.hora, consulta.status)
        return {"message": "Consulta Registrada Com Sucesso!"}
    except Exception as e : 
        logging.error(f"Erro ao Registrar COnsulta: {e}")
        raise HTTPException (status_code = 500, detail= "Erro  no Servidor" )


@app.get("/listarVeterinarios")
async def listar_Veterinarios(db: mysql.connector.connect = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id_veterinario, nome FROM Veterinario")
        veterinarios = cursor.fetchall()

        # Corrigindo o retorno
        return {"veterinarios": [{"id_veterinario": veterinario[0], "nome": veterinario[1]} for veterinario in veterinarios]}
    except Exception as e:
        logging.error(f"Erro ao obter Veterinário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao Obter Veterinário")
    finally:
        cursor.close()


# teste 

def format_time(hora):
    if isinstance(hora, timedelta):  # Caso seja um timedelta
        total_seconds = int(hora.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02}:{minutes:02}:00"
    elif isinstance(hora, datetime.time):  # Caso seja um objeto datetime.time
        return hora.strftime("%H:%M:%S")
    return "00:00:00"  # Valor padrão caso o tipo de dado seja inesperado

@app.get("/consultas")
async def listar_consultas():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        cursor = conexao.cursor()

        
        query = """
        SELECT 
            c.id_consulta, 
            a.nome_animal AS nome_animal, 
            v.nome AS nome_veterinario, 
            c.data_consulta, 
            c.hora_consulta, 
            c.status_consulta
        FROM 
            Consulta c
        JOIN 
            Animal a ON c.id_animal = a.id_animal
        JOIN 
            Veterinario v ON c.id_veterinario = v.id_veterinario
        """
        cursor.execute(query)
        consultas = cursor.fetchall()

        
        consultas_formatadas = [
            {
                "id_consulta": consulta[0],
                "nome_animal": consulta[1],
                "nome_veterinario": consulta[2],
                "data_consulta": consulta[3].strftime("%Y-%m-%d"),  # Formatação para string
                "hora_consulta": format_time(consulta[4]),  # Usando a função format_time para formatar a hora
                "status_consulta": consulta[5]
            }
            for consulta in consultas
        ]
        return {"consultas": consultas_formatadas}
    
    except mysql.connector.Error as e:
        print(f"Erro ao listar consultas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados.")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
