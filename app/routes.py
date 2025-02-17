from flask import redirect, render_template, request, send_file, url_for
from app import app
from app.database_sqlite import DatabaseSqlite
from app.modelo import ProcessarModelo
import os

@app.route('/')
@app.route('/index')
def index():
    db = DatabaseSqlite()
    db.create_database()
    return render_template('index/index.html', curriculos=DatabaseSqlite().get_curriculos())

@app.route('/new-form', methods=['GET', 'POST'])
def form():
    #
    #if request.method == 'POST':

    #    return render_template('formulario/form.html')
    return render_template('formulario/form.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    print(request.form)  # Verifique os dados recebidos no terminal
    
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    objetivo = request.form['objetivo']

    cursos = request.form.getlist('curso[]')
    instituicoes = request.form.getlist('instituicao[]')
    anos = request.form.getlist('ano[]')
    status = request.form.getlist('status[]')
    perfil = request.form['perfil']

    tempo_inicio = request.form.getlist('tempo_inicio[]')
    tempo_fim = request.form.getlist('tempo_fim[]')
    empresa = request.form.getlist('empresa[]')
    cargo = request.form.getlist('cargo[]')

    db = DatabaseSqlite()
    
    curriculo_id = db.insert_curriculo(nome, endereco, telefone, email, objetivo, perfil)
    
    for i in range(len(cursos)): 
        db.insert_curso(
            instituicoes[i], 
            cursos[i], 
            anos[i], 
            status[i], 
            curriculo_id
        )
    for i in range(len(empresa)):
        db.insert_experiencia(
            tempo_inicio[i],
            tempo_fim[i],
            empresa[i],
            cargo[i],
            curriculo_id
        )
    ProcessarModelo(curriculo_id)

    return redirect(url_for('index')) 

@app.route('/download/<int:id>')
def download_file(id):
    # Cria o caminho do arquivo de forma segura
    filename = os.path.join('curriculo', f'curriculo[{id}].docx')
    
    try:
        # Garante que o arquivo seja enviado com o status adequado
        db = DatabaseSqlite()
        name = db.get_curriculo_by_id(id)
        return send_file(filename, as_attachment=True,  download_name=f"{name[1]}.docx")
    except FileNotFoundError:
        # Retorna uma mensagem personalizada de erro com o código de status 404
        return "Arquivo não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)