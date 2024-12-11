--(Bases de Datos I)
--Curso académico (2024/25) y convocatoria (enero).
--(P3. Definición y modificación de datos en SQL).
-- fichero bd1-p3-revistas.sql
-- Kateryna Pasternak y IVAN ANDRES YAGUAL MENDEZ

-- 2 --
SELECT f.dni, f.nombre, c.revista, c.pago_articulo 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
WHERE f.dni IN (
SELECT f.dni 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
GROUP BY f.dni
HAVING COUNT(f.dni) > 2); 

UPDATE COLABORACION SET pago_articulo = pago_articulo*1.03 
WHERE freelance  IN (
SELECT f.dni 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
GROUP BY f.dni
HAVING COUNT(f.dni) > 2);

SELECT f.dni, f.nombre, c.revista, c.pago_articulo 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
WHERE f.dni IN (
SELECT f.dni 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
GROUP BY f.dni
HAVING COUNT(f.dni) > 2); 

ROLLBACK;

SELECT f.dni, f.nombre, c.revista, c.pago_articulo 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
WHERE f.dni IN (
SELECT f.dni 
FROM FREELANCE f
JOIN COLABORACION c ON c.freelance = f.dni
GROUP BY f.dni
HAVING COUNT(f.dni) > 2); 

-- 2 --
ALTER TABLE CONTRATADO
DISABLE CONSTRAINT CONTRATADO_FK_CONTRATADO;
ALTER TABLE REVISTA
DISABLE CONSTRAINT revista_fk_coordinador;
ALTER TABLE ARTICULO
DISABLE CONSTRAINT ARTICULO_FK_CONTRATADO;

UPDATE ARTICULO SET contratado = '99001122P' WHERE contratado = '11223344P';
UPDATE CONTRATADO SET dni = '99001122P' WHERE dni = '11223344P';
UPDATE CONTRATADO SET tutor = '99001122P' WHERE tutor = '11223344P';
UPDATE REVISTA SET coordinador = '99001122P' WHERE coordinador = '11223344P';

ALTER TABLE CONTRATADO
ENABLE CONSTRAINT CONTRATADO_FK_CONTRATADO;
ALTER TABLE REVISTA
ENABLE CONSTRAINT revista_fk_coordinador;
ALTER TABLE ARTICULO
ENABLE CONSTRAINT ARTICULO_FK_CONTRATADO;

