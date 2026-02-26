from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# BASE DE DATOS DE CANDIDATOS COMPLETA
partidos = [
    {"id": 1, "nombre": "MTS", "alcalde": "OLIVER OSCAR POMA CARTAGENA", "ciudad": "ORURO", "votos": 0},
    {"id": 2, "nombre": "PATRIA ORURO", "alcalde": "RAFAEL VARGAS VILLEGAS", "ciudad": "ORURO", "votos": 0},
    {"id": 3, "nombre": "LIBRE", "alcalde": "RENE BENJAMIN GUZMAN VARGAS", "ciudad": "ORURO", "votos": 0},
    {"id": 4, "nombre": "PP", "alcalde": "CARLOS AGUILAR", "ciudad": "ORURO", "votos": 0},
    {"id": 5, "nombre": "SOMOS ORURO", "alcalde": "MARCELO CORTEZ GUTIERREZ", "ciudad": "ORURO", "votos": 0},
    {"id": 6, "nombre": "JACHA", "alcalde": "MARCELO FERNANDO MEDINA CENTELLAS", "ciudad": "ORURO", "votos": 0},
    {"id": 7, "nombre": "SOL.BO", "alcalde": "MARCELO MEDINA", "ciudad": "ORURO", "votos": 0},
    {"id": 8, "nombre": "UN", "alcalde": "SAMUEL DORIA MEDINA", "ciudad": "LA PAZ", "votos": 0},
    {"id": 9, "nombre": "MAS", "alcalde": "CANDIDATO LA PAZ", "ciudad": "LA PAZ", "votos": 0}
]

# Registro de votos para evitar duplicados por CI
votos_registrados = []

@app.route('/')
def index():
    msg_type = request.args.get('msg_type')
    ci_votante = request.args.get('ci')
    return render_template('index.html', msg_type=msg_type, ci_votante=ci_votante)

@app.route('/votar/<ciudad>')
def votar(ciudad):
    # Filtra candidatos por la ciudad seleccionada
    partidos_ciudad = [p for p in partidos if p['ciudad'] == ciudad]
    return render_template('votar.html', ciudad=ciudad, partidos=partidos_ciudad)

@app.route('/confirmar_voto', methods=['POST'])
def confirmar_voto():
    # Captura de datos del formulario
    ci = request.form.get('ci').strip()
    partido_id = int(request.form.get('partido_id'))
    
    # VALIDACIÓN: Si el CI ya existe en la lista de votos_registrados
    if any(voto['ci'] == ci for voto in votos_registrados):
        # Redirige al index con el mensaje de error y el CI duplicado
        return redirect(url_for('index', msg_type='error', ci=ci))
    
    # Si es nuevo, se registra el voto
    nuevo_voto = {
        'ci': ci,
        'nombres': request.form.get('nombres').upper(),
        'apellido': request.form.get('apellido').upper(),
        'partido_id': partido_id
    }
    votos_registrados.append(nuevo_voto)
    
    # Sumar el voto al contador del partido correspondiente
    for p in partidos:
        if p['id'] == partido_id:
            p['votos'] += 1
            break
            
    # Redirige al index con mensaje de éxito
    return redirect(url_for('index', msg_type='success', ci=ci))

@app.route('/reporte')
def reporte():
    # Organiza los resultados por ciudad para el template reporte.html
    resultados = {}
    ciudades = sorted(list(set(p['ciudad'] for p in partidos)))
    
    for ciudad in ciudades:
        # Ordena de mayor a menor votación
        partidos_ordenados = sorted(
            [p for p in partidos if p['ciudad'] == ciudad],
            key=lambda x: x['votos'],
            reverse=True
        )
        resultados[ciudad] = partidos_ordenados
        
    return render_template('reporte.html', resultados=resultados)

if __name__ == '__main__':
    # Configuración para Render o ejecución local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
