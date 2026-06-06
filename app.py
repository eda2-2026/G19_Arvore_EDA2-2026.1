import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from arvore import ArvoreVermelhoPreto
from datetime import datetime

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
    nos = clinica_tree.obter_todos()
    pacientes = [{'nome': n.nome_original, 'cpf': n.cpf, 'especialidade': n.especialidade, 'data_consulta': n.data_consulta, 'cor': n.cor} for n in nos]
    arvore_dict = clinica_tree.obter_dicionario()
    return render_template('index.html', pacientes=pacientes, termo_busca="", arvore_dict=arvore_dict)

@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome'].strip()
    cpf = request.form['cpf'].strip()
    especialidade = request.form['especialidade'].strip()
    data_raw = request.form['data_consulta'] 

    try:
        data_obj = datetime.strptime(data_raw, '%Y-%m-%dT%H:%M')
        data_consulta = data_obj.strftime('%d/%m/%Y %H:%M')
    except ValueError:
        data_consulta = data_raw 

    clinica_tree.inserir(nome, especialidade, data_consulta, cpf)
    salvar_dados()
    
    flash(f'Consulta agendada com sucesso para {nome}!', 'success')
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET'])
def buscar():
    nome_busca = request.args.get('nome', '').strip()
    
    if not nome_busca:
        return redirect(url_for('index'))

    resultados = clinica_tree.buscar_parcial(nome_busca)
    
    if len(resultados) == 0:
        flash(f'Nenhum paciente encontrado para "{nome_busca}".', 'error')
        pacientes = []
    else:
        pacientes = [{'nome': n.nome_original, 'cpf': n.cpf, 'especialidade': n.especialidade, 'data_consulta': n.data_consulta, 'cor': n.cor} for n in resultados]

    return render_template('index.html', pacientes=pacientes, termo_busca=nome_busca)

@app.route('/cancelar', methods=['POST'])
def cancelar():
    nome_cancelar = request.form['nome'].strip()
    sucesso = clinica_tree.remover(nome_cancelar)
    
    if sucesso:
        salvar_dados()
        flash(f'Consulta de "{nome_cancelar}" removida com sucesso.', 'success')
    else:
        flash(f'Erro ao remover.', 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)