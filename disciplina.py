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
        df_disciplina = self.conn.execute(query).fetch_df() # Ejecuta el query y lo convierte en un dataframe de pandas.
        return df_disciplina
        
    def actualizar_disciplina(self, nombre_disciplina, id_disciplina):
        query = "UPDATE disciplina SET nombre_disciplina = ? WHERE id_disciplina = ?"
        self.conn.execute(query, (nombre_disciplina, id_disciplina))
        self.conn.commit()
        

class ComponentesDisciplina():
    def __init__(self):
        self.db_disciplina = Disciplina() #instancia.

    @st.dialog('Editar Disciplina')

    def form_editar_diciplina(self, serie_disciplina): # series es de pandas contiene datos de disciplina. loc Se utiliza para seleccionar datos por el nombre de la fila o del índice.
        with st.form(key='Editar_Disciplina', clear_on_submit = True): # La Propiedad clear_on_submit = True restablezcan a sus valores predeterminados
            st.title("## Editar Disciplina")
            nombre_disciplina = serie_disciplina.loc['Nombre'] 
            new_nombre_disciplina = st.text_input('Ingrese el nuevo nombre de la Disciplina', value= nombre_disciplina, max_chars=45) # Entrda de datos.
            btn_guardar = st.form_submit_button(label="Guardar", type='primary') # <-- IMPORTANTE DENTRO DEL FORMULARAIO SE DEBEN CREAR CON ESTE METODO LOS BOTONES.
            if btn_guardar:
                id_disciplina = int(serie_disciplina.loc['ID Disciplina'])
                self.db_disciplina.actualizar_disciplina(new_nombre_disciplina, id_disciplina)
                st.rerun() # reseteamos los labels.

    def visualizar_disciplina(self):
        with st.form(key='Visualizar_Disciplinas', clear_on_submit = True): # Contenedor formulario.
            df_disciplina = self.db_disciplina.obtener_disciplina()
            btn_editar = st.form_submit_button(label="Editar", icon=None, type='primary') # Le agregamos etiquetas al boton.
            if df_disciplina.empty: # verificamos sis el data frame esta vacio.
                st.warning("No hay Disciplinas Registradas en la base de datos.")
            else:
                diccionario_seleccion =  st.dataframe(df_disciplina,# Fuente de datos
                                                    height=250,# Largo de la tabla
                                                    use_container_width=True,# Ocupe todo el ancho del contenedor
                                                    selection_mode="single-row",# Especificar si vamos a seleccionar filas o culmnas
                                                    on_select="rerun",# Cada vez que seleccionemos un registro, se actualiza el buffer de la web
                                                    hide_index = True)# Ocultar los números de índice
            if diccionario_seleccion["selection"]["rows"]:
                if btn_editar:
                    indice_seleccionado = diccionario_seleccion["selection"]["rows"][0]
                    serie_disciplina_seleccionado = df_disciplina.loc[indice_seleccionado]
                    self.form_editar_diciplina(serie_disciplina_seleccionado)

    def formulario_ingresar_disciplina(self):
        with st.form("Ingreso_Disciplina", clear_on_submit = True):
            st.write("#### Registrar nueva Disciplina")
            nombre_disciplina = st.text_input("Nombre de la Disciplina", max_chars=45)
            btn_registrar = st.form_submit_button(label="Registrar", icon=None, type='primary') # IMPORTANTE EL BOTON DEBE SER EL ULTIMO ELEMENTO DEL FORMULARIO. 
            if btn_registrar:
                if nombre_disciplina:
                    self.db_disciplina.agregar_disciplina(nombre_disciplina)
                    st.success(f"La Disciplina {nombre_disciplina} fue registrado exitosamente. 😎")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Por favor, ingrese una Disciplina valida.")



def main_disciplina():
    st.set_page_config(
        page_title="Aplicación de Gestión Educativa",
        layout="wide"
    )
    disciplina = ComponentesDisciplina()

    columna_agregar_disciplina, columna_visualizar_disciplina =  st.columns([1.5,2])

    with columna_agregar_disciplina:
        disciplina.formulario_ingresar_disciplina()

    with columna_visualizar_disciplina:
        disciplina.visualizar_disciplina()
    

if __name__ == "__main__":
    main_disciplina()
