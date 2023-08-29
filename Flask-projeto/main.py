from flask import Flask, render_template

app = Flask(__name__) #representa o arquivo atual

@app.route("/") #representa a página padrão
def home():
    return render_template("principal.html") #Arquivo html dentro da pasta templates

@app.route("/secundaria") 
def secundaria():
    return render_template("segunda.html") 

if __name__ == "__main__": #atribuir o nome main
    app.run(debug=True) #Execução