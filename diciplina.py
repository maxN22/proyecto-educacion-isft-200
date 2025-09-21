import duckdb
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
import time



class Disciplina():
     
    def __init__(self, ruta_db = 'repositorio/db_educacion.duckdb'):
         self.ruta_db = ruta_db
         self.conn = duckdb.connect(database= self.ruta_db) # creamos el atributo conn al cual le pasamos conexion de duckdb; la cual contiene la DB.
     
    def agregar_disciplina(self, nombre_disciplina):
        query = "INSERT INTO disciplina (nombre_disciplina) VALUES(?)"
        self.conn.execute(query, (nombre_disciplina,))
        self.conn.commit() # --> colocar con los C.R.U.D.

    def obtener_disciplina(self):
        query = "SELECT id_disciplina as 'ID Disciplina', nombre_disciplina as 'Nombre' FROM disciplina"
        df_disciplina = self.conn.execute(query).fetch_df()
        return df_disciplina
        
        

class ComponentesDisciplina():
    def __init__(self):
        # Creamos las instancias con las entidades que interactua.
        #elf.db_carrera = Carrera()
        self.db_disciplina = Disciplina()   

    def form_ingreso_diciplina(self):
        # with st.form(key='Ingreso de Diciplinas', clear_on_submit = True):
        #     with st.container(height= 330, border= True):
        #         st.title("Agregar Diciplina")
        #         def form_ingreso_carrera(self):
        with st.form(key='Ingreso de Disciplina', clear_on_submit = True):
            with st.container(height= 330, border= True):
                st.title("Agregar Disciplina")
                nom_disciplina = st.text_input("Ingresa la Disciplina") # creamos una entrada de datos.
                df_disciplina = self.db_disciplina.agregar_disciplina() # creamos el dataframe al cual le pasamos el metodo de agregar.
                btn_cargar = st.button('Agregar') # <-- Creamos un boton
                diccionario_disciplina = dict(zip(df_disciplina['Nombre'],df_disciplina['ID Disciplina'])) # Unimos los campos del df con zip; lo parcemaos a un dict.
                tupla_diciplina = tuple(diccionario_disciplina.keys()) # Parceamos el dict en una tupla
                selector_diciplina = st.selectbox('Seleccionar una carrera',tupla_diciplina) # Creamos un selectbox con la tupla de las diciplinas.
                id_disciplina = diccionario_disciplina[selector_diciplina]
                if btn_cargar:
                    if nom_disciplina:
                        self.db_disciplina.agregar_disciplina(nom_disciplina,id_disciplina)
                        st.success('Disciplina Agregada')
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error('Falta ingresar el nombre de la Disciplina')
                        time.sleep(2)
                        st.rerun()




Diciplina1 = Disciplina()

Diciplina1.agregar_disciplina("Voley")
