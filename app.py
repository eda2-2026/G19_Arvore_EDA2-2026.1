import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from arvore import ArvoreVermelhoPreto

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flash_messages'

ARQUIVO_JSON = 'dados.json'
clinica_tree = ArvoreVermelhoPreto()

def carregar_dados():

    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as file:
            try:
                pacientes = json.load(file)
                for p in pacientes:
                    clinica_tree.inserir(p['nome'], p['especialidade'], p['data_consulta'], p['cpf'])
            except json.JSONDecodeError:
                pass

def salvar_dados():

    pacientes_para_salvar = []
    
    def in_order(no):
        if no != clinica_tree.NIL:
            in_order(no.esq)

            pacientes_para_salvar.append({
                'nome': no.nome_original,
                'cpf': no.cpf,
                'especialidade': no.especialidade,
                'data_consulta': no.data_consulta
            })
            in_order(no.dir)
            
    in_order(clinica_tree.raiz)

    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as file:
        json.dump(pacientes_para_salvar, file, ensure_ascii=False, indent=4)

carregar_dados()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome'].strip()
    cpf = request.form['cpf'].strip()
    especialidade = request.form['especialidade'].strip()
    data_consulta = request.form['data_consulta']

    clinica_tree.inserir(nome, especialidade, data_consulta, cpf)
    salvar_dados()
    
    flash(f'Consulta agendada com sucesso para {nome} (CPF: {cpf})!', 'success')
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET'])
def buscar():
    nome_busca = request.args.get('nome')
    
    if not nome_busca:
        return redirect(url_for('index'))
        
    resultado = clinica_tree.buscar(nome_busca)
    
    if resultado == clinica_tree.NIL:
        flash(f'Paciente "{nome_busca}" não encontrado.', 'error')
        paciente = None
    else:
        paciente = {
            'nome': resultado.nome_original,
            'cpf': resultado.cpf,
            'especialidade': resultado.especialidade,
            'data_consulta': resultado.data_consulta,
            'cor_do_no': resultado.cor
        }
        flash('Paciente encontrado!', 'success')

    return render_template('index.html', paciente=paciente)

@app.route('/cancelar', methods=['POST'])
def cancelar():
    nome_cancelar = request.form['nome'].strip()
    sucesso = clinica_tree.remover(nome_cancelar)
    
    if sucesso:
        salvar_dados()
        flash(f'Consulta de "{nome_cancelar}" cancelada com sucesso.', 'success')
    else:
        flash(f'Erro: Paciente "{nome_cancelar}" não encontrado no sistema.', 'error')
        
    return redirect(url_for('index'))

@app.route('/debug')
def debug_tree():
    def in_order(no, lista):
        if no != clinica_tree.NIL:
            in_order(no.esq, lista)
            lista.append({
                'nome': no.nome_original,
                'cpf': no.cpf,
                'cor': no.cor,
                'pai': no.pai.nome_original if no.pai != clinica_tree.NIL else "RAIZ"
            })
            in_order(no.dir, lista)
    
    nos = []
    in_order(clinica_tree.raiz, nos)
    return {'estado_da_arvore_ordenada': nos}

if __name__ == '__main__':
    app.run(debug=True)