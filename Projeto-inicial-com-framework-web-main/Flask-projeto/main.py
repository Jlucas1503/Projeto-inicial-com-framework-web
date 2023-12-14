from flask import Flask, render_template, request
import mysql.connector
import base64

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "labhugo",
    database = "pokemon"
)
cursor = banco.cursor()

app = Flask(__name__)

@app.route('/home') #Página Principal do site
def home():
    cursor.execute("SELECT nome, imagem FROM pokemon ORDER BY codigo DESC LIMIT 5;")
    resultados = cursor.fetchall()

    dados_pokemon = []
    for linha in resultados:
        nome_pokemon = linha[0]
        imagem_pokemon = linha[1]
        imagem_base64 = base64.b64encode(imagem_pokemon).decode('utf-8')

        dados_pokemon.append(nome_pokemon)
        dados_pokemon.append(imagem_base64)

    return render_template("principal.html", nome1=dados_pokemon[0], foto1=dados_pokemon[1], nome2=dados_pokemon[2], foto2=dados_pokemon[3], nome3=dados_pokemon[4], foto3=dados_pokemon[5], nome4=dados_pokemon[6], foto4=dados_pokemon[7], nome5=dados_pokemon[8], foto5=dados_pokemon[9])

@app.route('/cadastro', methods=['GET', 'POST']) #Cadastro de usuários do site
def cadastro():
    if request.method == 'POST':
        email = request.form['mail']
        nome = request.form['nome']
        senha = request.form['senha']
        nascimento = request.form['nascimento']

        cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}';")
        linha = cursor.fetchone()

        if linha is not None: #Caso já exista um valor com o mesmo e-mail
            return render_template("negativa1.html", mensagem="Parece que já existe um usuário com essas credenciais. Confira seus dados e tente novamente!")
        else:
            cursor.execute(f"INSERT INTO usuario VALUES (%s, %s, %s, %s);", (email, nome, nascimento, senha))
            banco.commit()
            return render_template("positiva1.html", mensagem="Obrigado por se cadastrar na plataforma! Sinta-se a vontade para explorar nossos pokemons cadastrados e cadastrar um pokemon também.")    
    else:
        return render_template("cadastrar.html")

@app.route('/dados', methods=['GET', 'POST']) #Exibição dos dados dos usuários do site
def dados():
    if request.method == 'POST':
        mail_pesquisa = request.form['mail_pesquisa']
        cursor.execute(f"SELECT nome, email, nascimento FROM usuario WHERE email = '{mail_pesquisa}';")

        linha = cursor.fetchone()
    
        if linha:
            nomeee = linha[0]
            mailll = linha[1]
            nascimentooo = linha[2]
        else:
            nomeee = ""
            mailll = ""
            nascimentooo = ""    
        return render_template("exibicao.html", nome2=nomeee, mail2=mailll, nascimento2=nascimentooo)
    else:
        return render_template("exibicao.html", nome2="", mail2="", nascimento2="")

@app.route('/atualizar', methods=['GET', 'POST']) #Página de atualização de senhas de usuários do site
def atualizar():
    if request.method == 'POST':
        email_atualizar = request.form['mail']
        senha_atual = request.form['senha_atual']
        senha_nova = request.form['nova_senha']

        cursor.execute(f"SELECT senha FROM usuario WHERE email = '{email_atualizar}';")

        linha = cursor.fetchone()

        if linha is not None: #Caso o usuário com o devido e-mail já exista
            if linha[0] == senha_atual:
                cursor.execute(f"UPDATE usuario SET senha = %s WHERE email = %s;", (senha_nova, email_atualizar))
                banco.commit()
                return render_template("positiva1.html", mensagem="Você acabou de atualizar sua senha! Continue explorando nossa plataforma e divirta-se.")
            else:
                return render_template("negativa1.html", mensagem="Parece que sua senha está incorreta. Confira seus dados e tente novamente!")
        else:
            return render_template("negativa1.html", mensagem="Parece que não existe um usuário com essas credenciais. Confira seus dados e tente novamente!")
    else:
        return render_template("atualizacao.html")
    
temp_nome = None
temp_tipo = None
temp_raridade = None
temp_foto = None
    
