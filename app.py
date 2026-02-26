from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('votos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY,
            ciudad TEXT,
            partido TEXT,
            alcalde TEXT,
            votos INTEGER DEFAULT 0
        )
    ''')
    
    # LISTA MAESTRA: Ordenada según papeleta oficial
    # Se eliminan nombres antiguos y se ponen los oficiales: JA-HA, SOMOS PUEBLO, etc.
    partidos_maestros = [
        {"id": 1, "nombre": "FRI", "alcalde": "CANDIDATO FRI"},
        {"id": 2, "nombre": "LODEL", "alcalde": "CANDIDATO LODEL"},
        {"id": 3, "nombre": "NGP", "alcalde": "CANDIDATO NGP"},
        {"id": 4, "nombre": "AORA", "alcalde": "CANDIDATO AORA"},
        {"id": 5, "nombre": "UN", "alcalde": "SAMUEL DORIA MEDINA"},
        {"id": 6, "nombre": "ALIANZA", "alcalde": "CANDIDATO ALIANZA"},
        {"id": 7, "nombre": "AESA", "alcalde": "CANDIDATO AESA"},
        {"id": 8, "nombre": "SÚMATE", "alcalde": "CANDIDATO SÚMATE"},
        {"id": 9, "nombre": "MTS", "alcalde": "OLIVER OSCAR POMA CARTAGENA"},
        {"id": 10, "nombre": "JALLALLA", "alcalde": "DAVID CASTRO"},
        {"id": 11, "nombre": "LIBRE", "alcalde": "RENE BENJAMIN GUZMAN VARGAS"},
        {"id": 12, "nombre": "PP", "alcalde": "CARLOS AGUILAR"},
        {"id": 13, "nombre": "SOMOS PUEBLO", "alcalde": "MARCELO CORTEZ GUTIERREZ"},
        {"id": 14, "nombre": "JA-HA", "alcalde": "MARCELO FERNANDO MEDINA CENTELLAS"},
        {"id": 15, "nombre": "PDC", "alcalde": "ANA MARÍA FLORES"}
    ]

    # Insertar solo si la tabla está vacía para evitar duplicados en Render
    cursor.execute('SELECT COUNT(*) FROM votos')
    if cursor.fetchone()[0] == 0:
        for p in partidos_maestros:
            # Inicializamos para ORURO y LA PAZ con el mismo orden oficial
            cursor.execute('INSERT INTO votos (id, ciudad, partido, alcalde, votos) VALUES (?, ?, ?, ?, ?)',
                           (p['id'], "ORURO", p['nombre'], p['alcalde'], 0))
            cursor.execute('INSERT INTO votos (id, ciudad, partido, alcalde, votos) VALUES (?, ?, ?, ?, ?)',
                           (p['id'] + 100, "LA PAZ", p['nombre'], p['alcalde'], 0))
    conn.commit()
    conn.close()

# ESTA LÍNEA ES LA SOLUCIÓN: Ejecuta la creación de tabla al cargar el módulo en Render
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votar/<ciudad>')
def votar(ciudad):
    conn = sqlite3.connect('votos.db')
    cursor = conn.cursor()
    # Mantenemos el orden por ID para que la vista de votación sea igual a la papeleta
    cursor.execute('SELECT * FROM votos WHERE ciudad = ? ORDER BY id ASC', (ciudad,))
    partidos = cursor.fetchall()
    conn.close()
    return render_template('votar.html', ciudad=ciudad, partidos=partidos)

@app.route('/registrar_voto/<int:partido_id>')
def registrar_voto(partido_id):
    conn = sqlite3.connect('votos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE votos SET votos = votos + 1 WHERE id = ?', (partido_id,))
    cursor.execute('SELECT ciudad FROM votos WHERE id = ?', (partido_id,))
    ciudad = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return render_template('exito.html', ciudad=ciudad)

@app.route('/reporte')
def reporte():
    conn = sqlite3.connect('votos.db')
    cursor = conn.cursor()
    # El orden ASC por ID garantiza que el FRI (ID 1) siempre sea el primero
    cursor.execute('SELECT ciudad, partido, alcalde, votos FROM votos ORDER BY ciudad, id ASC')
    data = cursor.fetchall()
    conn.close()

    resultados = {}
    for ciudad, partido, alcalde, votos in data:
        if ciudad not in resultados:
            resultados[ciudad] = []
        resultados[ciudad].append({'nombre': partido, 'alcalde': alcalde, 'votos': votos})

    return render_template('reporte.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
