from flask import Flask, render_template, request, redirect, url_for, flash
from arvore import ArvoreVermelhoPreto

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flash_messages'
clinica_tree = ArvoreVermelhoPreto()

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():

    try:
        matricula = int(request.form['matricula'])
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        data_consulta = request.form['data_consulta']

        clinica_tree.inserir(matricula, nome, especialidade, data_consulta)

        flash(f'Consulta agendada com sucesso para a matrícula {matricula}!', 'success')
    except ValueError:
        flash('Erro: A matrícula deve ser um número inteiro.', 'error')
        
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET'])
def buscar():
    matricula_str = request.args.get('matricula')
    
    if not matricula_str:
        return redirect(url_for('index'))
        
    try:
        matricula = int(matricula_str)
        resultado = clinica_tree.buscar(matricula)

        if resultado == clinica_tree.NIL:
            flash(f'Paciente com matrícula {matricula} não encontrado.', 'error')
            paciente = None
        else:

            paciente = {
                'matricula': resultado.matricula,
                'nome': resultado.nome,
                'especialidade': resultado.especialidade,
                'data_consulta': resultado.data_consulta,
                'cor_do_no': resultado.cor 
            }
            flash('Paciente encontrado!', 'success')
            
    except ValueError:
        flash('Erro: A matrícula deve ser um número inteiro.', 'error')
        paciente = None

    return render_template('index.html', paciente=paciente)

@app.route('/debug')
def debug_tree():

    def in_order(no, lista):
        if no != clinica_tree.NIL:
            in_order(no.esq, lista)
            lista.append({
                'matricula': no.matricula,
                'nome': no.nome,
                'cor': no.cor,
                'pai': no.pai.matricula if no.pai != clinica_tree.NIL else "RAIZ"
            })
            in_order(no.dir, lista)
    
    nos = []
    in_order(clinica_tree.raiz, nos)
    return {'estado_da_arvore': nos}

@app.route('/cancelar', methods=['POST'])
def cancelar():
    try:
        matricula = int(request.form['matricula'])
        sucesso = clinica_tree.remover(matricula)
        
        if sucesso:
            flash(f'Consulta da matrícula {matricula} cancelada com sucesso (removida da árvore).', 'success')
        else:
            flash(f'Erro: Matrícula {matricula} não encontrada.', 'error')
            
    except ValueError:
        flash('Erro: A matrícula deve ser um número inteiro.', 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)