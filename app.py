import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'consulta_ciudadana_secret'

# --- CONFIGURACIÓN DE BASE DE DATOS ---
uri = os.environ.get('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Compatibilidad con motores de DB y dispositivos antiguos
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"sslmode": "prefer"}}

db = SQLAlchemy(app)

# --- MODELOS ---
class Votante(db.Model):
    ci = db.Column(db.String(20), primary_key=True)
    ciudad = db.Column(db.String(50))
    ya_voto = db.Column(db.Boolean, default=False)
    fecha_voto = db.Column(db.DateTime, default=datetime.utcnow)

class Partido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    alcalde = db.Column(db.String(100), nullable=False)
    concejal = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)
    votos_alcalde = db.Column(db.Integer, default=0)
    votos_concejal = db.Column(db.Integer, default=0)

# --- INICIALIZACIÓN DE DATOS REALES ---
@app.route('/')
def index():
    try:
        db.drop_all()
        db.create_all()
        
        # Datos Oruro (de tu PDF)
        oruro_data = [
            {"p": "FRI", "a": "Rene Roberto Mamani Llave"}, {"p": "LEAL", "a": "Adhemar Willcarani Morales"},
            {"p": "NGP", "a": "Iván Quispe Gutiérrez"}, {"p": "AORA", "a": "Santiago Condori Apaza"},
            {"p": "UN", "a": "Enrique Fernando Urquidi Daza"}, {"p": "AUPP", "a": "Juan Carlos Choque Zubieta"},
            {"p": "UCS", "a": "Lino Marcos Main Adrián"}, {"p": "BST", "a": "Edgar Rafael Bazán Ortega"},
            {"p": "SUMATE", "a": "Oscar Miguel Toco Choque"}, {"p": "MTS", "a": "Oliver Oscar Poma Cartagena"},
            {"p": "PATRIA", "a": "Rafael Vargas Villegas"}, {"p": "LIBRE", "a": "Rene Benjamin Guzman Vargas"},
            {"p": "PP", "a": "Carlos Aguilar"}, {"p": "SOMOS ORURO", "a": "Marcelo Cortez Gutiérrez"},
            {"p": "JACHA", "a": "Marcelo Fernando Medina Centellas"}
        ]
        # Datos La Paz (de tu lista)
        lapaz_data = [
            {"p": "Jallalla", "a": "Jhonny Plata"}, {"p": "ASP", "a": "Xavier Iturralde"},
            {"p": "Venceremos", "a": "Waldo Albarracín"}, {"p": "Somos La Paz", "a": "Miguel Roca"},
            {"p": "UPC", "a": "Luis Eduardo 'Chichi' Siles"}, {"p": "Libre", "a": "Carlos 'Cae' Palenque"},
            {"p": "A-UPP", "a": "Isaac Fernández"}, {"p": "Innovación Humana", "a": "César Dockweiler"},
            {"p": "VIDA", "a": "Fernando Valencia"}, {"p": "FRI", "a": "Raúl Daza"},
            {"p": "PDC", "a": "Mario Silva"}, {"p": "MTS", "a": "Jorge Dulon"},
            {"p": "NGP", "a": "Hernán Rodrigo Rivera"}, {"p": "MPS", "a": "Ricardo Cuevas"},
            {"p": "APB-Súmate", "a": "Óscar Sogliano"}, {"p": "Alianza Patria", "a": "Carlos Nemo Rivera"},
            {"p": "Suma por el Bien Común", "a": "Iván Arias"}
        ]

        p_objs = []
        for i, c in enumerate(oruro_data, 1):
            p_objs.append(Partido(nombre=c["p"], alcalde=c["a"], concejal=f"Concejal {i}", ciudad="ORURO"))
        for i, c in enumerate(lapaz_data, 1):
            p_objs.append(Partido(nombre=c["p"], alcalde=c["a"], concejal=f"Concejal {i}", ciudad="LA PAZ"))
        
        db.session.bulk_save_objects(p_objs)
        db.session.commit()
        return render_template('index.html', mensaje="SISTEMA REINICIADO - DATOS CARGADOS")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/votar/<ciudad>')
def votar(ciudad):
    partidos = Partido.query.filter_by(ciudad=ciudad).order_by(Partido.id).all()
    prefijo = "OR" if ciudad == "ORURO" else "LP"
    return render_template('votar.html', ciudad=ciudad, partidos=partidos, prefijo=prefijo)

@app.route('/confirmar_voto', methods=['POST'])
def confirmar_voto():
    p = Partido.query.get(request.form.get('partido_id'))
    return render_template('confirmar.html', partido=p, ciudad=request.form.get('ciudad'))

@app.route('/registrar_voto', methods=['POST'])
def registrar_voto():
    ci = request.form.get('ci')
    p_id = request.form.get('partido_id')
    v = Votante.query.get(ci)
    if v and v.ya_voto: return render_template('error.html', mensaje="Ya votó.")
    if not v: v = Votante(ci=ci, ya_voto=True); db.session.add(v)
    else: v.ya_voto = True
    p = Partido.query.get(p_id)
    p.votos_alcalde += 1; p.votos_concejal += 1
    db.session.commit()
    return render_template('exito.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
