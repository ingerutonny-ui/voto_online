import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

def obtener_partidos(ciudad):
    es_lp = "LA PAZ" in ciudad.upper()
    offset = 100 if es_lp else 0
    return [
        {"id": 1 + offset, "nombre": "FRI", "alcalde": "CANDIDATO FRI"},
        {"id": 2 + offset, "nombre": "LODEL", "alcalde": "CANDIDATO LODEL"},
        {"id": 3 + offset, "nombre": "NGP", "alcalde": "CANDIDATO NGP"},
        {"id": 4 + offset, "nombre": "AORA", "alcalde": "CANDIDATO AORA"},
        {"id": 5 + offset, "nombre": "UN", "alcalde": "WALDO ALBARRACIN" if es_lp else "SAMUEL DORIA MEDINA"},
        {"id": 6 + offset, "nombre": "ALIANZA", "alcalde": "CANDIDATO ALIANZA"},
        {"id": 7 + offset, "nombre": "AESA", "alcalde": "CANDIDATO AESA"},
        {"id": 8 + offset, "nombre": "SÚMATE", "alcalde": "CANDIDATO SÚMATE"},
        {"id": 9 + offset, "nombre": "MTS", "alcalde": "RONALD ESCOBAR" if es_lp else "OLIVER OSCAR POMA CARTAGENA"},
        {"id": 10 + offset, "nombre": "JALLALLA", "alcalde": "DAVID CASTRO"},
        {"id": 11 + offset, "nombre": "LIBRE", "alcalde": "FRANKLIN FLORES" if es_lp else "RENE BENJAMIN GUZMAN VARGAS"},
        {"id": 12 + offset, "nombre": "PP", "alcalde": "AMILCAR BARRAL" if es_lp else "CARLOS AGUILAR"},
        {"id": 13 + offset, "nombre": "SOMOS PUEBLO", "alcalde": "IVAN ARIAS" if es_lp else "MARCELO CORTEZ GUTIERREZ"},
        {"id": 14 + offset, "nombre": "JA-HA", "alcalde": "MARCELO FERNANDO MEDINA CENTELLAS"},
        {"id": 15 + offset, "nombre": "PDC", "alcalde": "ANA MARÍA FLORES"}
    ]

@app.route('/reporte')
def reporte():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT partido_id, COUNT(*) FROM votos GROUP BY partido_id')
    conteos = dict(cur.fetchall())
    cur.close()
    conn.close()
    
    res = {}
    totales = {}
    for ciudad in ["ORURO", "LA PAZ"]:
        lista = obtener_partidos(ciudad)
        suma = 0
        for p in lista:
            p['votos'] = conteos.get(p['id'], 0)
            suma += p['votos']
        res[ciudad] = lista
        totales[ciudad] = suma
    return render_template('reporte.html', resultados=res, totales=totales)

# ... (mantener rutas de index y votar que ya funcionan)
