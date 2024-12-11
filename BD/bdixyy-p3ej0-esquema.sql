
--(Bases de Datos I)
--Curso académico (2024/25) y convocatoria (enero).
--(P3. Definición y modificación de datos en SQL).
-- fichero bd1-p3-revistas-esquema.sql
-- Kateryna Pasternak y IVAN ANDRES YAGUAL MENDEZ
CREATE TABLE REVISTA(
idrev CHAR(4) PRIMARY KEY,
nombre VARCHAR2(30) NOT NULL UNIQUE,
web VARCHAR2(30) NULL,
tema VARCHAR2(30) NOT NULL,
periodicidad VARCHAR2(15) NOT NULL,
coordinador CHAR(9) NOT NULL UNIQUE,

CHECK (periodicidad IN ('Semanal', 'Quincenal', 'Mensual',
'Bimestral', 'Trimestral', 'Anual'))
);

CREATE TABLE NUMERO(
numero NUMBER(5) NOT NULL,
fecha DATE NOT NULL,
num_articulos NUMBER(4) NOT NULL,
revista CHAR(4) NOT NULL,
PRIMARY KEY(numero,revista),
CONSTRAINT numero_fk_revista
FOREIGN KEY (revista) REFERENCES REVISTA (idrev)
                      ON DELETE CASCADE,
                       -- ON UPDATE CASCADE--
CHECK (numero > 0),
CHECK (num_articulos >= 0)
);


CREATE TABLE ARTICULO (
idart CHAR(4) PRIMARY KEY,
titulo VARCHAR2(60) NOT NULL,
tipo VARCHAR2(15) NOT NULL,
revista CHAR(4) NULL,
numero NUMBER(5) NULL,
contratado CHAR(9) NULL,
freelance CHAR(9) NULL,
CONSTRAINT articulo_fk_numero
FOREIGN KEY (numero,revista) REFERENCES NUMERO (numero,revista),
                    -- ON DELETE NO ACTION, ON UPDATE CASCADE--
CHECK (tipo IN ('Opinion', 'Informacion', 'Analisis'))
);

CREATE TABLE CONTRATADO (
dni CHAR(9) PRIMARY KEY,
nombre VARCHAR2(30) NOT NULL,
email VARCHAR2(30) NOT NULL UNIQUE,
sueldo NUMBER(10, 3) NOT NULL,
fecha_contrato DATE NOT NULL,
revista CHAR(4) NOT NULL,
tutor CHAR(9) NULL,
CONSTRAINT contratado_fk_revista
FOREIGN KEY (revista) REFERENCES REVISTA (idrev),
 -- ON DELETE NO ACTION, ON UPDATE CASCADE--
CONSTRAINT contratado_fk_contratado
FOREIGN KEY (tutor) REFERENCES CONTRATADO(dni),
 -- ON DELETE NO ACTION, ON UPDATE CASCADE--
 
 CHECK (sueldo > 0),
 CHECK(dni<>tutor)
);

CREATE TABLE FREELANCE (
dni CHAR(9) PRIMARY KEY,
nombre VARCHAR2(30) NOT NULL,
email VARCHAR2(30) NOT NULL UNIQUE
);

CREATE TABLE COLABORACION(
revista CHAR(4) NOT NULL,
freelance CHAR(9) NOT NULL,
pago_articulo NUMBER(10,3) NOT NULL,
PRIMARY KEY(revista,freelance),
CONSTRAINT colaboracion_fk_revista
FOREIGN KEY (revista) REFERENCES REVISTA (idrev),
 -- ON DELETE NO ACTION, ON UPDATE CASCADE--
CONSTRAINT colaboracion_fk_freelance
FOREIGN KEY (freelance) REFERENCES FREELANCE (dni),
 -- ON DELETE NO ACTION, ON UPDATE CASCADE--
 
 CHECK (pago_articulo > 0)
);

ALTER TABLE REVISTA
    ADD CONSTRAINT  revista_fk_coordinador
        FOREIGN KEY(coordinador)
        REFERENCES CONTRATADO(dni);
        -- ON DELETE NO ACTION, ON UPDATE CASCADE--

UPDATE NUMERO
    SET num_articulos = (SELECT COUNT(*)
        FROM ARTICULO
        WHERE numero = NUMERO.numero 
            AND revista = NUMERO.revista );

ALTER TABLE ARTICULO
    ADD CONSTRAINT  articulo_fk_contratado
        FOREIGN KEY(contratado)
        REFERENCES CONTRATADO(dni);
        -- ON DELETE NO ACTION, ON UPDATE CASCADE--
        
ALTER TABLE ARTICULO
    ADD CONSTRAINT  articulo_fk_freelance
        FOREIGN KEY(freelance)
        REFERENCES FREELANCE(dni);
        -- ON DELETE NO ACTION, ON UPDATE CASCADE--
        
ALTER TABLE ARTICULO
ADD CONSTRAINT contratado_not_freelance
CHECK(
    (contratado IS NOT NULL AND freelance IS NULL)
    OR (contratado IS NULL AND freelance IS NOT NULL)
);
    
ALTER TABLE ARTICULO
ADD CONSTRAINT revista_y_numero
CHECK(
    (revista IS NOT NULL AND numero IS NOT NULL)
    OR (revista IS NULL AND numero IS NULL)
);