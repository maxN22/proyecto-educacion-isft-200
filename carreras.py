import duckdb
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
import time
from disciplina import Disciplina # Lo importamos porque la entidad carrera depende de la entidad diciplina



class Carrera():

    def __init__(self, ruta_db = 'repositorio/db_educacion.duckdb'):
        self.ruta_db = ruta_db
        self.conn = duckdb.connect(database = self.ruta_db)

    def agregar_carrera(self, nombre_carrera, fk_disciplina):
        query = "INSERT INTO carrera (nombre_carrera, fk_disciplina ) VALUES (?,?)"
        self.conn.execute(query, ( nombre_carrera, fk_disciplina))
        self.conn.commit() # --> colocar con los C.R.U.D.
        
    def buscar_carreras(self):
        query = """SELECT
                        carrera.id_carrera as 'ID Carrera', 
                        carrera.nombre_carrera as 'Carrera',
                        disciplina.nombre_disciplina as 'Disciplina'
                    FROM carrera JOIN disciplina ON  carrera.fk_disciplina = disciplina.id_disciplina"""
        df_carrera = self.conn.execute(query).fetch_df()
        #Se devuelve un DataFrame
        return df_carrera


class ComponentesCarrera():
    def __init__(self):
        # Creamos las instancias con las entidades que interactua.
        self.db_carrera = Carrera()
        self.db_disciplina = Disciplina()   

    @st.dialog('Agregados de Carreras') # IMPORTANTE COLOCAR PARA QUE MANTENGA EL FORMULARIO

    def ingreso_carrera(self):
        with st.form("formulario Carrera", clear_on_submit = True):
            st.title("Agregar Carreras")
            nom_carrera = st.text_input('Ingresa la Carrera', max_chars=45) # Entrada de datos.
            df_disciplina = self.db_disciplina.obtener_disciplina() # Creamos un adataframe con el metodo obtener disciplina de disciplina.py
            diccionario_disciplina = dict(zip(df_disciplina['Nombre'],df_disciplina['ID Disciplina'])) # al campo nombre y id disciplina lo unimos y parcemaos a un diccionario
            tupla_disciplina = tuple(diccionario_disciplina.keys()) # A las claves del diccionario_disciplina las guardamos en una tupla.
            selector_disciplina = st.selectbox('Seleccionar una disciplina: ',tupla_disciplina) # Al selectbox le pasamos la tupla con las disciplinas.
            id_disciplina = diccionario_disciplina[selector_disciplina]
            btn_cargar = st.form_submit_button('Agregar')
            if btn_cargar:
                if nom_carrera:
                    self.db_carrera.agregar_carrera(nom_carrera, id_disciplina)
                    st.success('Carrera Agregada')
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error('Falta ingresar el nombre de la Disciplina')
                    time.sleep(2)
                    st.rerun()




        
        
        
     
#==============================

#===============OBJETOS================================



carrera1 = ComponentesCarrera() # instancia.
carrera1.ingreso_carrera()
