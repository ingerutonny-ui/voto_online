from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# BASE DE DATOS LOCAL
votos = [] 

# LISTA REAL DE CANDIDATOS SEGÚN PAPELETAS DE CONSULTA
partidos_oruro = [
    {"id": 1, "nombre": "MTS", "alcalde": "OLIVER OSCAR POMA CARTAGENA"},
    {"id": 2, "nombre": "PATRIA ORURO", "alcalde": "RAFAEL VARGAS VILLEGAS"},
    {"id": 3, "nombre": "LIBRE", "alcalde": "RENE BENJAMIN GUZMAN VARGAS"},
    {"id": 4, "nombre": "PP", "alcalde": "CARLOS AGUILAR"},
    {"id": 5, "nombre": "SOMOS ORURO", "alcalde": "MARCELO CORTEZ GUTIERREZ"},
    {"id": 6, "nombre": "JACHA", "alcalde": "MARCELO FERNANDO MEDINA CENTELLAS"},
    {"id": 7, "nombre": "SOL.BO", "alcalde": "MARCELO MEDINA"},
    {"id": 8, "nombre": "UN", "alcalde": "SAMUEL DORIA MEDINA"},
    {"id": 9, "nombre": "MAS-IPSP", "alcalde": "ADHEMAR WILCARANI"},
    {"id": 10, "nombre": "PBCP", "alcalde": "LIZETH TITO"},
    {"id": 11, "nombre": "UCS", "alcalde": "JORGE CALLE"},
    {"id": 12, "nombre": "PAN-BOL", "alcalde": "MILTON GOMEZ"},
    {"id": 13, "nombre": "AS", "alcalde": "ALVARO CASTELLON"},
    {"id": 14, "nombre": "FPV", "alcalde": "JAVIER CALIZAYA"},
    {"id": 15, "nombre": "BST", "alcalde": "FREDDY CANAVIRI"},
    {"id": 16, "nombre": "LIDER", "alcalde": "CARMEN ROSA QUISPE"},
    {"id": 17, "nombre": "UNSOL", "alcalde": "ESTEBAN MAMANI"}
]

partidos_lapaz = [
    {"id": 101, "nombre": "SOBERANÍA", "alcalde": "FELIPE QUISPE"},
    {"id": 102, "nombre": "SOL.BO", "alcalde": "ALVARO BLONDEL"},
    {"id": 103, "nombre": "PAN-BOL", "alcalde": "AMILCAR BARRAL"},
    {"id": 104, "nombre": "MAS-IPSP", "alcalde": "CESAR DOCKWEILER"},
    {"id": 105, "nombre": "UCS", "alcalde": "PETER MALDONADO"},
    {"id": 106, "nombre": "MTS", "alcalde": "RONALD ESCOBAR"},
    {"id": 107, "nombre": "JALLALLA", "alcalde": "DAVID CASTRO"},
    {"id": 108, "nombre": "PBCP", "alcalde": "LOURDES CHUMACERO"},
    {"id": 109, "nombre": "FICO", "alcalde": "LUIS LARREA"},
    {"id": 110, "nombre": "ASP", "alcalde": "RAMIRO BURGOS"},
    {"id": 111, "nombre": "VENCEREMOS", "alcalde": "OSCAR HEREDIA"},
    {"id": 112, "nombre": "UN", "alcalde": "WALDO ALBARRACIN"},
    {"id": 113, "nombre": "FPV", "alcalde": "FRANKLIN FLORES"},
    {"id": 114, "nombre": "C-A", "alcalde": "JOSE LUIS BEDREGAL"},
    {"id": 115, "nombre": "MDS", "alcalde": "IVAN ARIAS"},
    {"id": 116, "nombre": "MNR", "alcalde": "REINALDO GARCIA"},
    {"id": 117, "nombre": "PDC", "alcalde": "ANA MARÍA FLORES"}
]

@app.route('/')
def index():
    msg_type = request.args.get('msg_type')
    ci_votante = request.args.get('ci')
    return render_template('index.html', msg_type=msg_type, ci_votante=ci_votante)

@app.route('/votar/<ciudad>')
def votar(ciudad):
    ciudad_upper = ciudad.upper().replace("_", " ")
    lista = partidos_oruro if "ORURO" in ciudad_upper else partidos_lapaz
    return render_template('votar.html', ciudad=ciudad_upper, partidos=lista)

@app.route('/confirmar_voto', methods=['POST'])
def confirmar_voto():
    ci = request.form.get('ci')
    
    # Verificación de duplicados
    for v in votos:
        if v['ci'] == ci:
            return redirect(url_for('index', msg_type='error', ci=ci))
    
    # Registro completo
    nuevo_voto = {
        "ci": ci,
        "nombres": request.form.get('nombres').upper(),
        "apellido": request.form.get('apellido').upper(),
        "edad": request.form.get('edad'),
        "genero": request.form.get('genero'),
        "celular": request.form.get('celular'),
        "partido_id": request.form.get('partido_id')
    }
    votos.append(nuevo_voto)
    
    return redirect(url_for('index', msg_type='success', ci=ci))

if __name__ == '__main__':
    app.run(debug=True)
