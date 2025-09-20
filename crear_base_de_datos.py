import duckdb

# Conectamos al nuevo archivo de base de datos DuckDB.
# Si el archivo no existe, DuckDB lo creará automáticamente.
# Si ya habían creado uno, eliminenlo antes de ejecutar este script.
# Porque hay tablas que ya existen y no se pueden crear de nuevo.
con = duckdb.connect("db_educacion.duckdb")

# Fíjense que separé las secuencias de las tablas, para que sea más fácil de leer y mantener.
# Antes las habíamos mezclado con cada tabla, pero ahora las agrupamos al inicio.
sql_script = """
-- Secuencias
CREATE SEQUENCE IF NOT EXISTS sec_pais START 1;
CREATE SEQUENCE IF NOT EXISTS sec_provincia START 1;
CREATE SEQUENCE IF NOT EXISTS sec_ciudad START 1;
CREATE SEQUENCE IF NOT EXISTS sec_calle START 1;
CREATE SEQUENCE IF NOT EXISTS sec_direccion START 1;
CREATE SEQUENCE IF NOT EXISTS sec_rol START 1;
CREATE SEQUENCE IF NOT EXISTS sec_titulo_superior START 1;
CREATE SEQUENCE IF NOT EXISTS sec_disciplina START 1;
CREATE SEQUENCE IF NOT EXISTS sec_carrera START 1;
CREATE SEQUENCE IF NOT EXISTS sec_catedra START 1;
CREATE SEQUENCE IF NOT EXISTS sec_titulo_secundario START 1;
CREATE SEQUENCE IF NOT EXISTS sec_categoria_nota START 1;
CREATE SEQUENCE IF NOT EXISTS sec_calificacion START 1;

-- Tablas
CREATE TABLE IF NOT EXISTS pais (
    id_pais INTEGER DEFAULT nextval('sec_pais') PRIMARY KEY,
    nombre_pais VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS provincia_estado (
    id_provincia INTEGER DEFAULT nextval('sec_provincia')  PRIMARY KEY,
    nombre_provincia VARCHAR(50) NOT NULL,
    fk_pais INTEGER NOT NULL,
    FOREIGN KEY (fk_pais) REFERENCES pais(id_pais)
);

CREATE TABLE IF NOT EXISTS ciudad_municipio (
    id_ciudad INTEGER DEFAULT nextval('sec_ciudad') PRIMARY KEY,
    nombre_ciudad VARCHAR(55) NOT NULL,
    fk_provincia INTEGER NOT NULL,
    FOREIGN KEY (fk_provincia) REFERENCES provincia_estado(id_provincia)
);

CREATE TABLE IF NOT EXISTS calle (
    id_calle BIGINT DEFAULT nextval('sec_calle') PRIMARY KEY,
    nombre_calle VARCHAR(55) NOT NULL,
    fk_ciudad INTEGER NOT NULL,
    FOREIGN KEY (fk_ciudad) REFERENCES ciudad_municipio(id_ciudad)
);

CREATE TABLE IF NOT EXISTS direccion (
    id_direccion INTEGER DEFAULT nextval('sec_direccion') PRIMARY KEY,
    numero_direccion INTEGER NOT NULL,
    departamento VARCHAR(6),
    fk_calle BIGINT NOT NULL,
    FOREIGN KEY (fk_calle) REFERENCES calle(id_calle)
);

CREATE TABLE IF NOT EXISTS persona (
    matricula_persona VARCHAR(45) PRIMARY KEY,
    nombre_persona VARCHAR(45) NOT NULL,
    apellido_persona VARCHAR(45) NOT NULL,
    dni_persona INTEGER NOT NULL,
    fecha_nac_persona DATE NOT NULL,
    genero_persona VARCHAR(1) NOT NULL CHECK genero_persona IN ('M','F','O')),
    email_persona VARCHAR(60),
    contraseña_persona VARCHAR(70),
    fk_direccion INTEGER NOT NULL,
    FOREIGN KEY (fk_direccion) REFERENCES direccion(id_direccion)
);

CREATE TABLE IF NOT EXISTS rol (
    id_rol INTEGER DEFAULT nextval('sec_rol') PRIMARY KEY,
    nombre_rol VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS persona_has_rol (
    fk_matricula_persona VARCHAR(45) NOT NULL,
    fk_rol INTEGER NOT NULL,
    PRIMARY KEY (fk_matricula_persona, fk_rol),
    FOREIGN KEY (fk_matricula_persona) REFERENCES persona(matricula_persona),
    FOREIGN KEY (fk_rol) REFERENCES rol(id_rol)
);

CREATE TABLE IF NOT EXISTS profesor (
    matricula_persona VARCHAR(45) PRIMARY KEY,
    fecha_ingreso_profesor DATE NOT NULL,
    FOREIGN KEY (matricula_persona) REFERENCES persona(matricula_persona)
);

CREATE TABLE IF NOT EXISTS titulo_superior (
    id_titulo INTEGER DEFAULT nextval('sec_titulo_superior') PRIMARY KEY,
    nombre_titulo VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS profesor_has_titulo (
    fk_matricula_profesor VARCHAR(45) NOT NULL,
    fk_titulo INTEGER NOT NULL,
    PRIMARY KEY (fk_matricula_profesor, fk_titulo),
    FOREIGN KEY (fk_matricula_profesor) REFERENCES profesor(matricula_persona),
    FOREIGN KEY (fk_titulo) REFERENCES titulo_superior(id_titulo)
);

CREATE TABLE IF NOT EXISTS disciplina (
    id_disciplina INTEGER DEFAULT nextval('sec_disciplina') PRIMARY KEY,
    nombre_disciplina VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS carrera (
    id_carrera INTEGER DEFAULT nextval('sec_carrera') PRIMARY KEY,
    nombre_carrera VARCHAR(45) NOT NULL,
    fk_disciplina INTEGER NOT NULL,
    FOREIGN KEY (fk_disciplina) REFERENCES disciplina(id_disciplina)
);

CREATE TABLE IF NOT EXISTS catedra (
    id_catedra INTEGER DEFAULT nextval('sec_catedra') PRIMARY KEY,
    nombre_catedra VARCHAR(45) NOT NULL,
    fk_carrera INTEGER NOT NULL,
    FOREIGN KEY (fk_carrera) REFERENCES carrera(id_carrera)
);

CREATE TABLE IF NOT EXISTS profesor_has_catedra (
    fk_profesor VARCHAR(45) NOT NULL,
    fk_catedra INTEGER NOT NULL,
    PRIMARY KEY (fk_profesor, fk_catedra),
    FOREIGN KEY (fk_profesor) REFERENCES profesor(matricula_persona),
    FOREIGN KEY (fk_catedra) REFERENCES catedra(id_catedra)
);

CREATE TABLE IF NOT EXISTS titulo_secundario (
    id_titulo_secundario INTEGER DEFAULT nextval('sec_titulo_secundario') PRIMARY KEY,
    nombre_titulo_secundario VARCHAR(65) NOT NULL
);

CREATE TABLE IF NOT EXISTS alumno (
    matricula_alumno VARCHAR(45) PRIMARY KEY,
    fk_titulo_secundario INTEGER NOT NULL,
    FOREIGN KEY (matricula_alumno) REFERENCES persona(matricula_persona),
    FOREIGN KEY (fk_titulo_secundario) REFERENCES titulo_secundario(id_titulo_secundario)
);

CREATE TABLE IF NOT EXISTS alumno_has_catedra (
    fk_catedra INTEGER NOT NULL,
    fk_alumno VARCHAR(45) NOT NULL,
    PRIMARY KEY (fk_catedra, fk_alumno),
    FOREIGN KEY (fk_catedra) REFERENCES catedra(id_catedra),
    FOREIGN KEY (fk_alumno) REFERENCES alumno(matricula_alumno)
);

CREATE TABLE IF NOT EXISTS categoria_calificacion (
    id_categoria INTEGER DEFAULT nextval('sec_categoria_nota') PRIMARY KEY,
    nombre_categoria VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS directivo (
    matricula_directivo VARCHAR(45) PRIMARY KEY,
    FOREIGN KEY (matricula_directivo) REFERENCES persona(matricula_persona)
);

CREATE TABLE IF NOT EXISTS directivo_has_titulo (
    fk_matricula_directivo VARCHAR(45) NOT NULL,
    fk_titulo INTEGER NOT NULL,
    PRIMARY KEY (fk_matricula_directivo, fk_titulo),
    FOREIGN KEY (fk_matricula_directivo) REFERENCES directivo(matricula_directivo),
    FOREIGN KEY (fk_titulo) REFERENCES titulo_superior(id_titulo)
);

CREATE TABLE IF NOT EXISTS calificacion (
    id_calificacion INTEGER DEFAULT nextval('sec_calificacion') PRIMARY KEY,
    fk_profesor VARCHAR(45) NOT NULL,
    fk_catedra INTEGER NOT NULL,
    fk_directivo VARCHAR(45) NOT NULL,
    fk_alumno VARCHAR(45) NOT NULL,
    fk_categoria INTEGER NOT NULL,
    nota_calificacion DOUBLE,
    descripcion_calificacion TEXT,
    FOREIGN KEY (fk_profesor) REFERENCES profesor(matricula_persona),
    FOREIGN KEY (fk_catedra) REFERENCES catedra(id_catedra),
    FOREIGN KEY (fk_directivo) REFERENCES directivo(matricula_directivo),
    FOREIGN KEY (fk_alumno) REFERENCES alumno(matricula_alumno),
    FOREIGN KEY (fk_categoria) REFERENCES categoria_calificacion(id_categoria)
);
"""

# Ejecutar el script
con.execute(sql_script)
con.close()
