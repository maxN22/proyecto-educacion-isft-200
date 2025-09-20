import duckdb
import pandas as pd
import streamlit as st
import os

# notas.
# DML = AGREGAR, EDITAR, ELIMINAR DATOS. (MODIFICAR EL CONTENIDO DE LA BASE DE DATOS).
# DDL = CREAR, MODIFICAR, ELIMINAR, COPIAR TABLA (MODIFICA EL FORMATO, NO EL CONTENIDO).
# DQL = PARA SELCCIONAR, O FILTRAR DATOS. 


# Clase para manejar la conexión y operaciones con la tabla 'pais'.
class Pais:
    def __init__(self, ruta_db ='db_educacion.duckdb'):
        self.ruta_db = ruta_db
        self.conn = duckdb.connect(database = self.ruta_db) # realizamos conexion a la base de datos.

    def obtener_paises(self):
        query = "SELECT id_pais as 'ID País', nombre_pais as 'Nombre' FROM pais" # DQL.
        df = self.conn.execute(query).fetchdf() #  devuelve los datos de forma tabular (tabla con filas y columnas)en dataframe.
        return df


    def insertar_pais(self, nombre_pais):
        query = "INSERT INTO pais (nombre_pais) VALUES (?)" # agregamos valores a la tabla.
        self.conn.execute(query,(nombre_pais,)) 
        self.conn.commit() # CONFIRMA LA EJECUCION. se coloca con los C.R.U.D


    def actualizar_pais(self, nombre_pais, id_pais):
        query = "UPDATE pais SET nombre_pais = ? WHERE id_pais = ?" # actualizamos valores a la tabla.
        self.conn.execute(query,(nombre_pais, id_pais)) 
        self.conn.commit() # CONFIRMA LA EJECUCION. se coloca con los C.R.U.D

# clase Vista.
class ComponentesPais:  # la clase lleva las clases van en parentesis cuando se herdan es un.

    def __init__(self):
        self.db = Pais() # es un objeto o  INSTANCIA PERO NO UNA HERENCIA DE LA CALSE Pais. el OBJETO ES LA COSA EN SI DE LA CALSE.

    def visualizar_paises(self):
        df_paises = self.db.obtener_paises() # self.db es una instancia de pais por lo tanto hereda los metodos.
        if df_paises.empty: # chequeamos que no este vacia.
            st.warning("No hay países registrados en la base de datos.") # ventana de mensaje.
        else:
            diccionario_selccion = st.dataframe(df_paises, # <- se aliemntan con los datos del df_paises.
                                                    height=250, # usamos un alto de 250.
                                                    use_container_width=True, # usamos el ancho total de la tabla.
                                                    selection_mode = 'single-row', # casilla de selccion. Especificar modo de selccion.
                                                    on_select = 'rerun', # se actualiza el buffer de la web.
                                                    hide_index = 'true') # ocultamos los numero del indice.
    

    def ingresar_paises(self):
        with st.form("formulario_pais", clear_on_submit = True): # creamos un formulario const.form. y limpiamos todos los campos
            st.write("### Registrar País") # titulo del formulario.
            nombre_pais = st.text_input("Nombre del País", max_chars=50) # text_input es un campo de ingreso de datos
            if st.form_submit_button("Registrar País"): # creaamos el boton
                    self.db.insertar_pais(nombre_pais) # metodo insertar y pasamos la variable.
                    st.rerun() # actualizamos el ingreso de datos a la tabla.
                    st.success(f"El país {nombre_pais} fue registrado exitosamente.") # mensaje de exito.
            else:
                st.error("Por favor, ingrese un nombre de país válido.") # mensaje de error.s


def main_paises(): # genera un objeo pais que sera una instancia de pais.
    objeto_pais = ComponentesPais()
    _col_formulario, _col_tabla = st.columns(2) # agregamos columnas al formulario.

    with _col_formulario: # llamamos a los metodos. with = dentro de...
        objeto_pais.ingresar_paises()
    with _col_tabla:
        objeto_pais.visualizar_paises()

if __name__ == "__main__":
    main_paises()


# para ejecutar el archivo debemos escribir la linea de comando "streamlit run archivo_pais.py"
# con la combiancion de teclas ctrl + c cerramos la cession.



