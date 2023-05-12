use examen_cd_python_flask;
-- delete from usuarios where id = 2;
-- select * from usuarios;
  -- delete from publicaciones where id = 11;

-- select * from usuarios;
 -- insert into publicaciones (cuerpo, id_autor, created_at, updated_at) values ('en la competencia de los mejores se obtiene la excelenecia',8,now(),now());
  -- update publicaciones set created_at = now(), updated_at = now() where id = 6;
  -- select * from usuarios;
--  select * from publicaciones;
-- select * from usuarios;
-- select * from megusta;

SELECT *, count(m.id_publicacion) FROM publicaciones p left join usuarios u on p.id_autor = u.id left join megusta m on p.id = m.id_publicacion group by m.id_publicacion;




-- delete from usuarios where id between 1 and 100;