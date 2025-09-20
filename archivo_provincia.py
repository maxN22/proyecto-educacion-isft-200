import duckdb
import pandas as pd # para dataframe.
import streamlit as st
import os
from archivo_pais import Pais
import time


# notas.
# DML = AGREGAR, EDITAR, ELIMINAR DATOS. (MODIFICAR EL CONTENIDO DE LA BASE DE DATOS).
# DDL = CREAR, MODIFICAR, ELIMINAR, COPIAR TABLA (MODIFICA EL FORMATO, NO EL CONTENIDO).
# DQL = PARA SELCCIONAR, O FILTRAR DATOS. 

# Clase para manejar la conexión y operaciones con la tabla 'pais'.
class Provincia:

    def __init__(self, ruta_db ='db_educacion.duckdb'): # base de datos envevida.
        self.ruta_db = ruta_db
        self.conn = duckdb.connect(database = self.ruta_db)

    def obtener_provincias(self):

        query_provincia = '''SELECT provincia_estado.id_provincia as "ID Provincia", 
                            provincia_estado.nombre_provincia as "Nombre provincia" 
                            pais.nombre_pais as 'Pais'
                            FROM provincia_estado
                            JOIN pais ON provincia_estado.fk_pais = pais.id_pais'''
        
        df_provincia = self.conn.execute(query=query_provincia).fetch_df() #  devuelve los datos en dataframe.
        return df_provincia

    def insertar_provincias(self, nombre_provincia, clave_pais):

        query = "INSERT INTO provincia_estado(nombre_provincia, fk_pais) VALUES (?,?)" # agregamos valores a la tabla.
        self.conn.execute(query, (nombre_provincia, clave_pais)) # primer parametro es el query y luego la tupla conjunto de valores que le pasamos como parametros.
        self.conn.commit() # CONFIRMA LA EJECUCION. (comprometemos).


class ComponentesProvincia():
    
    def __init__(self):
        self.db_provincia = Provincia()

    def visdualizar_provincias(self):
        st.dataframe(self.db_provincia.obtener_provincias(),
                     hide_index= True,
                     column_order= ['ID Provincia', 'Provincia']) # con este atributo cambiamos el orden de las columnas.
            
    def ingresar_provincias(self):

            txt_provincia = st.text_input('Íngrese la provincia: ') # creamos una caja de texto.
            df_pais = self.db_pais.obtener_paises() # dataframe
            diccionario_paises = dict(zip(df_pais['Nombre'],df_pais['ID_Pais'])) # CREAMOS EL DICCIONARIO PARA ALMACENAR Y VINCULAR.
            lista_paises = list(diccionario_paises.keys())
            selector_pais = st.selectbox('Seleccionar un pais: ', lista_paises) # box de seleccion.
            id_pais = diccionario_paises[selector_pais]
            if st.bottom('Agregar provincia'):
                self.db_provincia.insertar_provincias(txt_provincia, id_pais)
                st.success('Provincia Agregada')
                time.sleep(1.5) # retrasamos por un tiempo.
                st.rerun() # actualizamos 



nuevo_componente = ComponentesProvincia()

objeto_provincia = Provincia()

objeto_provincia.insertar_provincias('Buenos Aires', 1)

st.write(objeto_provincia.obtener_provincias())



