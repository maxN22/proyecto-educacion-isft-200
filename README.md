<center><h1>AGREGADOS</h1></center> 

## Se agrego dentro del archivo_provincia.py

> **El metodo buscar_provincia_pais.**

#### El mismo Contiene:
 * --> Un formulario que nos permite ingresar una busqueda por nombre_pais o nombre_provincia. 
 * --> Condiional de verificacion si la variable recibe un dato por el submit.
 * --> Creamos una variable df_paises a la cual le pasamos el dataframe obtenido por el metodo obtener_paises de la clase Pais.
 * --> **IMPORTANTE!** la variable *dict_option* guarda un **Diccionario** el cual es obtenido mediante el metodo *to_dict* el cual **Convierte un dataframe de Pandas en un diccionario** el metodo recibe *orient="index"*, *para que nos permita recorrer mejor clave valor* .
 * --> Creamos un diccionario nombrado *claves_encontradas*; mediante (comprension de diccionario) el cual devuelve claves y valores del *dict_option* en condicional si la clave 'Nombre' se encuentra en los valores y el valor de la variable lbl_busqueda_pais es igual al valor en el valor 'Nombre'.
 * --> Creamos otro condicional para verificar si dentro claves_encotradas en la clave 0; valor clave "Nombre" es igual a lo recibido por input; en ese caso almacenamos ese valor en un avariable y la devolvemos con el metodo -> st.write(). 

> **Nota:** *Hay una falla ya que se ingresa un pais no cargado en el dataframe se pincha todo.*



## Se agrego dentro del archivo_paises.py

> **El metodo obtener_paises_filtro.**

> **Nota:** *Hay una falla ya que se ingresa un pais no cargado en el dataframe se pincha todo.*


> Se agrego dentro del archivo_paises.py
    * El metodo obtener_paises_filtro.