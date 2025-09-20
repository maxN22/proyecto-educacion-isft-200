import duckdb
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
import time


# Clase para manejar la conexión y operaciones con la tabla 'pais'
class Pais:
    def __init__(self, ruta_db = 'repositorio/db_educacion.duckdb'):
        self.ruta_db = ruta_db
        self.conn = duckdb.connect(database = self.ruta_db)

    def obtener_paises(self):
        query = "SELECT id_pais as 'ID País', nombre_pais as 'Nombre' FROM pais"
        df_pais = self.conn.execute(query).fetch_df()
        #Se devuelve un DataFrame
        return df_pais
    
    def obtener_paises_filtro(self): # <--metodo de obtencion de paises filtrados.
        query = "SELECT FROM pais WHERE (nombre_pais) = (?)"
        df_pais_filtrado = self.conn.execute(query).fetch_df() # --> devuelve los datos en forma de datafreme.
        self.conn.commit() # --> colocar con los C.R.U.D.
        return df_pais_filtrado
        

    def insertar_pais(self, nom_pais):
        query = "INSERT INTO pais (nombre_pais) VALUES (?)"
        self.conn.execute(query, (nom_pais,))
        self.conn.commit()

    def actualizar_pais(self, nom_pais, id_pais):
        query = "UPDATE pais SET nombre_pais = ? WHERE id_pais = ?"
        self.conn.execute(query, (nom_pais, id_pais))
        self.conn.commit()


class ComponentesPais:
    def __init__(self):
        self.db = Pais()

    @st.dialog('Editar País')
    def formulario_editar_pais(self, serie_pais):
        nombre_pais = serie_pais.loc['Nombre']
        nuevo_nombre_pais = st.text_input('Ingresar nuevo nombre: ', value = nombre_pais, max_chars=50)
        if st.button('Guardar'):
            id_pais = int(serie_pais.loc['ID País'])
            self.db.actualizar_pais(nuevo_nombre_pais,id_pais)
            st.rerun()

            
    def visualizar_paises(self):
        df_paises = self.db.obtener_paises()
        if df_paises.empty:
            st.warning("No hay países registrados en la base de datos.")
        else:
            diccionario_seleccion =  st.dataframe(df_paises,# Fuente de datos
                                                height=250,# Largo de la tabla
                                                use_container_width=True,# Ocupe todo el ancho del contenedor
                                                selection_mode="single-row",# Especificar si vamos a seleccionar filas o culmnas
                                                on_select="rerun",# Cada vez que seleccionemos un registro, se actualiza el buffer de la web
                                                hide_index = True)# Ocultar los números de índice
        if diccionario_seleccion["selection"]["rows"]:
            if st.button('Editar'):
                indice_seleccionado = diccionario_seleccion["selection"]["rows"][0]
                st.write(indice_seleccionado)
                serie_pais_seleccionado = df_paises.loc[indice_seleccionado]
                self.formulario_editar_pais(serie_pais_seleccionado)

# nuevo_objeto_componete_pais = ComponentesPais()
# nuevo_objeto_componete_pais.visualizar_paises()

    def formulario_ingresar_paises(self):
        with st.form("formulario_pais", clear_on_submit = True):
            with st.container(height= 220, border= False):
                st.write("#### Registrar Nuevo País")
                nombre_pais = st.text_input("Nombre del País: ", max_chars=50)
                if st.form_submit_button("Registrar País"):
                    if nombre_pais:
                        self.db.insertar_pais(nombre_pais)
                        st.success(f"El país {nombre_pais} fue registrado exitosamente. 😎")
                        time.sleep(1.5)
                        st.rerun()
                        
                    else:
                        st.error("Por favor, ingrese un nombre de país válido.")

def main_paises():
    st.set_page_config(
        page_title="Aplicación de Gestión Educativa",
        layout="wide"
    )
    objeto_pais = ComponentesPais()

    columna_agregar_pais, columna_visualizar_pais =  st.columns([1.5,2])

    with columna_agregar_pais:
        objeto_pais.formulario_ingresar_paises()

    with columna_visualizar_pais:
        objeto_pais.visualizar_paises()
    

if __name__ == "__main__":
    main_paises()

