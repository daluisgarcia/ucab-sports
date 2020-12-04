
--Posts
INSERT INTO main_posts(titulo,cuerpo) VALUES('post de prueba', 'más asdasdasd');
INSERT INTO main_posts(titulo,cuerpo) VALUES('otro post', 'más asdasdasd');

--Fases
INSERT INTO main_fases(nombre, descripcion, equipos_por_grupo, num_grupos, part_por_equipo, equipos_por_partido) VALUES('Fase de prueba','esta fase es la primera de todas', 4, 8, 10, 2);
INSERT INTO main_fases(nombre, descripcion, equipos_por_grupo, num_grupos, part_por_equipo, equipos_por_partido) VALUES('8vos de final', 'fase para pasar a 8vos de final', 4, 8, 10, 2);

--Juego
INSERT INTO main_juegos(nombre) VALUES('Clash Royale');

--Organizador
INSERT INTO main_organizadores(usuario, contrasena) VALUES('Organizador1', '12345');

--Torneo
INSERT INTO main_torneos(id_juego_id, nombre, fecha_inicio, fecha_fin, edicion) VALUES (1, 'Un torneo', '13-01-2020', '27-09-2020', 4);