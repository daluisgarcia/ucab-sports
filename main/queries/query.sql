
--Posts
INSERT INTO main_post(titulo,cuerpo) VALUES('post de prueba', 'más asdasdasd');
INSERT INTO main_post(titulo,cuerpo) VALUES('otro post', 'más asdasdasd');

--Fases
INSERT INTO main_stage(nombre, descripcion, equipos_por_grupo, num_grupos, part_por_equipo, equipos_por_partido) VALUES('Fase de prueba','esta fase es la primera de todas', 4, 8, 2, 2);
INSERT INTO main_stage(nombre, descripcion, equipos_por_grupo, num_grupos, part_por_equipo, equipos_por_partido) VALUES('8vos de final', 'fase para pasar a 8vos de final', 4, 8, 10, 2);

--Juego
INSERT INTO main_game(nombre) VALUES('Clash Royale');

--Organizador
INSERT INTO main_organizer(usuario, contrasena) VALUES('Organizador 1', '12345');
INSERT INTO main_organizer(usuario, contrasena) VALUES('Organizador 2', '12345');

--Torneo
INSERT INTO main_tournament(id_juego_id, nombre, fecha_inicio, fecha_fin, edicion) VALUES (1, 'Un torneo', '13-01-2020', '27-09-2020', 4);

--Preinscripcion
--INSERT INTO main_preteamregister(fecha_registro,rol,estatus,id_persona,id_equipo,id_torneo) VALUES ('2020-01-01','j','p',1,1,1);