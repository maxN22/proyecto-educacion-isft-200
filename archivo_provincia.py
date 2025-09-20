import duckdb
import pandas as pd
import streamlit as st
import os
from archivo_pais import Pais
import time


# Clase para manejar la conexión y operaciones con la tabla 'provincia'
# 1 País -> muchas provincias (Agregación)
class Provincia:
    def __init__(self, ruta_db ='repositorio/db_educacion.duckdb'):
        self.ruta_db = ruta_db
        self.conn = duckdb.connect(database = self.ruta_db)

    def obtener_provincias(self):
        query = """SELECT
                        provincia_estado.id_provincia as 'ID Provincia', 
                        provincia_estado.nombre_provincia as 'Provincia',
                        pais.nombre_pais as 'País'
                    FROM provincia_estado
                    JOIN pais ON  provincia_estado.fk_pais = pais.id_pais"""
        df_provincia = self.conn.execute(query).fetchdf()
        return df_provincia

    def insertar_provincia(self, nombre_provincia, clave_pais):
        query = "Insert into provincia_estado (nombre_provincia, fk_pais) values (?,?)"
        self.conn.execute(query,(nombre_provincia, clave_pais))
        self.conn.commit()
    
    def actualizar_provincia(self, nom_provincia, id_provincia, id_pais):
        query = "UPDATE provincia_estado SET nombre_provincia = ?, fk_pais = ?  WHERE id_provincia = ?"
        self.conn.execute(query, (nom_provincia, id_pais, id_provincia))
        self.conn.commit()


class ComponentesProvincia():
    def __init__(self):
        self.db_provincia = Provincia()
        self.db_pais = Pais()   

    @st.dialog('Editar Provincia') # --> funcion que habre un cuadro de dialogo.

    def editar_provincia(self, nombre_provincia, id_provincia, nombre_pais, diccionario_pais):
        txt_editar_provincia = st.text_input("Modificar la provincia/estado/departamento:", value = nombre_provincia)
        tupla_editar_pais = tuple(diccionario_pais.keys())
        indice_pais = tupla_editar_pais.index(nombre_pais)
        editar_pais = st.selectbox("Ingresar Pais: ", tupla_editar_pais, index = indice_pais)
        id_pais_seleccionado = diccionario_pais[editar_pais]
        if st.button('Guardar Provincia'):
            if txt_editar_provincia:
                #def actualizar_provincia(self, nom_provincia, id_provincia, id_pais):
                self.db_provincia.actualizar_provincia(txt_editar_provincia, id_provincia, id_pais_seleccionado)
                st.success('Provincia/Estado/Departamento Modificado con Éxito')
                time.sleep(1.5)
                st.rerun()
            else:
                st.error('ERROR: Falta ingresar una provincia/estado/departamento')


    def visualizar_provincias(self):
        #df_provincias es un DataFrame de Pandas
        df_provincias = self.db_provincia.obtener_provincias()
        #st.dataframe es de Streamlit
        diccionario_provincia_seleccionada = st.dataframe(df_provincias,
                                                    #hide_index = True,
                                                    selection_mode='single-row',
                                                    on_select= 'rerun')
        
        if diccionario_provincia_seleccionada['selection']['rows']: # selection= clave que contiene otro cuya clave es rows y valor una lista
            indice_provincia_seleccionada = diccionario_provincia_seleccionada['selection']['rows'][0]
            serie_provincia = df_provincias.loc[indice_provincia_seleccionada]
        
            if st.button('Editar Provincia'):
                df_pais = self.db_pais.obtener_paises()
                diccionario_paises = dict(zip(df_pais['Nombre'],df_pais['ID País']))
                id_provincia_seleccionada = int(serie_provincia['ID Provincia'])
                self.editar_provincia(diccionario_pais = diccionario_paises,id_provincia = id_provincia_seleccionada,nombre_pais = str(serie_provincia.loc['País']), nombre_provincia = str(serie_provincia.loc['Provincia']))

                
        else:
            indice_provincia_seleccionada = None


    def ingresar_provincias(self):
        txt_provincia = st.text_input('Ingrese la Provincia/Estado/Departamento', max_chars=50)
        df_pais = self.db_pais.obtener_paises()
        diccionario_paises = dict(zip(df_pais['Nombre'],df_pais['ID País']))
        tupla_paises = tuple(diccionario_paises.keys())
        selector_pais = st.selectbox('Seleccionar un país: ',tupla_paises)
        id_pais = diccionario_paises[selector_pais]
        if st.button('Agregar'):
            if txt_provincia:
                self.db_provincia.insertar_provincia(txt_provincia,id_pais)
                st.success('Provincia Agregada')
                time.sleep(1.5)
                st.rerun()
            else:
                st.error('Falta ingresar el nombre de la provincia/estado/departamento')
                time.sleep(2)
                st.rerun()
#============================================================

    def buscar_provincia_pais(self):
        # Creamos el formulario de busqueda.
        with st.form(key='form_busqueda'):
            st.title("Busqueda Filtrada por pais y nombre de provincia")
            lbl_busqueda_pais = st.text_input("Ingresa el pais: ") 
            lbl_busqueda_provincia = st.text_input("Ingresa la provincia: ")

            # Botón para enviar el formulario
            enviar_busqueda = st.form_submit_button('Buscar')
        
        # condicional de opciones.
        if enviar_busqueda:
            if lbl_busqueda_pais:
                pais = self.db_pais.obtener_paises_filtro()   
                st.write(f"Resultados para: {pais}")
                
            elif lbl_busqueda_provincia:
                provincia = ComponentesProvincia.visualizar_provincias_filtrada()
                st.write(provincia)

            else:
                pass
                

           

        


    



#============================================================
objeto_provincia = ComponentesProvincia()
objeto_provincia.visualizar_provincias()
objeto_provincia.ingresar_provincias()
objeto_provincia.buscar_provincia_pais()




