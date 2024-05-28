from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/gat')
def gat():
    return render_template("gat.html")

@app.route('/cap')
def cap():
    return render_template("cap.html")

@app.route('/orn')
def orn():
    return render_template("orn.html")

@app.route('/contacto')
def con():
    return render_template("contacto.html")

@app.route('/agrega_comenta', methods=['POST'])
def agrega_comenta():
    if request.method == 'POST':
        aux_Correo = request.form['correo']
        aux_Comentarios = request.form['comentarios']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='operaciones' )
        cursor = conn.cursor()
        cursor.execute('insert into comentarios (correo,comentarios) values (%s, %s)',(aux_Correo, aux_Comentarios))
        conn.commit()
    return redirect(url_for('home'))

@app.route('/tabla')
def tabla():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='operaciones')
    cursor = conn.cursor()
    cursor.execute('select id, correo, comentarios from comentarios order by id')
    datos = cursor.fetchall()
    return render_template("tabla.html", comentarios = datos)

@app.route('/editar/<string:id>')
def editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='operaciones')
    cursor = conn.cursor()
    cursor.execute('select id, correo, comentarios from comentarios where id = %s', (id))
    dato  = cursor.fetchall()
    return render_template("editar.html", comentar=dato[0])

@app.route('/borrar/<string:id>')
def borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='operaciones')
    cursor = conn.cursor()
    cursor.execute('delete from comentarios where id = {0}'.format(id))
    conn.commit()
    return redirect(url_for('tabla'))

@app.route('/editar_comenta/<string:id>',methods=['POST'])
def editar_comenta(id):
    if request.method == 'POST':
        corr=request.form['correo']
        come=request.form['comentarios']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='operaciones')
        cursor = conn.cursor()
        cursor.execute('update comentarios set correo=%s, comentarios=%s where id=%s', (corr,come,id))
        conn.commit()
    return redirect(url_for('tabla'))

if __name__ == "__main__":
    app.run(debug=True)
