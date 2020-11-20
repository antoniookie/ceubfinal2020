import mysql.connector
from veiculos import base
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')
@app.route('/formincluir')
def formincluir():
    return render_template('formincluir.html')
@app.route('/incluir', methods=['POST'])
def incluir():
    modelo = request.form['modelo']
    placa = request.form['placa']
    cilindrada = float(request.form['cilindrada'])
    cor = request.form['cor']
    valor = float(request.form['valor'])

    mysql = base.SQL('root', 'antonio09')
    comando = '''INSERT INTO tb_veiculos(modelo_veiculos, placa_veiculo, cilin_veiculos, cor_veiculos, valor_veiculos) values
     (%s, %s, %s, %s, %s);'''
    if mysql.executar(comando, [modelo, placa, cilindrada, cor, valor]):
        msg = 'Inserido veiculo ' + modelo + ' com sucesso.'
    else:
        msg = 'Falha na inclusao...'
    return render_template('incluir.html', msg=msg)

@app.route('/parconsultar')
def parconsultar():
    mysql = base.SQL('root', 'antonio09')
    comando = '''SELECT DISTINCT modelo_veiculos from tb_veiculos order by modelo_veiculos;'''
    cs = mysql.consultar(comando, ())
    sel = "<SELECT NAME='modelo'>"
    sel += "<OPTION>Todos</OPTION>"
    for [modelo] in cs:
        sel += "<OPTION>" + modelo + "</OPTION>"
    sel += "</SELECT>"
    cs.close()

    comando = "SELECT MIN(valor_veiculos) as menor, MAX(valor_veiculos) as maior from tb_veiculos;"
    cs = mysql.consultar(comando, ())
    dados = cs.fetchone()
    menor = dados[0]
    maior = dados[1]
    return render_template('parconsultar.html', modelo=sel, menor=menor, maior=maior)

@app.route('/consultar', methods=['POST'])
def consultar():
    modelo = request.form['modelo']
    menor = float(request.form['ini'])
    maior = float(request.form['fim'])
    modelo = "" if modelo=="Todos" else modelo

    mysql = base.SQL('root', 'antonio09')
    comando = '''SELECT * FROM tb_veiculos where modelo_veiculos like concat ('%', %s, '%') and valor_veiculos 
    between %s and %s order by valor_veiculos;'''

    cs = mysql.consultar(comando, [modelo, menor, maior])
    modelos = ""
    for [idt, modelo ,placa, cilindrada, cor, valor] in cs:
        modelos += '<TR>'
        modelos += '<TD>' + modelo + '</TD>'
        modelos += '<TD>' + placa + '</TD>'
        modelos += '<TD>' + str(cilindrada) + '</TD>'
        modelos += '<TD>' + cor + '</TD>'
        modelos += '<TD>' + str(valor) + '</TD>'
        modelos += '</TR>'
    cs.close()
    return render_template('consultar.html', modelos=modelos)

@app.route('/paralterar')
def paralterar():
    return render_template('paralterar.html')
@app.route('/formalterar', methods=['POST'])
def formalterar():
    placa = request.form['placa']
    mysql = base.SQL('root', 'antonio09')
    comando = '''SELECT * FROM tb_veiculos where placa_veiculo=%s;'''
    cs = mysql.consultar(comando, [placa])
    dados = cs.fetchone()
    cs.close()
    if dados == None:
        return render_template('naoencontrado.html')
    else:
        return render_template('formalterar.html', idt=dados[0], modelo=dados[1], placa=dados[2], cilindrada=dados[3], cor=dados[4], valor=dados[5])
@app.route('/alterar', methods=['POST'])
def alterar():
    idt = int(request.form['idt'])
    modelo = request.form['modelo']
    placa = request.form['placa']
    cilindrada = float(request.form['cilindrada'])
    cor = request.form['cor']
    valor = float(request.form['valor'])
    mysql = base.SQL('root', 'antonio09')
    comando = '''UPDATE tb_veiculos SET modelo_veiculos=%s, placa_veiculo=%s, cilin_veiculos=%s, cor_veiculos=%s,
    valor_veiculos=%s, where idt_veiculos=%s;'''
    if mysql.executar(comando, [idt, modelo, placa, cilindrada, cor, valor]):
        msg = "Veiculo " + modelo + " alterado com sucesso..."
    else:
        msg = "Falha na alteracao do veiculo..."
    return render_template('alterar.html', msg=msg)
