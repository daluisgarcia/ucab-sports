
--Posts
INSERT INTO main_posts(titulo,resumen,cuerpo) VALUES('post de prueba', 'asdasdasd', 'más asdasdasd');
INSERT INTO main_posts(titulo,resumen,cuerpo) VALUES('otro post', 'asdasdasd', 'más asdasdasd');

--Fases
INSERT INTO main_fases(nombre, num_partidos) VALUES('Fase de prueba', 20);
INSERT INTO main_fases(nombre, num_partidos) VALUES('8vos de final', 4);

--Juego
INSERT INTO main_juegos(nombre) VALUES('Clash Royale');

--Organizador
INSERT INTO main_organizadores(usuario, contrasena) VALUES('Organizador1', '12345');

--Torneo
INSERT INTO main_torneos(id_juego_id, nombre, fecha_inicio, fecha_fin, edicion) VALUES (1, 'Un torneo', '13-01-2020', '27-09-2020', 4);