@app.route('/inserir', methods=['GET', 'POST']) #Página onde o usuário pode inserir um pokemon
def inserir():
    global temp_nome, temp_tipo, temp_raridade, temp_foto

    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        raridade = request.form['raridade']
        foto = request.files['imagem']

        imagem = foto.read() #Converter a imagem em binário

        cursor.execute(f"SELECT * FROM pokemon WHERE nome = '{nome}';")
        linha = cursor.fetchone()

        if linha is not None: #Caso o pokemom com as caracteristicas acima já exista
            return render_template("negativa1.html", mensagem="Parece que já existe um pokemon com essas características. Confira seus dados e tente novamente!")
        else:
            temp_nome = nome
            temp_tipo = tipo
            temp_raridade = raridade
            temp_foto = imagem
            return render_template("validacao.html")
    else:
        return render_template("inserir.html")
    
@app.route('/validar', methods=['GET', 'POST']) #Página de confirmação de dados
def validar_dados():
    global temp_nome, temp_tipo, temp_raridade, temp_foto

    if request.method == 'POST':
        mail_pesquisa = request.form['mail']
        senha_pesquisa = request.form['senha']

        nome = temp_nome
        tipo = temp_tipo
        raridade = temp_raridade
        imagem = temp_foto

        cursor.execute(f"SELECT email, senha FROM usuario WHERE email = '{mail_pesquisa}';")

        linha = cursor.fetchone()

        if linha is not None: #Caso o usuário com o devido e-mail já exista
            senha = linha[1]
            if (senha_pesquisa == senha):
                cursor.execute(f"INSERT INTO pokemon(nome, tipo, raridade, imagem) VALUES (%s, %s, %s, %s);", (nome, tipo, raridade, imagem))
                cursor.execute(f"SELECT codigo FROM pokemon WHERE nome = '{nome}';")
                linha = cursor.fetchone()
                cod = linha[0]
                cursor.execute(f"INSERT INTO cadastra VALUES (%s, %s);", (cod, mail_pesquisa))
                banco.commit()
                return render_template("positiva1.html", mensagem="Obrigado por nos mostrar outro pokemon! Sinta-se a vontade para explorar nossos pokemons cadastrados e cadastrar outro pokemon também.")
            else:
                return render_template("negativa1.html", mensagem="Parece que sua senha está incorreta. Confira seus dados e tente novamente!")
        else:
            return render_template("negativa1.html", mensagem="Parece que não existe um usuário com essas credenciais. Confira seus dados e tente novamente!")
    else:
        return render_template("validacao.html")
    
@app.route('/pokemons/', methods=['GET', 'POST']) #Página onde o usuário pode verificar os pokemos existentes no site
def mostrar_pokemon():
    if request.method == 'POST':
        nomepokemon = request.form['search']
        cursor.execute(f"SELECT nome, tipo, raridade, imagem FROM pokemon WHERE nome = '{nomepokemon}';")

        linha = cursor.fetchone()

        if linha:
            nomepoke = linha[0]
            tipopoke = linha[1]
            raridadepoke = linha[2]
            fotopoke = linha[3]
            fotopoke2 = base64.b64encode(fotopoke).decode('utf-8') #Converter os dados binários em uma imagem

            return render_template("mostrarpokemon.html", nome2=nomepoke, tipo2=tipopoke, raridade2=raridadepoke, foto2 = fotopoke2)
        else:
            return render_template("negativa1.html", mensagem="Parece que não existe um pokemon com essas características. Confira seus dados e tente novamente!")
    else:
        return render_template("mostrarpokemon.html", nome2="", tipo2="", raridade2="", foto2="")
    
@app.route('/pokemon/<nome>', methods=['GET']) #Página onde serão exibidas as informações dos cards
def mostrar_pokemons(nome):
    cursor.execute(f"SELECT nome, tipo, raridade, imagem FROM pokemon WHERE nome = '{nome}';")

    linha = cursor.fetchone()

    if linha:
        nomepoke = linha[0]
        tipopoke = linha[1]
        raridadepoke = linha[2]
        fotopoke = linha[3]
        fotopoke2 = base64.b64encode(fotopoke).decode('utf-8') #Converter os dados binários em uma imagem

        return render_template("mostrarpokemon.html", nome2=nomepoke, tipo2=tipopoke, raridade2=raridadepoke, foto2 = fotopoke2)
    else:
        return render_template("negativa1.html", mensagem="Parece que não existe um pokemon com essas características. Confira seus dados e tente novamente!")
    
if __name__ == "__main__":
    app.run(debug=True)