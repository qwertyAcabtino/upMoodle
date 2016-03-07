PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(80) NOT NULL UNIQUE);
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"), UNIQUE ("group_id", "permission_id"));
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "group_id" integer NOT NULL REFERENCES "auth_group" ("id"), UNIQUE ("user_id", "group_id"));
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"), UNIQUE ("user_id", "permission_id"));
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO "django_session" VALUES('iweqy1uzvu8syfw4iilg3hu1age8grn6','NGNlMzY4ZmY3OGIzMTJlZDRjYjQ0NTIzZmVjMmQ5MGI2NjdiZDdhYjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5ZTMwMzhmN2I3M2MxOWRiNWQ4MzUxZDAwNzFlZjZiOTk2ODM5YWYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOjF9','2014-11-02 19:36:22.520742');
INSERT INTO "django_session" VALUES('9qey0aya5ii3qp8zwyors2l5m53zpnyh','NWRiZTM4MTc4Y2I4NTIyYWQ1MDI4NmRkMjYwYjNmZGZlNDMwOGNmMzp7fQ==','2014-11-09 18:22:44.238686');
INSERT INTO "django_session" VALUES('dr07caz6w4hmfwas1eotjkew5bf8a1st','NWRiZTM4MTc4Y2I4NTIyYWQ1MDI4NmRkMjYwYjNmZGZlNDMwOGNmMzp7fQ==','2014-11-09 18:33:46.824201');
CREATE TABLE "rest_leveltype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);
INSERT INTO "rest_leveltype" VALUES(1,'carrer');
INSERT INTO "rest_leveltype" VALUES(2,'course');
INSERT INTO "rest_leveltype" VALUES(3,'subject');
INSERT INTO "rest_leveltype" VALUES(4,'student');
INSERT INTO "rest_leveltype" VALUES(5,'university');
CREATE TABLE "rest_errormessage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "error" varchar(200) NOT NULL, "http_code" integer NOT NULL);
CREATE TABLE "rest_bannedhash" ("hash" varchar(65) NOT NULL PRIMARY KEY);
INSERT INTO "rest_bannedhash" VALUES('aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f');
INSERT INTO "rest_bannedhash" VALUES('b5d417261307d6902ec32a5355d056c647e101678b99106690ddd1953fd126f5');
CREATE TABLE "rest_filecomments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" datetime NOT NULL, "text" varchar(1000) NOT NULL, "idAuthor_id" integer NOT NULL REFERENCES "rest_user" ("id"), "idFile_id" integer NOT NULL REFERENCES "rest_file" ("id"));
CREATE TABLE "rest_filereportlist" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "comment" varchar(200) NOT NULL, "idFile_id" integer NOT NULL REFERENCES "rest_file" ("id"), "idReporter_id" integer NOT NULL REFERENCES "rest_user" ("id"));
CREATE TABLE "rest_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);
INSERT INTO "rest_tag" VALUES(1,'Notes');
INSERT INTO "rest_tag" VALUES(2,'Practices');
INSERT INTO "rest_tag" VALUES(3,'Bibliography');
INSERT INTO "rest_tag" VALUES(4,'Exams');
INSERT INTO "rest_tag" VALUES(5,'Others');
CREATE TABLE "rest_year" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "verbose" varchar(20) NOT NULL);
INSERT INTO "rest_year" VALUES(1,'2014/2015');
INSERT INTO "rest_year" VALUES(2,'2013/2015');
INSERT INTO "rest_year" VALUES(3,'2015/2016');
CREATE TABLE "rest_filetag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "idFile_id" integer NOT NULL REFERENCES "rest_file" ("id"), "idTag_id" integer NOT NULL REFERENCES "rest_tag" ("id"));
CREATE TABLE "rest_message" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "message" varchar(200) NOT NULL
);
INSERT INTO "rest_message" VALUES(1,'Successfully signed in');
INSERT INTO "rest_message" VALUES(2,'Email is now confirmed');
INSERT INTO "rest_message" VALUES(3,'A new password has been sent to your email adress. Check your inbox');
INSERT INTO "rest_message" VALUES(4,'Your user account has been removed.');
INSERT INTO "rest_message" VALUES(5,'Your profile has been updated');
INSERT INTO "rest_message" VALUES(6,'Note updated');
INSERT INTO "rest_message" VALUES(7,'The note is been removed');
INSERT INTO "rest_message" VALUES(8,'The calendar event is been removed');
INSERT INTO "rest_message" VALUES(9,'Calendar event has been updated.');
INSERT INTO "rest_message" VALUES(10,'The file has been removed');
INSERT INTO "rest_message" VALUES(11,'Account successfully validated.');
INSERT INTO "rest_message" VALUES(12,'Your note was successfully created');
INSERT INTO "rest_message" VALUES(13,'Your file was successfully uploaded');
INSERT INTO "rest_message" VALUES(14,'File''s info has been updated');
CREATE TABLE "rest_rol" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL,
    "priority" integer NOT NULL
);
INSERT INTO "rest_rol" VALUES(1,'Alumno',0);
INSERT INTO "rest_rol" VALUES(2,'Profesor',1);
INSERT INTO "rest_rol" VALUES(3,'Coordinador de asignatura',2);
INSERT INTO "rest_rol" VALUES(4,'Delegado de curso',3);
INSERT INTO "rest_rol" VALUES(5,'Administrador',4);
INSERT INTO "rest_rol" VALUES(6,'g0d',5);
CREATE TABLE "rest_calendarregularevent" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(200) NOT NULL,
    "text" varchar(2000) NOT NULL,
    "created" date NOT NULL,
    "lastUpdate" date NOT NULL,
    "author_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "lastUpdated_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "level_id" integer NOT NULL REFERENCES "rest_level" ("id"),
    "hourStart" time,
    "hourEnd" time,
    "firstDate" date NOT NULL,
    "lastDate" date,
    "allDay" bool NOT NULL,
    "frequency_id" integer NOT NULL REFERENCES "rest_calendarfrequency" ("id")
);
INSERT INTO "rest_calendarregularevent" VALUES(1,'Estadistica','Clases de estadistica de los lunes','2015-02-01','2015-02-01',1,1,1,'12:00:00','14:00:00','2015-02-01','2015-04-01',0,1);
CREATE TABLE "rest_calendarfrequency" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(50) NOT NULL
);
INSERT INTO "rest_calendarfrequency" VALUES(1,'daily');
INSERT INTO "rest_calendarfrequency" VALUES(2,'weekly');
INSERT INTO "rest_calendarfrequency" VALUES(3,'monthly');
INSERT INTO "rest_calendarfrequency" VALUES(4,'unique');
CREATE TABLE "rest_calendar" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(200) NOT NULL,
    "text" varchar(2000) NOT NULL,
    "created" date NOT NULL,
    "lastUpdate" date NOT NULL,
    "author_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "lastUpdated_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "level_id" integer NOT NULL REFERENCES "rest_level" ("id"),
    "hourStart" time,
    "hourEnd" time,
    "firstDate" date NOT NULL,
    "lastDate" date NOT NULL,
    "allDay" bool NOT NULL,
    "frequency_id" integer NOT NULL REFERENCES "rest_calendarfrequency" ("id")
);
INSERT INTO "rest_calendar" VALUES(1,'New calendar title','Description for this calendar event','2015-02-03','2015-02-10',1,1,1,'21:41:17','21:41:18','2015-02-03','2015-02-03',1,1);
INSERT INTO "rest_calendar" VALUES(2,'asdf','asdf','2015-02-03','2015-02-03',2,2,1,'21:51:01','21:51:02','2015-02-27','2015-03-06',1,1);
INSERT INTO "rest_calendar" VALUES(5,'asdfasdf','qwerqwer','2015-02-10','2015-02-10',1,1,1,'21:41:17','21:41:17','2015-02-03','2015-02-03',1,4);
INSERT INTO "rest_calendar" VALUES(6,'POST POST','qwerqwer','2015-02-10','2015-02-22',1,1,1,'21:41:17','21:41:17','2015-02-03','2015-02-03',1,4);
CREATE TABLE "rest_calendardate" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "calendarId_id" integer NOT NULL REFERENCES "rest_calendar" ("id"),
    "date" datetime NOT NULL
);
INSERT INTO "rest_calendardate" VALUES(2,2,'2015-02-27 00:00:00');
INSERT INTO "rest_calendardate" VALUES(5,2,'2015-03-02 00:00:00');
INSERT INTO "rest_calendardate" VALUES(6,2,'2015-03-03 00:00:00');
INSERT INTO "rest_calendardate" VALUES(7,2,'2015-03-04 00:00:00');
INSERT INTO "rest_calendardate" VALUES(8,2,'2015-03-05 00:00:00');
INSERT INTO "rest_calendardate" VALUES(9,2,'2015-03-06 00:00:00');
INSERT INTO "rest_calendardate" VALUES(28,1,'2015-02-03 00:00:00');
INSERT INTO "rest_calendardate" VALUES(29,5,'2015-02-03 00:00:00');
INSERT INTO "rest_calendardate" VALUES(31,6,'2015-02-03 00:00:00');
CREATE TABLE "rest_level" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(50) NOT NULL,
    "type_id" integer NOT NULL REFERENCES "rest_leveltype" ("id"),
    "visible" bool NOT NULL,
    "parent_id" integer REFERENCES "rest_level" ("id")
);
INSERT INTO "rest_level" VALUES(1,'Ingenieria del software',1,1,7);
INSERT INTO "rest_level" VALUES(2,'Ingenieria de computadores',1,1,7);
INSERT INTO "rest_level" VALUES(3,'3ro de software',2,1,1);
INSERT INTO "rest_level" VALUES(4,'Verificacion y Validacion',3,1,3);
INSERT INTO "rest_level" VALUES(5,'Calidad del software',3,1,3);
INSERT INTO "rest_level" VALUES(6,'Gestion de proyectos',3,1,3);
INSERT INTO "rest_level" VALUES(7,'UPM',5,1,NULL);
CREATE TABLE "corsheaders_corsmodel" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "cors" varchar(255) NOT NULL
);
CREATE TABLE "rest_user_subjects" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" integer NOT NULL,
    "level_id" integer NOT NULL REFERENCES "rest_level" ("id"),
    UNIQUE ("user_id", "level_id")
);
INSERT INTO "rest_user_subjects" VALUES(5,2,1);
INSERT INTO "rest_user_subjects" VALUES(273,3,4);
INSERT INTO "rest_user_subjects" VALUES(274,3,5);
INSERT INTO "rest_user_subjects" VALUES(275,3,6);
INSERT INTO "rest_user_subjects" VALUES(294,1,4);
INSERT INTO "rest_user_subjects" VALUES(295,1,5);
INSERT INTO "rest_user_subjects" VALUES(296,1,6);
INSERT INTO "rest_user_subjects" VALUES(305,5,4);
INSERT INTO "rest_user_subjects" VALUES(306,5,5);
INSERT INTO "rest_user_subjects" VALUES(307,5,6);
CREATE TABLE "rest_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "rol_id" integer NOT NULL REFERENCES "rest_rol" ("id"),
    "email" varchar(100) NOT NULL UNIQUE,
    "nick" varchar(20) NOT NULL UNIQUE,
    "name" varchar(100) NOT NULL,
    "password" varchar(100) NOT NULL,
    "profilePic" varchar(100) NOT NULL,
    "lastTimeActive" datetime NOT NULL,
    "joined" datetime NOT NULL,
    "banned" bool NOT NULL,
    "confirmedEmail" bool NOT NULL,
    "sessionToken" varchar(256) NOT NULL UNIQUE
);
INSERT INTO "rest_user" VALUES(1,6,'viperey@alumnos.upm.es','viperey','Victor Perez Rey','qwerqwer','pics/users/arda-425467.jpg','2016-02-18 19:05:47.228188','2015-03-04 13:30:32',0,1,'.eJxVzEEOwiAQheG7zNoQBsQGl-49AxmYQaoGktKujHe3Tbqo6_d_7wOBlrmEpcsUCvUCV6CsRfzZOYfWZL6g1Ymyt0a81W5AGkziiBlORxwpvaTy6vlJ9dFUanWexqi2RO1rV_fG8r7t7d_BuFmE7w_pKTE0:1aWSU5:q3xhs2YhjGiciFcDpi2eT2vUa40');
INSERT INTO "rest_user" VALUES(2,1,'asdfasd@alumnos.upm.es','qwerqwer','','qwerqwer','_default.png','2015-03-04 13:31:59','2015-03-04 13:31:59',0,0,'.eJxVi70OwiAQgN_lZkMglxbo6O4zEI47pGogKe1kfHdt0qGu388bQtzWErYuSyixF5iAvKBGly1ZTMYzDexwMKy1NZJH8n506GOGy3meGSbzRyimp9QfBn7Eem8qtbouM6k9UYft6tZYXtej_XwBZ48w3w:1YT9Or:JJm7SkZVxAqnADr-Yr9r1QQo-pY');
INSERT INTO "rest_user" VALUES(3,1,'victoereno@eui.upm.es','mlmlfemf','asdfasdf asdf asd','qwerqwer','_default.png','2015-04-26 12:02:50.220249','2015-03-04 13:39:12',0,1,'e30:1YmLGo:qgdTQcy-Rv7kEtoQ2FtPkxDLmfk');
INSERT INTO "rest_user" VALUES(4,1,'asdf@alumnos.upm.es','qwer','qwerqwe','qwerqwer','pics/users/_default.png','2015-04-26 13:49:48.448076','2015-04-26 13:49:16',0,1,'e30:1YmMwL:-1SmZ4xargcMAS0LbhW3IQfNklY');
INSERT INTO "rest_user" VALUES(5,1,'victor.perezr@alumnos.upm.es','vipvip','vip vip','qwerqwer','pics/users/1854070.jpg','2016-03-06 17:43:59.686237','2015-05-10 15:17:00',0,1,'.eJxVi70OgyAQgN-F2RAOSg0du_cZyMEdojaQiE5N372aONj1-_kIj9ua_dZ48RlbFg-BSTG7m7UWjE50B6MiJmc0O6NsD9jrSAGS6K7zSPsK_yxgnLkcgiYsQ5WxlnUZgzwSedomX5X4_Tzb7w-wKzE0:1acciX:3j-cbf69a23QZSvIwQK3qWVFGiQ');
CREATE TABLE "rest_noteboard" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "topic" varchar(100) NOT NULL,
    "text" varchar(2000) NOT NULL,
    "level_id" integer NOT NULL REFERENCES "rest_level" ("id"),
    "author_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "visible" bool NOT NULL,
    "authorized" bool NOT NULL,
    "created" datetime NOT NULL
);
INSERT INTO "rest_noteboard" VALUES(1,'qwer2','qwerqwer',1,1,1,1,'2015-04-13 13:31:19');
INSERT INTO "rest_noteboard" VALUES(2,'asdf','sdfasdf',2,1,1,1,'2015-04-13 13:33:36');
INSERT INTO "rest_noteboard" VALUES(3,'asdf','asdfa',3,1,1,1,'2015-04-13 13:33:52.576212');
INSERT INTO "rest_noteboard" VALUES(4,'Lastest','.',1,1,1,1,'2015-04-13 13:44:33.743823');
INSERT INTO "rest_noteboard" VALUES(5,'Lastest lastest','.asdfas',3,1,1,1,'2015-04-13 13:46:14.239982');
INSERT INTO "rest_noteboard" VALUES(6,'asdf','asdf',1,1,1,1,'2015-04-13 23:51:21.448678');
INSERT INTO "rest_noteboard" VALUES(7,'asdf','asdfasdf',1,1,0,1,'2015-04-14 00:05:12.293724');
INSERT INTO "rest_noteboard" VALUES(8,'Note','Message',3,1,0,1,'2015-04-14 00:06:12.817530');
INSERT INTO "rest_noteboard" VALUES(9,'asdf','asdf',7,1,0,1,'2015-04-26 13:02:27.024524');
INSERT INTO "rest_noteboard" VALUES(10,'asdf','asdfasdf',1,1,1,1,'2015-05-10 13:33:33.028163');
CREATE TABLE "rest_filetype" (
    "name" varchar(20) NOT NULL,
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT
);
INSERT INTO "rest_filetype" VALUES('Theory',1);
INSERT INTO "rest_filetype" VALUES('Practice',2);
INSERT INTO "rest_filetype" VALUES('Classwork',3);
INSERT INTO "rest_filetype" VALUES('Bibliography',4);
INSERT INTO "rest_filetype" VALUES('Exam',5);
INSERT INTO "rest_filetype" VALUES('Exercise',6);
CREATE TABLE "rest_file" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "subject_id" integer NOT NULL REFERENCES "rest_level" ("id"),
    "hash" varchar(65) NOT NULL,
    "name" varchar(100) NOT NULL,
    "year_id" integer NOT NULL REFERENCES "rest_year" ("id"),
    "fileType_id" integer NOT NULL REFERENCES "rest_filetype" ("id"),
    "uploaded" datetime NOT NULL,
    "uploader_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "lastUpdate" datetime NOT NULL,
    "lastUpdater_id" integer NOT NULL REFERENCES "rest_user" ("id"),
    "visible" bool NOT NULL,
    "file" varchar(100) NOT NULL,
    "text" varchar(2000) NOT NULL
);
INSERT INTO "rest_file" VALUES(1,6,'7528590d779aae2af62b3d78fe6a0fbbd15c195b2ae9eaaadbd91b1336a6ae11','Horario',1,1,'2015-04-15 02:06:01.549045',1,'2015-04-15 02:06:01.549104',1,1,'files/7528590d779aae2af62b3d78fe6a0fbbd15c195b2ae9eaaadbd91b1336a6ae11.png','');
INSERT INTO "rest_file" VALUES(2,6,'0d54f77bf7b343eaa44a75e97d5009eab9ca4f1c83296eedf24c11747f40b491','bla',1,2,'2015-04-15 02:12:17.696964',1,'2015-04-16 16:09:33.893755',1,1,'files/0d54f77bf7b343eaa44a75e97d5009eab9ca4f1c83296eedf24c11747f40b491.sublime-project','blabla');
INSERT INTO "rest_file" VALUES(3,6,'b60c283e959c2558f0896cc9d6bae5bb81fbcc08c14ed79d65a87a9cfcd97b13','bower',1,1,'2015-04-16 16:25:40.758247',1,'2015-04-16 16:25:40.758327',1,1,'files/b60c283e959c2558f0896cc9d6bae5bb81fbcc08c14ed79d65a87a9cfcd97b13.json','');
INSERT INTO "rest_file" VALUES(4,6,'27f17c59cc854d8541f7ca879fd2ca56e370a425ddb70580f49e5b068d8dca1a','LICENSE',1,1,'2015-04-16 16:25:40.768219',1,'2015-04-16 16:25:40.768313',1,1,'files/27f17c59cc854d8541f7ca879fd2ca56e370a425ddb70580f49e5b068d8dca1a.LICENSE','');
INSERT INTO "rest_file" VALUES(5,6,'6caee45251954f251fa4b8d0bdb898d5b1f87666d383ea1f216bf89242f197a2','CHANGELOG',1,1,'2015-04-16 16:25:40.771430',1,'2015-04-16 16:25:40.771590',1,1,'files/6caee45251954f251fa4b8d0bdb898d5b1f87666d383ea1f216bf89242f197a2.md','');
INSERT INTO "rest_file" VALUES(6,6,'6caee45251954f251fa4b8d0bdb898d5b1f87666d383ea1f216bf89242f197a2','CHANGELOG',1,1,'2015-04-16 19:04:02.725702',1,'2015-04-16 19:04:02.725789',1,1,'files/6caee45251954f251fa4b8d0bdb898d5b1f87666d383ea1f216bf89242f197a2_yK0A4Qv.md','');
INSERT INTO "rest_file" VALUES(7,6,'b60c283e959c2558f0896cc9d6bae5bb81fbcc08c14ed79d65a87a9cfcd97b13','bower',1,1,'2015-04-16 19:04:02.922797',1,'2015-04-16 19:04:02.922911',1,1,'files/b60c283e959c2558f0896cc9d6bae5bb81fbcc08c14ed79d65a87a9cfcd97b13_nhzr3nY.json','');
INSERT INTO "rest_file" VALUES(8,6,'27f17c59cc854d8541f7ca879fd2ca56e370a425ddb70580f49e5b068d8dca1a','LICENSE',1,5,'2015-04-16 19:04:03.163569',1,'2015-04-25 22:16:24.319327',1,1,'files/27f17c59cc854d8541f7ca879fd2ca56e370a425ddb70580f49e5b068d8dca1a_ODlxbL9.LICENSE','tEST');
INSERT INTO "rest_file" VALUES(9,6,'6523dc5d228b5d09031c29e23a3362120ede559facd5b70fcf242cb98654936b','Ciutat Morta (2014)(Spa + Sub Eng)(360p)(H',1,1,'2015-04-16 19:06:03.111833',1,'2015-04-16 19:06:03.111895',1,1,'files/6523dc5d228b5d09031c29e23a3362120ede559facd5b70fcf242cb98654936b.mp4','');
INSERT INTO "rest_file" VALUES(10,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:40:13.556031',1,'2015-04-25 22:40:13.556069',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4.jpg','');
INSERT INTO "rest_file" VALUES(11,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:41:19.137011',1,'2015-04-25 22:41:19.137076',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_p4txx9U.jpg','');
INSERT INTO "rest_file" VALUES(12,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:41:28.256647',1,'2015-04-25 22:41:28.256710',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_oro9nEj.jpg','');
INSERT INTO "rest_file" VALUES(13,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:42:53.759096',1,'2015-04-25 22:42:53.759178',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_Hf4R9aI.jpg','');
INSERT INTO "rest_file" VALUES(14,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:42:56.982471',1,'2015-04-25 22:42:56.982515',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_sDysSZ4.jpg','');
INSERT INTO "rest_file" VALUES(15,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:43:17.925390',1,'2015-04-25 22:43:17.925443',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_vAHkAWN.jpg','');
INSERT INTO "rest_file" VALUES(16,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:44:04.146339',1,'2015-04-25 22:44:04.146451',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_ccYxe5s.jpg','');
INSERT INTO "rest_file" VALUES(17,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00',1,1,'2015-04-25 22:44:10.286766',1,'2015-04-25 22:44:10.286994',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_6xfJ5iV.jpg','');
INSERT INTO "rest_file" VALUES(18,6,'17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8','Sin título-1',1,1,'2015-04-25 22:44:28.308755',1,'2015-04-25 22:44:28.308824',1,1,'files/17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8.png','');
INSERT INTO "rest_file" VALUES(19,6,'17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8','Sin título-1',1,1,'2015-04-25 22:45:26.075854',1,'2015-04-25 22:45:26.075919',1,1,'files/17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8_h1kJxLL.png','');
INSERT INTO "rest_file" VALUES(20,6,'17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8','Sin título-1',1,1,'2015-04-25 22:45:44.700864',1,'2015-04-25 22:45:44.701002',1,1,'files/17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8_dRHqGjJ.png','');
INSERT INTO "rest_file" VALUES(21,6,'1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851','EM275797',1,1,'2015-04-25 22:46:45.084068',1,'2015-04-25 22:46:45.084135',1,1,'files/1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851.pdf','');
INSERT INTO "rest_file" VALUES(22,6,'1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851','EM275797',1,1,'2015-04-25 22:47:34.400033',1,'2015-04-25 22:47:34.400075',1,1,'files/1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851_7r6eyxd.pdf','');
INSERT INTO "rest_file" VALUES(23,6,'1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851','pedeefe.pdf',1,1,'2015-04-25 22:48:49.420623',1,'2015-04-25 22:48:49.420712',1,1,'files/1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851_wUpML4q.pdf','');
INSERT INTO "rest_file" VALUES(24,6,'1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851','EM275797.pdf',1,3,'2015-04-25 22:50:24.058695',1,'2015-04-25 22:50:24.058776',1,1,'files/1a34c97ed7d37e927c867983064680580f4f057d571598be6339db5474b7c851_yo2UfaR.pdf','');
INSERT INTO "rest_file" VALUES(25,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00.jpg',1,5,'2015-04-25 22:50:34.984835',1,'2015-04-25 22:50:34.984878',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_Gm2Xsmq.jpg','');
INSERT INTO "rest_file" VALUES(26,6,'17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8','Sin título-1.png',1,1,'2015-04-25 22:51:20.975158',1,'2015-04-25 22:51:20.975227',1,1,'files/17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8_vm64BQd.png','');
INSERT INTO "rest_file" VALUES(27,6,'17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8','Sin título-1.png',1,1,'2015-04-25 22:51:41.697013',1,'2015-04-25 22:51:41.697055',1,1,'files/17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8_xhiaDF7.png','');
INSERT INTO "rest_file" VALUES(28,6,'17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8','Sin título-1.png',1,1,'2015-04-25 22:52:24.653703',1,'2015-04-25 22:52:24.653768',1,1,'files/17d7dcf236c072d63bfa172771ab0e3cbd2e7c34c29929079951408b420b22a8_2GPfxfZ.png','');
INSERT INTO "rest_file" VALUES(29,6,'a25b037eb8e80d793bd77230c90d6bb7b22d27b0f8c639b087553afc278437b3','xbmc_crashlog-20150314_223839.log',1,5,'2015-04-25 22:52:35.510490',1,'2015-04-25 22:52:35.510566',1,1,'files/a25b037eb8e80d793bd77230c90d6bb7b22d27b0f8c639b087553afc278437b3.log','');
INSERT INTO "rest_file" VALUES(30,6,'7533c8b5adcdbb17152f0a6a0f7397eb4387107773bf4f618f26ef9d6eb07674','xbmc_crashlog-20150131_212200.log',1,4,'2015-04-25 22:52:38.675933',1,'2015-04-25 22:52:38.675995',1,1,'files/7533c8b5adcdbb17152f0a6a0f7397eb4387107773bf4f618f26ef9d6eb07674.log','');
INSERT INTO "rest_file" VALUES(31,6,'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','output',1,1,'2015-04-25 22:54:28.184368',1,'2015-04-25 22:54:28.184415',1,1,'files/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.txt','');
INSERT INTO "rest_file" VALUES(32,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00.jpg',1,1,'2015-04-25 22:55:45.128721',1,'2015-04-25 22:58:04.002023',1,0,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_Gu3Y9FA.jpg','');
INSERT INTO "rest_file" VALUES(33,6,'f2ef80068762f9298b95691f3885bbe9d4f1c5f2ef725ab7d88c77a3f26f8b54','Screenshot from 2015-04-09 16:52:20.png',1,1,'2015-04-26 13:44:10.012742',1,'2015-04-26 13:44:10.013177',1,1,'files/f2ef80068762f9298b95691f3885bbe9d4f1c5f2ef725ab7d88c77a3f26f8b54.png','');
INSERT INTO "rest_file" VALUES(34,6,'2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4','logo-00.jpg',1,1,'2015-04-26 17:00:53.136575',1,'2015-04-26 17:00:53.136928',1,1,'files/2c08e343954db43c5151fc5d8dcfd71e00f3f2685b1cf5c484d683fe3b7d53a4_edt3VCE.jpg','');
INSERT INTO "rest_file" VALUES(35,6,'59a8439928f95d2e9e62ea90ec5ca338215e7832ea828a7ed63ca1ed30653f29','install.sh',1,2,'2015-05-05 13:46:53.416028',1,'2015-05-05 13:47:04.292168',1,1,'files/59a8439928f95d2e9e62ea90ec5ca338215e7832ea828a7ed63ca1ed30653f29.sh','asdfasdf');
INSERT INTO "rest_file" VALUES(36,5,'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','output.txt',1,1,'2015-05-11 22:27:03.839168',5,'2015-05-11 22:27:03.839300',5,1,'files/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855_EpfH6Yr.txt','');
INSERT INTO "rest_file" VALUES(37,5,'78b704464ae8c567788558a51963642168f4d67427a11d7755b26814a7964e71','asdfasdf.png',3,6,'2016-03-03 18:01:36.434918',5,'2016-03-03 18:01:36.434951',5,1,'files/78b704464ae8c567788558a51963642168f4d67427a11d7755b26814a7964e71.png','');
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO "django_migrations" VALUES(1,'rest','0001_initial','2016-03-06 23:02:11.797873');
INSERT INTO "django_migrations" VALUES(2,'rest','0002_auto_20160306_2304','2016-03-06 23:05:02.431270');
INSERT INTO "django_migrations" VALUES(3,'contenttypes','0001_initial','2016-03-06 23:07:32.139015');
INSERT INTO "django_migrations" VALUES(4,'auth','0001_initial','2016-03-06 23:07:32.165259');
INSERT INTO "django_migrations" VALUES(5,'admin','0001_initial','2016-03-06 23:07:32.179855');
INSERT INTO "django_migrations" VALUES(6,'admin','0002_logentry_remove_auto_add','2016-03-06 23:07:32.208281');
INSERT INTO "django_migrations" VALUES(7,'contenttypes','0002_remove_content_type_name','2016-03-06 23:07:32.252769');
INSERT INTO "django_migrations" VALUES(8,'auth','0002_alter_permission_name_max_length','2016-03-06 23:07:32.279919');
INSERT INTO "django_migrations" VALUES(9,'auth','0003_alter_user_email_max_length','2016-03-06 23:07:32.318890');
INSERT INTO "django_migrations" VALUES(10,'auth','0004_alter_user_username_opts','2016-03-06 23:07:32.341082');
INSERT INTO "django_migrations" VALUES(11,'auth','0005_alter_user_last_login_null','2016-03-06 23:07:32.364464');
INSERT INTO "django_migrations" VALUES(12,'auth','0006_require_contenttypes_0002','2016-03-06 23:07:32.372005');
INSERT INTO "django_migrations" VALUES(13,'auth','0007_alter_validators_add_error_messages','2016-03-06 23:07:32.443934');
INSERT INTO "django_migrations" VALUES(14,'sessions','0001_initial','2016-03-06 23:07:32.638409');
INSERT INTO "django_migrations" VALUES(15,'sites','0001_initial','2016-03-06 23:07:32.647898');
INSERT INTO "django_migrations" VALUES(16,'sites','0002_alter_domain_unique','2016-03-06 23:07:32.665761');
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id"), "user_id" integer NOT NULL REFERENCES "auth_user" ("id"), "action_time" datetime NOT NULL);
INSERT INTO "django_admin_log" VALUES(1,'1','carrer',1,'',10,1,'2014-10-19 19:30:22.310998');
INSERT INTO "django_admin_log" VALUES(2,'2','course',1,'',10,1,'2014-10-19 19:30:36.160617');
INSERT INTO "django_admin_log" VALUES(3,'3','subject',1,'',10,1,'2014-10-19 19:30:41.147819');
INSERT INTO "django_admin_log" VALUES(4,'1','Ingenieria del Software',2,'Changed type.',9,1,'2014-10-19 19:36:29.566632');
INSERT INTO "django_admin_log" VALUES(5,'1','1st topic',1,'',11,1,'2014-10-19 19:37:24.895118');
INSERT INTO "django_admin_log" VALUES(6,'1','1st topic for Ig. Software',2,'Changed topic.',11,1,'2014-10-19 19:37:40.973835');
INSERT INTO "django_admin_log" VALUES(7,'2','2nd for Ig del software',1,'',11,1,'2014-10-19 21:44:03.369356');
INSERT INTO "django_admin_log" VALUES(8,'2','Ingenieria de computadores',1,'',9,1,'2014-10-19 22:08:32.258207');
INSERT INTO "django_admin_log" VALUES(9,'3','1st for computadores',1,'',11,1,'2014-10-19 22:08:50.170917');
INSERT INTO "django_admin_log" VALUES(10,'b5d417261307d6902ec32a5355d056c647e101678b99106690ddd1953fd126f5','b5d417261307d6902ec32a5355d056c647e101678b99106690ddd1953fd126f5',1,'',13,1,'2014-10-22 21:35:47.732058');
INSERT INTO "django_admin_log" VALUES(11,'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f','aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f',1,'',13,1,'2014-10-22 21:36:01.046084');
INSERT INTO "django_admin_log" VALUES(12,'1','g0d',1,'',14,1,'2014-10-22 22:18:54.746710');
INSERT INTO "django_admin_log" VALUES(13,'2','alumno',1,'',14,1,'2014-10-22 22:19:18.311733');
INSERT INTO "django_admin_log" VALUES(14,'3','profesor',1,'',14,1,'2014-10-22 22:19:34.932218');
INSERT INTO "django_admin_log" VALUES(15,'4','Coordinador de asignatura',1,'',14,1,'2014-10-22 22:19:45.086062');
INSERT INTO "django_admin_log" VALUES(16,'5','Delegado de curso',1,'',14,1,'2014-10-22 22:19:52.273794');
INSERT INTO "django_admin_log" VALUES(17,'6','Adminstrador',1,'',14,1,'2014-10-22 22:20:00.662862');
INSERT INTO "django_admin_log" VALUES(18,'3','Profesor',2,'Changed name.',14,1,'2014-10-22 22:20:18.173981');
INSERT INTO "django_admin_log" VALUES(19,'3','Profesor',2,'No fields changed.',14,1,'2014-10-22 22:20:20.427917');
INSERT INTO "django_admin_log" VALUES(20,'2','Alumno',2,'Changed name.',14,1,'2014-10-22 22:20:26.260484');
INSERT INTO "django_admin_log" VALUES(21,'2','Alumno',2,'No fields changed.',14,1,'2014-10-22 22:20:28.495972');
INSERT INTO "django_admin_log" VALUES(22,'1','viperey',1,'',15,1,'2014-10-22 22:26:44.709114');
INSERT INTO "django_admin_log" VALUES(23,'2','pGomez',1,'',15,1,'2014-10-22 22:27:10.361387');
INSERT INTO "django_admin_log" VALUES(25,'1','viperey',2,'Changed profilePic.',15,1,'2014-10-26 11:35:17.312353');
INSERT INTO "django_admin_log" VALUES(26,'1','viperey',2,'Changed profilePic.',15,1,'2014-10-26 11:36:52.808163');
INSERT INTO "django_admin_log" VALUES(27,'1','daily',1,'',19,1,'2014-10-26 11:46:15.947196');
INSERT INTO "django_admin_log" VALUES(28,'2','weekly',1,'',19,1,'2014-10-26 11:46:22.068362');
INSERT INTO "django_admin_log" VALUES(29,'3','monthly',1,'',19,1,'2014-10-26 11:46:26.573183');
INSERT INTO "django_admin_log" VALUES(30,'4','unique',1,'',19,1,'2014-10-26 11:47:07.528912');
INSERT INTO "django_admin_log" VALUES(34,'1','Notes',1,'',23,1,'2014-10-26 12:59:02.334914');
INSERT INTO "django_admin_log" VALUES(35,'2','Practices',1,'',23,1,'2014-10-26 12:59:17.254599');
INSERT INTO "django_admin_log" VALUES(36,'3','Bibliography',1,'',23,1,'2014-10-26 12:59:42.526250');
INSERT INTO "django_admin_log" VALUES(37,'4','Exams',1,'',23,1,'2014-10-26 13:00:09.803343');
INSERT INTO "django_admin_log" VALUES(38,'5','Others',1,'',23,1,'2014-10-26 13:00:13.491021');
INSERT INTO "django_admin_log" VALUES(39,'3','Verificacion y Validacion del software',1,'',9,1,'2014-10-26 13:01:11.766444');
INSERT INTO "django_admin_log" VALUES(40,'1','2014/2015',1,'',21,1,'2014-10-26 13:01:44.413673');
INSERT INTO "django_admin_log" VALUES(41,'1','Practica 1',1,'',22,1,'2014-10-26 13:02:36.926801');
INSERT INTO "django_admin_log" VALUES(43,'2','Apuntes 1',1,'',22,1,'2014-10-26 15:50:36.827409');
INSERT INTO "django_admin_log" VALUES(44,'1','viperey',2,'Changed sessionToken.',15,1,'2014-10-26 23:01:22.218494');
INSERT INTO "django_admin_log" VALUES(45,'1','asdfasdf',1,'',29,1,'2014-11-02 14:54:44.818432');
INSERT INTO "django_admin_log" VALUES(46,'1','asdfasdf',3,'',29,1,'2014-11-02 14:55:23.437082');
INSERT INTO "django_admin_log" VALUES(47,'1','ssadfasdf',1,'',29,1,'2014-11-02 15:10:33.831049');
INSERT INTO "django_admin_log" VALUES(48,'1','Request cannot be performed',1,'',28,1,'2014-11-02 15:27:30.327844');
INSERT INTO "django_admin_log" VALUES(49,'2','Incorrect data',1,'',28,1,'2014-11-02 15:27:38.526901');
INSERT INTO "django_admin_log" VALUES(50,'3','Cookies disabled',1,'',28,1,'2014-11-02 15:27:44.003180');
INSERT INTO "django_admin_log" VALUES(51,'4','Already confirmed',1,'',28,1,'2014-11-02 15:27:49.838172');
INSERT INTO "django_admin_log" VALUES(52,'5','Invalid token',1,'',28,1,'2014-11-02 15:27:55.826860');
INSERT INTO "django_admin_log" VALUES(53,'6','User already in use',1,'',28,1,'2014-11-02 15:28:03.090438');
INSERT INTO "django_admin_log" VALUES(54,'7','Unauthorized',1,'',28,1,'2014-11-02 15:28:07.828015');
INSERT INTO "django_admin_log" VALUES(55,'8','Incorrect file data',1,'',28,1,'2014-11-02 15:28:13.762621');
INSERT INTO "django_admin_log" VALUES(56,'9','Password length has to be at least 8 chars long',1,'',28,1,'2014-11-02 18:36:07.236229');
INSERT INTO "django_admin_log" VALUES(57,'10','NICK_LENGTH',1,'',28,1,'2014-11-02 19:48:21.244521');
INSERT INTO "django_admin_log" VALUES(58,'10','Nickname length has to be at least 4 chars long.',2,'Changed error.',28,1,'2014-11-02 20:09:44.785356');
INSERT INTO "django_admin_log" VALUES(59,'11','Email field cannot be empty',1,'',28,1,'2014-11-02 23:24:53.652519');
INSERT INTO "django_admin_log" VALUES(60,'10','Nickname''s length has to be between 4 and 20',2,'Changed error.',28,1,'2014-11-02 23:45:24.152021');
INSERT INTO "django_admin_log" VALUES(61,'9','Password''s length has to be between 8 and 100',2,'Changed error.',28,1,'2014-11-02 23:47:10.457912');
INSERT INTO "django_admin_log" VALUES(62,'15','qwerqwer',3,'',15,1,'2014-11-16 01:07:47.130082');
INSERT INTO "django_admin_log" VALUES(63,'14','asasdfsadfasd',3,'',15,1,'2014-11-16 01:07:47.273810');
INSERT INTO "django_admin_log" VALUES(64,'13','vipvip',3,'',15,1,'2014-11-16 01:07:47.430737');
INSERT INTO "django_admin_log" VALUES(65,'12','asasdf',3,'',15,1,'2014-11-16 01:07:47.585912');
INSERT INTO "django_admin_log" VALUES(66,'11','',3,'',15,1,'2014-11-16 01:07:47.744499');
INSERT INTO "django_admin_log" VALUES(67,'10','sdfasdfasdf',3,'',15,1,'2014-11-16 01:07:47.912156');
INSERT INTO "django_admin_log" VALUES(68,'9','vipasdfasdfasdf',3,'',15,1,'2014-11-16 01:07:48.064651');
INSERT INTO "django_admin_log" VALUES(69,'8','vip',3,'',15,1,'2014-11-16 01:07:48.377042');
INSERT INTO "django_admin_log" VALUES(70,'7','vip',3,'',15,1,'2014-11-16 01:07:48.512446');
INSERT INTO "django_admin_log" VALUES(71,'6','vip',3,'',15,1,'2014-11-16 01:07:48.645581');
INSERT INTO "django_admin_log" VALUES(72,'5','vip',3,'',15,1,'2014-11-16 01:07:48.790704');
INSERT INTO "django_admin_log" VALUES(73,'4','vip',3,'',15,1,'2014-11-16 01:07:49.055364');
INSERT INTO "django_admin_log" VALUES(74,'3','vip',3,'',15,1,'2014-11-16 01:07:49.249736');
INSERT INTO "django_admin_log" VALUES(75,'1','viperey',2,'Changed email.',15,1,'2014-11-16 01:08:00.431777');
INSERT INTO "django_admin_log" VALUES(76,'16','qwerqwereerer',3,'',15,1,'2014-11-16 01:09:25.302752');
INSERT INTO "django_admin_log" VALUES(77,'17','qwerqwereerer',3,'',15,1,'2014-11-16 01:13:20.536909');
INSERT INTO "django_admin_log" VALUES(78,'18','qwerqwereerer',3,'',15,1,'2014-11-16 01:13:43.507004');
INSERT INTO "django_admin_log" VALUES(79,'19','qwerqwereerer',3,'',15,1,'2014-11-16 01:46:26.989223');
INSERT INTO "django_admin_log" VALUES(80,'4','This used is already confirmed',2,'Changed error.',28,1,'2014-11-16 02:06:52.165543');
INSERT INTO "django_admin_log" VALUES(81,'4','This user is already confirmed',2,'Changed error.',28,1,'2014-11-16 14:56:46.140759');
INSERT INTO "django_admin_log" VALUES(82,'1','Succesfull',2,'Changed message.',29,1,'2014-11-16 15:15:18.699786');
INSERT INTO "django_admin_log" VALUES(83,'1','Successfully loging in',2,'Changed message.',29,1,'2014-11-16 15:15:44.784799');
INSERT INTO "django_admin_log" VALUES(84,'2','Email is now confirmed',1,'',29,1,'2014-11-16 15:17:33.404361');
INSERT INTO "django_admin_log" VALUES(85,'1','Successfully signed in',2,'Changed message.',29,1,'2014-11-16 15:18:30.080321');
INSERT INTO "django_admin_log" VALUES(86,'12','Please, check your inbox and confirm your email.',1,'',28,1,'2014-11-16 15:34:15.081426');
INSERT INTO "django_admin_log" VALUES(87,'1','viperey',1,'',15,1,'2014-11-16 15:48:19.649884');
INSERT INTO "django_admin_log" VALUES(88,'1','viperey',3,'',15,1,'2014-11-16 15:48:40.358489');
INSERT INTO "django_admin_log" VALUES(89,'2','Provided data is incorrect',2,'Changed error.',28,1,'2014-11-16 15:51:48.670955');
INSERT INTO "django_admin_log" VALUES(90,'2','viperey',2,'Changed sessionToken.',15,1,'2014-11-16 19:28:43.249125');
INSERT INTO "django_admin_log" VALUES(91,'3','A new password has been sent to your email adress. Check your inbox',1,'',29,1,'2014-11-16 22:46:41.073093');
INSERT INTO "django_admin_log" VALUES(92,'2','viperey',2,'Changed password.',15,1,'2014-11-16 23:05:38.032732');
INSERT INTO "django_admin_log" VALUES(93,'13','Please, sign in first',1,'',28,1,'2014-11-21 23:48:26.876861');
INSERT INTO "django_admin_log" VALUES(94,'3','qwerqwer',1,'',15,1,'2014-11-23 16:56:30.901496');
INSERT INTO "django_admin_log" VALUES(95,'4','qwerqwer',1,'',15,1,'2014-11-23 16:57:18.831254');
INSERT INTO "django_admin_log" VALUES(97,'4','Your user account has been removed.',1,'',29,1,'2014-11-23 17:18:11.859759');
INSERT INTO "django_admin_log" VALUES(98,'5','Testuser',2,'Changed confirmedEmail.',15,1,'2014-11-23 17:43:23.948222');
INSERT INTO "django_admin_log" VALUES(99,'5','Your profile has been updated',1,'',29,1,'2014-11-23 20:29:00.671369');
INSERT INTO "django_admin_log" VALUES(100,'3','1st for computadores',3,'',11,1,'2014-11-23 21:55:07.477704');
INSERT INTO "django_admin_log" VALUES(101,'2','2nd for Ig del software',3,'',11,1,'2014-11-23 21:55:07.654855');
INSERT INTO "django_admin_log" VALUES(102,'1','1st topic for Ig. Software',3,'',11,1,'2014-11-23 21:55:07.999357');
INSERT INTO "django_admin_log" VALUES(103,'1','Topic',1,'',11,1,'2014-11-23 22:22:03.610982');
INSERT INTO "django_admin_log" VALUES(104,'6','Note updated',1,'',29,1,'2014-11-25 23:23:04.806339');
INSERT INTO "django_admin_log" VALUES(105,'1','bla',2,'Changed topic.',11,1,'2014-12-07 22:10:53.151837');
INSERT INTO "django_admin_log" VALUES(106,'1','bla',2,'No fields changed.',11,1,'2014-12-07 22:11:17.496690');
INSERT INTO "django_admin_log" VALUES(107,'6','asasdfsadfasd',3,'',15,1,'2014-12-11 15:47:03.214930');
INSERT INTO "django_admin_log" VALUES(108,'5','testes',3,'',15,1,'2014-12-11 15:47:03.339664');
INSERT INTO "django_admin_log" VALUES(109,'7','asasdfsadfasd',2,'Changed confirmedEmail.',15,1,'2014-12-11 16:02:39.897658');
INSERT INTO "django_admin_log" VALUES(110,'7','asasdfsadfasd',2,'Changed password.',15,1,'2014-12-11 16:02:48.727277');
INSERT INTO "django_admin_log" VALUES(111,'7','asasdfsadfasd',2,'Changed lastTimeActive and joined.',15,1,'2014-12-11 16:08:12.268282');
INSERT INTO "django_admin_log" VALUES(112,'9','vipvipr',3,'',15,1,'2014-12-11 16:25:47.446383');
INSERT INTO "django_admin_log" VALUES(113,'8','vipvip',3,'',15,1,'2014-12-11 16:25:47.584723');
INSERT INTO "django_admin_log" VALUES(114,'7','asasdfsadfasd',3,'',15,1,'2014-12-11 16:25:47.751696');
INSERT INTO "django_admin_log" VALUES(115,'10','qwer',1,'',15,1,'2014-12-11 16:26:08.917750');
INSERT INTO "django_admin_log" VALUES(116,'10','qwer',2,'No fields changed.',15,1,'2014-12-11 16:26:26.825799');
INSERT INTO "django_admin_log" VALUES(117,'10','qwerr',2,'Changed nick.',15,1,'2014-12-11 16:28:47.694995');
INSERT INTO "django_admin_log" VALUES(118,'11','qwerqwerqwer',3,'',15,1,'2014-12-11 16:36:06.772223');
INSERT INTO "django_admin_log" VALUES(119,'10','qwerr',3,'',15,1,'2014-12-11 16:36:06.899583');
INSERT INTO "django_admin_log" VALUES(120,'12','asasdfsadfasd',3,'',15,1,'2014-12-11 16:41:56.088604');
INSERT INTO "django_admin_log" VALUES(121,'13','asasdfsadfasd',2,'Changed lastTimeActive and joined.',15,1,'2014-12-11 16:55:44.461860');
INSERT INTO "django_admin_log" VALUES(122,'13','asasdfsadfasd',2,'Changed lastTimeActive and joined.',15,1,'2014-12-11 16:55:52.709246');
INSERT INTO "django_admin_log" VALUES(123,'13','asasdfsadfasd',2,'Changed lastTimeActive and joined.',15,1,'2014-12-11 16:56:10.983695');
INSERT INTO "django_admin_log" VALUES(124,'13','asasdfsadfasd',2,'Changed lastTimeActive, joined and confirmedEmail.',15,1,'2014-12-11 16:59:05.829573');
INSERT INTO "django_admin_log" VALUES(125,'1','qwer',1,'',15,1,'2014-12-11 17:04:33.310396');
INSERT INTO "django_admin_log" VALUES(126,'2','Note 1',1,'',11,1,'2014-12-11 18:02:31.752903');
INSERT INTO "django_admin_log" VALUES(127,'2','note2',1,'',15,1,'2014-12-11 18:02:55.229781');
INSERT INTO "django_admin_log" VALUES(128,'3','Note 2',1,'',11,1,'2014-12-11 18:03:11.840537');
INSERT INTO "django_admin_log" VALUES(129,'1','Note 1',1,'',11,1,'2014-12-12 17:01:31.259026');
INSERT INTO "django_admin_log" VALUES(130,'1','admin',2,'Changed nick.',15,1,'2014-12-12 17:01:49.496372');
INSERT INTO "django_admin_log" VALUES(131,'2','Note 2',1,'',11,1,'2014-12-12 17:02:05.498329');
INSERT INTO "django_admin_log" VALUES(132,'7','The note is been removed',1,'',29,1,'2014-12-12 17:07:31.263337');
INSERT INTO "django_admin_log" VALUES(133,'2','alumno',2,'Changed nick.',15,1,'2014-12-12 17:49:24.051469');
INSERT INTO "django_admin_log" VALUES(134,'1','admin',2,'Changed rol.',15,1,'2014-12-12 17:49:30.152042');
INSERT INTO "django_admin_log" VALUES(135,'1','Alumno',1,'',14,1,'2014-12-12 17:54:21.447897');
INSERT INTO "django_admin_log" VALUES(136,'2','Profesor',1,'',14,1,'2014-12-12 17:54:31.314220');
INSERT INTO "django_admin_log" VALUES(137,'3','Coordinador de asignatura',1,'',14,1,'2014-12-12 17:54:41.255298');
INSERT INTO "django_admin_log" VALUES(138,'4','Delegado de curso',1,'',14,1,'2014-12-12 17:54:49.840287');
INSERT INTO "django_admin_log" VALUES(139,'5','Administrador',1,'',14,1,'2014-12-12 17:55:07.790058');
INSERT INTO "django_admin_log" VALUES(140,'6','g0d',1,'',14,1,'2014-12-12 17:55:11.788244');
INSERT INTO "django_admin_log" VALUES(141,'4','Delegado de curso',2,'Changed priority.',14,1,'2014-12-12 17:55:21.915363');
INSERT INTO "django_admin_log" VALUES(142,'4','Delegado de curso',2,'Changed priority.',14,1,'2014-12-12 17:55:37.095390');
INSERT INTO "django_admin_log" VALUES(143,'5','Administrador',2,'Changed priority.',14,1,'2014-12-12 17:55:54.678742');
INSERT INTO "django_admin_log" VALUES(144,'6','g0d',2,'Changed priority.',14,1,'2014-12-12 17:55:59.840009');
INSERT INTO "django_admin_log" VALUES(145,'2','alumno',2,'Changed rol.',15,1,'2014-12-12 18:00:36.746898');
INSERT INTO "django_admin_log" VALUES(146,'1','admin',2,'No fields changed.',15,1,'2014-12-12 18:00:42.898762');
INSERT INTO "django_admin_log" VALUES(147,'1','admin',2,'Changed rol.',15,1,'2014-12-12 18:01:11.396360');
INSERT INTO "django_admin_log" VALUES(148,'1','admin',2,'Changed rol.',15,1,'2014-12-12 18:01:20.843868');
INSERT INTO "django_admin_log" VALUES(149,'1','admin',2,'Changed rol.',15,1,'2014-12-12 18:01:36.745565');
INSERT INTO "django_admin_log" VALUES(150,'2','alumno',2,'Changed rol.',15,1,'2014-12-12 18:01:42.958695');
INSERT INTO "django_admin_log" VALUES(151,'1','Note alumno',2,'Changed topic.',11,1,'2014-12-12 18:01:56.303711');
INSERT INTO "django_admin_log" VALUES(152,'2','Note g0d',2,'Changed topic.',11,1,'2014-12-12 18:02:13.609054');
INSERT INTO "django_admin_log" VALUES(153,'1','Note alumno',2,'Changed visible.',11,1,'2014-12-12 18:26:02.315589');
INSERT INTO "django_admin_log" VALUES(154,'2','Note g0d',2,'Changed level.',11,1,'2014-12-12 21:48:13.960621');
INSERT INTO "django_admin_log" VALUES(155,'2','Note g0d',2,'Changed level.',11,1,'2014-12-12 21:48:51.711356');
INSERT INTO "django_admin_log" VALUES(158,'2','weekly',3,'',19,1,'2015-02-01 13:55:45.067391');
INSERT INTO "django_admin_log" VALUES(160,'5','weekly',1,'',19,1,'2015-02-03 21:26:47.505811');
INSERT INTO "django_admin_log" VALUES(161,'1','daily',1,'',19,1,'2015-02-03 21:28:10.932483');
INSERT INTO "django_admin_log" VALUES(162,'2','weekly',1,'',19,1,'2015-02-03 21:28:18.130625');
INSERT INTO "django_admin_log" VALUES(163,'3','monthly',1,'',19,1,'2015-02-03 21:28:21.434545');
INSERT INTO "django_admin_log" VALUES(164,'4','unique',1,'',19,1,'2015-02-03 21:28:25.184424');
INSERT INTO "django_admin_log" VALUES(165,'1','asdf',1,'',30,1,'2015-02-03 21:42:28.665438');
INSERT INTO "django_admin_log" VALUES(166,'2','asdf',1,'',30,1,'2015-02-03 21:51:16.333351');
INSERT INTO "django_admin_log" VALUES(167,'2','asdf',2,'No fields changed.',30,1,'2015-02-03 21:51:43.610826');
INSERT INTO "django_admin_log" VALUES(168,'2','asdf',2,'No fields changed.',30,1,'2015-02-03 21:52:15.852394');
INSERT INTO "django_admin_log" VALUES(169,'2','asdf',2,'Changed lastDate.',30,1,'2015-02-03 22:03:08.941498');
INSERT INTO "django_admin_log" VALUES(170,'3','month',1,'',30,1,'2015-02-03 22:15:03.650306');
INSERT INTO "django_admin_log" VALUES(171,'3','month',3,'',30,1,'2015-02-03 22:40:46.352985');
INSERT INTO "django_admin_log" VALUES(172,'4','testet',1,'',30,1,'2015-02-03 23:05:26.417707');
INSERT INTO "django_admin_log" VALUES(173,'4','testet',2,'Changed hourStart, hourEnd and allDay.',30,1,'2015-02-03 23:06:04.438937');
INSERT INTO "django_admin_log" VALUES(174,'4','testet',2,'No fields changed.',30,1,'2015-02-03 23:07:05.994882');
INSERT INTO "django_admin_log" VALUES(175,'8','The calendar event is been removed',1,'',29,1,'2015-02-07 21:21:17.900902');
INSERT INTO "django_admin_log" VALUES(176,'4','student',1,'',10,1,'2015-02-10 19:29:39.360190');
INSERT INTO "django_admin_log" VALUES(177,'9','Calendar event has been updated.',1,'',29,1,'2015-02-10 21:07:16.887985');
INSERT INTO "django_admin_log" VALUES(178,'3','AdminTest',1,'',22,1,'2015-02-10 22:50:11.284343');
INSERT INTO "django_admin_log" VALUES(179,'3','AdminTest',2,'Changed file.',22,1,'2015-02-10 22:53:22.346905');
INSERT INTO "django_admin_log" VALUES(180,'10','The file has been removed',1,'',29,1,'2015-02-11 18:23:28.730215');
INSERT INTO "django_admin_log" VALUES(181,'3','AdminTest',2,'Changed visible.',22,1,'2015-02-11 18:26:25.700528');
INSERT INTO "django_admin_log" VALUES(182,'3','AdminTest',2,'Changed visible.',22,1,'2015-02-11 18:27:09.050987');
INSERT INTO "django_admin_log" VALUES(183,'3','AdminTest',2,'Changed file.',22,1,'2015-02-11 18:34:46.685539');
INSERT INTO "django_admin_log" VALUES(184,'3','AdminTest',2,'Changed file.',22,1,'2015-02-11 18:35:02.109911');
INSERT INTO "django_admin_log" VALUES(185,'3','AdminTest',2,'Changed file.',22,1,'2015-02-11 18:35:27.233697');
INSERT INTO "django_admin_log" VALUES(186,'3','AdminTest',2,'Changed hash.',22,1,'2015-02-11 18:36:06.969562');
INSERT INTO "django_admin_log" VALUES(187,'1','Ingenieria del software',1,'',9,1,'2015-02-22 15:37:37.925543');
INSERT INTO "django_admin_log" VALUES(188,'2','Ingenieria de computadores',1,'',9,1,'2015-02-22 15:37:57.454273');
INSERT INTO "django_admin_log" VALUES(189,'3','3ro de software',1,'',9,1,'2015-02-22 15:38:30.603986');
INSERT INTO "django_admin_log" VALUES(190,'4','Verificacion y Validacion',1,'',9,1,'2015-02-22 15:38:56.199719');
INSERT INTO "django_admin_log" VALUES(191,'6','POST POST',2,'No fields changed.',30,1,'2015-02-22 15:39:42.422957');
INSERT INTO "django_admin_log" VALUES(192,'1','viperey',1,'',15,1,'2015-03-04 13:31:28.551948');
INSERT INTO "django_admin_log" VALUES(193,'1','viperey',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:13:47.241917');
INSERT INTO "django_admin_log" VALUES(194,'1','viperey',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:14:06.777751');
INSERT INTO "django_admin_log" VALUES(195,'1','viperey',2,'No fields changed.',15,1,'2015-03-04 18:14:09.593811');
INSERT INTO "django_admin_log" VALUES(196,'2','qwerqwer',2,'Changed confirmedEmail and subjects.',15,1,'2015-03-04 18:14:19.277852');
INSERT INTO "django_admin_log" VALUES(197,'3','mlmlfemf',2,'Changed confirmedEmail and subjects.',15,1,'2015-03-04 18:14:35.988391');
INSERT INTO "django_admin_log" VALUES(198,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:15:10.366316');
INSERT INTO "django_admin_log" VALUES(199,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:15:30.732401');
INSERT INTO "django_admin_log" VALUES(200,'3','mlmlfemf',2,'No fields changed.',15,1,'2015-03-04 18:15:44.617489');
INSERT INTO "django_admin_log" VALUES(201,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:17:13.349551');
INSERT INTO "django_admin_log" VALUES(202,'3','mlmlfemf',2,'No fields changed.',15,1,'2015-03-04 18:17:21.064337');
INSERT INTO "django_admin_log" VALUES(203,'3','mlmlfemf',2,'No fields changed.',15,1,'2015-03-04 18:17:39.079556');
INSERT INTO "django_admin_log" VALUES(204,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:17:41.980559');
INSERT INTO "django_admin_log" VALUES(205,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:17:58.186345');
INSERT INTO "django_admin_log" VALUES(206,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:20:52.167238');
INSERT INTO "django_admin_log" VALUES(207,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:21:32.005885');
INSERT INTO "django_admin_log" VALUES(208,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:22:00.957645');
INSERT INTO "django_admin_log" VALUES(209,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:23:50.422396');
INSERT INTO "django_admin_log" VALUES(210,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 18:26:36.736713');
INSERT INTO "django_admin_log" VALUES(211,'11','Account successfully validated.',1,'',29,1,'2015-03-04 21:08:20.622080');
INSERT INTO "django_admin_log" VALUES(212,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 21:13:59.037053');
INSERT INTO "django_admin_log" VALUES(213,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 21:14:16.179571');
INSERT INTO "django_admin_log" VALUES(214,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 21:17:46.750805');
INSERT INTO "django_admin_log" VALUES(215,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 21:19:19.930253');
INSERT INTO "django_admin_log" VALUES(216,'3','mlmlfemf',2,'Changed confirmedEmail.',15,1,'2015-03-04 21:19:50.211031');
INSERT INTO "django_admin_log" VALUES(217,'1','viperey',2,'Changed password.',15,1,'2015-03-04 21:45:02.324080');
INSERT INTO "django_admin_log" VALUES(218,'1','viperey',2,'Changed password.',15,1,'2015-03-04 21:51:22.116424');
INSERT INTO "django_admin_log" VALUES(219,'1','viperey',2,'Changed password.',15,1,'2015-03-04 21:53:09.256414');
INSERT INTO "django_admin_log" VALUES(220,'1','viperey',2,'Changed subjects.',15,1,'2015-03-05 12:32:05.724148');
INSERT INTO "django_admin_log" VALUES(221,'1','viperey',2,'Changed password.',15,1,'2015-03-05 14:13:08.701455');
INSERT INTO "django_admin_log" VALUES(222,'1','viperey',2,'Changed password.',15,1,'2015-03-05 14:16:25.184423');
INSERT INTO "django_admin_log" VALUES(223,'1','viperey',2,'Changed password.',15,1,'2015-03-05 14:18:01.509944');
INSERT INTO "django_admin_log" VALUES(224,'1','viperey',2,'Changed profilePic and sessionToken.',15,1,'2015-03-11 00:48:08.348527');
INSERT INTO "django_admin_log" VALUES(225,'1','viperey',2,'Changed profilePic and sessionToken.',15,1,'2015-03-11 00:48:52.202834');
INSERT INTO "django_admin_log" VALUES(226,'1','victor',2,'Changed email, nick and password.',15,1,'2015-03-14 17:33:24.343321');
INSERT INTO "django_admin_log" VALUES(227,'14','Name''s length has to be between 4 and 20',1,'',28,1,'2015-03-14 17:55:25.880914');
INSERT INTO "django_admin_log" VALUES(228,'14','Name''s length has to be between 4 and 100',2,'Changed error.',28,1,'2015-03-14 17:56:12.873579');
INSERT INTO "django_admin_log" VALUES(229,'1','viperey',2,'Changed password.',15,1,'2015-03-14 18:38:42.734377');
INSERT INTO "django_admin_log" VALUES(230,'1','viperey',2,'Changed password.',15,1,'2015-03-18 08:20:07.510777');
INSERT INTO "django_admin_log" VALUES(231,'1','viperey',2,'Changed sessionToken and subjects.',15,1,'2015-04-09 10:35:01.549174');
INSERT INTO "django_admin_log" VALUES(232,'1','viperey',2,'Changed subjects.',15,1,'2015-04-09 11:14:42.998935');
INSERT INTO "django_admin_log" VALUES(233,'5','Calidad del software',1,'',9,1,'2015-04-09 11:15:00.907406');
INSERT INTO "django_admin_log" VALUES(234,'1','viperey',2,'Changed subjects.',15,1,'2015-04-09 11:15:03.506050');
INSERT INTO "django_admin_log" VALUES(235,'6','Gestion de proyectos',1,'',9,1,'2015-04-09 15:45:03.997052');
INSERT INTO "django_admin_log" VALUES(236,'1','viperey',2,'No fields changed.',15,1,'2015-04-09 15:45:07.021125');
INSERT INTO "django_admin_log" VALUES(237,'1','viperey',2,'Changed subjects.',15,1,'2015-04-09 15:55:03.476079');
INSERT INTO "django_admin_log" VALUES(238,'5','university',1,'',10,1,'2015-04-11 19:48:25.475265');
INSERT INTO "django_admin_log" VALUES(239,'7','UPM',1,'',9,1,'2015-04-11 19:48:50.703130');
INSERT INTO "django_admin_log" VALUES(240,'2','Ingenieria de computadores',2,'Changed parent.',9,1,'2015-04-11 19:48:58.433664');
INSERT INTO "django_admin_log" VALUES(241,'1','Ingenieria del software',2,'Changed parent.',9,1,'2015-04-11 19:49:04.314918');
INSERT INTO "django_admin_log" VALUES(242,'3','Antenistas',1,'',11,1,'2015-04-12 14:06:14.321944');
INSERT INTO "django_admin_log" VALUES(243,'3','Antenistas',2,'Changed level.',11,1,'2015-04-12 14:22:47.464563');
INSERT INTO "django_admin_log" VALUES(244,'3','Antenistas',2,'Changed level.',11,1,'2015-04-12 14:30:02.455749');
INSERT INTO "django_admin_log" VALUES(245,'3','Antenistas',2,'Changed level.',11,1,'2015-04-12 17:19:17.357173');
INSERT INTO "django_admin_log" VALUES(246,'12','Your note was successfully created',1,'',29,1,'2015-04-12 21:57:28.773268');
INSERT INTO "django_admin_log" VALUES(247,'23','Nota seria',3,'',11,1,'2015-04-13 13:29:57.684126');
INSERT INTO "django_admin_log" VALUES(248,'22','asdfas',3,'',11,1,'2015-04-13 13:29:57.919730');
INSERT INTO "django_admin_log" VALUES(249,'21','asdfa',3,'',11,1,'2015-04-13 13:29:58.262822');
INSERT INTO "django_admin_log" VALUES(250,'20','asldkflasdkjf',3,'',11,1,'2015-04-13 13:29:58.632045');
INSERT INTO "django_admin_log" VALUES(251,'19','qqqqqqqqqqqqq',3,'',11,1,'2015-04-13 13:29:58.895501');
INSERT INTO "django_admin_log" VALUES(252,'18','asdf',3,'',11,1,'2015-04-13 13:29:59.117878');
INSERT INTO "django_admin_log" VALUES(253,'17','notas calidad',3,'',11,1,'2015-04-13 13:29:59.344314');
INSERT INTO "django_admin_log" VALUES(254,'16','asdf',3,'',11,1,'2015-04-13 13:29:59.639349');
INSERT INTO "django_admin_log" VALUES(255,'15','Nota',3,'',11,1,'2015-04-13 13:30:00.238519');
INSERT INTO "django_admin_log" VALUES(256,'14','message',3,'',11,1,'2015-04-13 13:30:00.659792');
INSERT INTO "django_admin_log" VALUES(257,'13','asdf',3,'',11,1,'2015-04-13 13:30:01.225844');
INSERT INTO "django_admin_log" VALUES(258,'12','qwer2',3,'',11,1,'2015-04-13 13:30:01.536980');
INSERT INTO "django_admin_log" VALUES(259,'11','qwer2',3,'',11,1,'2015-04-13 13:30:01.830086');
INSERT INTO "django_admin_log" VALUES(260,'10','qwer2',3,'',11,1,'2015-04-13 13:30:02.426685');
INSERT INTO "django_admin_log" VALUES(261,'9','asdf',3,'',11,1,'2015-04-13 13:30:02.749986');
INSERT INTO "django_admin_log" VALUES(262,'8','asdf',3,'',11,1,'2015-04-13 13:30:03.090865');
INSERT INTO "django_admin_log" VALUES(263,'7','asdf',3,'',11,1,'2015-04-13 13:30:03.471585');
INSERT INTO "django_admin_log" VALUES(264,'6','Nota',3,'',11,1,'2015-04-13 13:30:03.704825');
INSERT INTO "django_admin_log" VALUES(265,'5','asdf',3,'',11,1,'2015-04-13 13:30:04.000266');
INSERT INTO "django_admin_log" VALUES(266,'4','asdfa',3,'',11,1,'2015-04-13 13:30:04.333168');
INSERT INTO "django_admin_log" VALUES(267,'3','Antenistas',3,'',11,1,'2015-04-13 13:30:04.627190');
INSERT INTO "django_admin_log" VALUES(268,'2','Note g0d',3,'',11,1,'2015-04-13 13:30:05.143313');
INSERT INTO "django_admin_log" VALUES(269,'1','qwer2',3,'',11,1,'2015-04-13 13:30:05.699809');
INSERT INTO "django_admin_log" VALUES(270,'1','Nte',1,'',11,1,'2015-04-13 13:33:29.774092');
INSERT INTO "django_admin_log" VALUES(271,'2','asdf',1,'',11,1,'2015-04-13 13:33:41.701633');
INSERT INTO "django_admin_log" VALUES(272,'3','AdminTest',2,'Changed subject.',22,1,'2015-04-13 14:28:30.550874');
INSERT INTO "django_admin_log" VALUES(273,'20','TAREA3.docx',3,'',22,1,'2015-04-14 00:38:12.253046');
INSERT INTO "django_admin_log" VALUES(274,'19','TAREA3.docx',3,'',22,1,'2015-04-14 00:38:12.425108');
INSERT INTO "django_admin_log" VALUES(275,'18','TAREA3.docx',3,'',22,1,'2015-04-14 00:38:12.602270');
INSERT INTO "django_admin_log" VALUES(276,'17','DNI victor 2.png',3,'',22,1,'2015-04-14 00:38:12.818513');
INSERT INTO "django_admin_log" VALUES(277,'16','fingers-crossed.jpg',3,'',22,1,'2015-04-14 00:38:13.024927');
INSERT INTO "django_admin_log" VALUES(278,'15','unnamed.png',3,'',22,1,'2015-04-14 00:38:13.207130');
INSERT INTO "django_admin_log" VALUES(279,'14','12fbf08 (1).jpg',3,'',22,1,'2015-04-14 00:38:13.421260');
INSERT INTO "django_admin_log" VALUES(280,'13','TAREA3.docx',3,'',22,1,'2015-04-14 00:38:13.604418');
INSERT INTO "django_admin_log" VALUES(281,'12','TAREA1_1_GST31.docx',3,'',22,1,'2015-04-14 00:38:13.761709');
INSERT INTO "django_admin_log" VALUES(282,'11','HzEEBF2w.png',3,'',22,1,'2015-04-14 00:38:13.964342');
INSERT INTO "django_admin_log" VALUES(283,'10','DNI victor.png',3,'',22,1,'2015-04-14 00:38:14.186699');
INSERT INTO "django_admin_log" VALUES(284,'9','DNI victor.png',3,'',22,1,'2015-04-14 00:38:14.383499');
INSERT INTO "django_admin_log" VALUES(285,'8','fingers-crossed.jpg',3,'',22,1,'2015-04-14 00:38:14.597944');
INSERT INTO "django_admin_log" VALUES(286,'7','fingers-crossed.jpg',3,'',22,1,'2015-04-14 00:38:14.895827');
INSERT INTO "django_admin_log" VALUES(287,'6','fingers-crossed.jpg',3,'',22,1,'2015-04-14 00:38:15.100792');
INSERT INTO "django_admin_log" VALUES(288,'5','fingers-crossed.jpg',3,'',22,1,'2015-04-14 00:38:15.295794');
INSERT INTO "django_admin_log" VALUES(289,'4','fingers-crossed.jpg',3,'',22,1,'2015-04-14 00:38:15.539788');
INSERT INTO "django_admin_log" VALUES(290,'3','AdminTest',3,'',22,1,'2015-04-14 00:38:15.777817');
INSERT INTO "django_admin_log" VALUES(291,'13','Your file was successfully uploaded',1,'',29,1,'2015-04-14 00:49:19.858227');
INSERT INTO "django_admin_log" VALUES(292,'32','files/1d119d545510974f4b49e012b39cfa3cabdb76f8964ae12062f904cd00d4dbd2.jpg',2,'Changed fileType and visible.',22,1,'2015-04-14 00:55:09.581890');
INSERT INTO "django_admin_log" VALUES(293,'31','files/82238e34b6ff6603e24b6560c7ababe7c0f323fce2911552f1b0ea9f2e0eacd6_JQ0g31t.docx',2,'Changed fileType.',22,1,'2015-04-14 00:55:50.856630');
INSERT INTO "django_admin_log" VALUES(294,'30','DNI victor 2.png',2,'Changed fileType.',22,1,'2015-04-14 00:56:54.074414');
INSERT INTO "django_admin_log" VALUES(295,'32','files/1d119d545510974f4b49e012b39cfa3cabdb76f8964ae12062f904cd00d4dbd2.jpg',3,'',22,1,'2015-04-14 00:57:27.105065');
INSERT INTO "django_admin_log" VALUES(296,'31','files/82238e34b6ff6603e24b6560c7ababe7c0f323fce2911552f1b0ea9f2e0eacd6_JQ0g31t.docx',3,'',22,1,'2015-04-14 00:57:27.305583');
INSERT INTO "django_admin_log" VALUES(297,'30','DNI victor 2.png',3,'',22,1,'2015-04-14 00:57:55.241345');
INSERT INTO "django_admin_log" VALUES(298,'29','fingers-crossed.jpg',2,'Changed fileType.',22,1,'2015-04-14 00:58:03.161350');
INSERT INTO "django_admin_log" VALUES(299,'104','Memoria.pdf',3,'',22,1,'2015-04-14 01:08:04.228439');
INSERT INTO "django_admin_log" VALUES(300,'103','Memoria (1).pdf',3,'',22,1,'2015-04-14 01:08:04.389698');
INSERT INTO "django_admin_log" VALUES(301,'102','Idea.txt',3,'',22,1,'2015-04-14 01:08:04.599335');
INSERT INTO "django_admin_log" VALUES(302,'101','Memoria.txt',3,'',22,1,'2015-04-14 01:08:04.798827');
INSERT INTO "django_admin_log" VALUES(303,'100','PB5.pdf',3,'',22,1,'2015-04-14 01:08:04.986602');
INSERT INTO "django_admin_log" VALUES(304,'99','PBSemana11.pdf',3,'',22,1,'2015-04-14 01:08:05.157741');
INSERT INTO "django_admin_log" VALUES(305,'98','pb3.pdf',3,'',22,1,'2015-04-14 01:08:05.345907');
INSERT INTO "django_admin_log" VALUES(306,'97','Segunda.jpg',3,'',22,1,'2015-04-14 01:08:05.542594');
INSERT INTO "django_admin_log" VALUES(307,'96','PB4.pdf',3,'',22,1,'2015-04-14 01:08:05.733662');
INSERT INTO "django_admin_log" VALUES(308,'95','primera.jpg',3,'',22,1,'2015-04-14 01:08:05.923021');
INSERT INTO "django_admin_log" VALUES(309,'94','Pb10.pdf',3,'',22,1,'2015-04-14 01:08:06.115349');
INSERT INTO "django_admin_log" VALUES(310,'93','PB1.pdf',3,'',22,1,'2015-04-14 01:08:06.303835');
INSERT INTO "django_admin_log" VALUES(311,'92','PB2-Grupo07.pdf',3,'',22,1,'2015-04-14 01:08:06.516114');
INSERT INTO "django_admin_log" VALUES(312,'91','Pb7 - Provisional.pdf',3,'',22,1,'2015-04-14 01:08:06.715288');
INSERT INTO "django_admin_log" VALUES(313,'90','Diapo 2.odp',3,'',22,1,'2015-04-14 01:08:06.915929');
INSERT INTO "django_admin_log" VALUES(314,'89','Diapo 2.pdf',3,'',22,1,'2015-04-14 01:08:07.226731');
INSERT INTO "django_admin_log" VALUES(315,'88','Plantilla Plan de Proyectov1.0.docx',3,'',22,1,'2015-04-14 01:08:07.402322');
INSERT INTO "django_admin_log" VALUES(316,'87','Diapo 2.ppt',3,'',22,1,'2015-04-14 01:08:07.602566');
INSERT INTO "django_admin_log" VALUES(317,'86','pb8.pdf',3,'',22,1,'2015-04-14 01:08:07.879833');
INSERT INTO "django_admin_log" VALUES(318,'85','Burndown.pdf',3,'',22,1,'2015-04-14 01:08:08.125958');
INSERT INTO "django_admin_log" VALUES(319,'84','Practica1Curso2013.pdf',3,'',22,1,'2015-04-14 01:08:08.328998');
INSERT INTO "django_admin_log" VALUES(320,'83','Burndown.ods',3,'',22,1,'2015-04-14 01:08:08.519942');
INSERT INTO "django_admin_log" VALUES(321,'82','Burndown graph.pdf',3,'',22,1,'2015-04-14 01:08:08.705928');
INSERT INTO "django_admin_log" VALUES(322,'81','Tema 3 - Apuntes.txt',3,'',22,1,'2015-04-14 01:08:08.896523');
INSERT INTO "django_admin_log" VALUES(323,'80','Tema 4 - Apuntes.txt',3,'',22,1,'2015-04-14 01:08:09.097912');
INSERT INTO "django_admin_log" VALUES(324,'79','Tema 1 - Ciclo de vida.pdf',3,'',22,1,'2015-04-14 01:08:09.607755');
INSERT INTO "django_admin_log" VALUES(325,'78','Tema 2 - Equipo.pdf',3,'',22,1,'2015-04-14 01:08:09.803606');
INSERT INTO "django_admin_log" VALUES(326,'77','tema 4.0  - Formalizacion_10.pdf',3,'',22,1,'2015-04-14 01:08:09.995999');
INSERT INTO "django_admin_log" VALUES(327,'76','tema1_EnfoqueProyecto.pdf',3,'',22,1,'2015-04-14 01:08:10.196452');
INSERT INTO "django_admin_log" VALUES(328,'75','tema 4.3 - Planificación.pdf',3,'',22,1,'2015-04-14 01:08:10.385424');
INSERT INTO "django_admin_log" VALUES(329,'74','Tema 3 - Fases.pdf',3,'',22,1,'2015-04-14 01:08:10.606792');
INSERT INTO "django_admin_log" VALUES(330,'73','Tema 5 Gestión del riesgo.pdf',3,'',22,1,'2015-04-14 01:08:10.795090');
INSERT INTO "django_admin_log" VALUES(331,'72','Tema 1 - Enfoque.pdf',3,'',22,1,'2015-04-14 01:08:10.973459');
INSERT INTO "django_admin_log" VALUES(332,'71','tema4_1_medidas_10.pdf',3,'',22,1,'2015-04-14 01:08:11.151089');
INSERT INTO "django_admin_log" VALUES(333,'70','Tema 4 - Apuntes',3,'',22,1,'2015-04-14 01:08:11.338992');
INSERT INTO "django_admin_log" VALUES(334,'69','tema3_Fases.pdf',3,'',22,1,'2015-04-14 01:08:11.555743');
INSERT INTO "django_admin_log" VALUES(335,'68','tema1_CiclosVida.pdf',3,'',22,1,'2015-04-14 01:08:11.764323');
INSERT INTO "django_admin_log" VALUES(336,'67','tema 4.1 - Medidas_10.pdf',3,'',22,1,'2015-04-14 01:08:12.138514');
INSERT INTO "django_admin_log" VALUES(337,'66','tema4_Formalizacion_10.pdf',3,'',22,1,'2015-04-14 01:08:12.684796');
INSERT INTO "django_admin_log" VALUES(338,'65','Tema 4.4 - Gestion de costes.pdf',3,'',22,1,'2015-04-14 01:08:13.010196');
INSERT INTO "django_admin_log" VALUES(339,'64','Tema 1 - Requisitos.pdf',3,'',22,1,'2015-04-14 01:08:13.226324');
INSERT INTO "django_admin_log" VALUES(340,'63','Tema 1 Ciclos - Apuntes.txt',3,'',22,1,'2015-04-14 01:08:13.414194');
INSERT INTO "django_admin_log" VALUES(341,'62','tema 4.2 - Estimacion.pdf',3,'',22,1,'2015-04-14 01:08:13.613378');
INSERT INTO "django_admin_log" VALUES(342,'61','tema1_Requisitos.pdf',3,'',22,1,'2015-04-14 01:08:13.810896');
INSERT INTO "django_admin_log" VALUES(343,'60','tema2_Equipo.pdf',3,'',22,1,'2015-04-14 01:08:14.001166');
INSERT INTO "django_admin_log" VALUES(344,'59','Tema 5 - Apuntes.txt',3,'',22,1,'2015-04-14 01:08:14.834237');
INSERT INTO "django_admin_log" VALUES(345,'58','Tema 1 - Agiles.txt',3,'',22,1,'2015-04-14 01:08:15.477392');
INSERT INTO "django_admin_log" VALUES(346,'57','Tema 2 - Vision del proyecto.pdf',3,'',22,1,'2015-04-14 01:08:15.677878');
INSERT INTO "django_admin_log" VALUES(347,'56','Tema 2 - Apuntes.txt',3,'',22,1,'2015-04-14 01:08:15.878097');
INSERT INTO "django_admin_log" VALUES(348,'55','Plan de medidas.pdf',3,'',22,1,'2015-04-14 01:08:16.073815');
INSERT INTO "django_admin_log" VALUES(349,'54','Tema 1 - Agiles.pdf',3,'',22,1,'2015-04-14 01:08:16.267422');
INSERT INTO "django_admin_log" VALUES(350,'53','Tema 2 - Inception deck.txt',3,'',22,1,'2015-04-14 01:08:16.445123');
INSERT INTO "django_admin_log" VALUES(351,'52','Tema 2 - Inception deck.pdf',3,'',22,1,'2015-04-14 01:08:16.635421');
INSERT INTO "django_admin_log" VALUES(352,'51','Pb7 - Provisional.pdf',3,'',22,1,'2015-04-14 01:08:16.809588');
INSERT INTO "django_admin_log" VALUES(353,'50','Plantilla Plan de Proyecto v1.9.docx',3,'',22,1,'2015-04-14 01:08:16.978604');
INSERT INTO "django_admin_log" VALUES(354,'49','Plantilla Plan de Proyectov1.0.odt',3,'',22,1,'2015-04-14 01:08:17.155810');
INSERT INTO "django_admin_log" VALUES(355,'48','Productbox semana 6.pdf',3,'',22,1,'2015-04-14 01:08:17.378603');
INSERT INTO "django_admin_log" VALUES(356,'47','Plan15.docx',3,'',22,1,'2015-04-14 01:08:17.601421');
INSERT INTO "django_admin_log" VALUES(357,'46','Plantilla Plan de Proyectov1.0.docx',3,'',22,1,'2015-04-14 01:08:17.902224');
INSERT INTO "django_admin_log" VALUES(358,'45','Plantilla Plan de Proyectov1.0.doc',3,'',22,1,'2015-04-14 01:08:18.087318');
INSERT INTO "django_admin_log" VALUES(359,'44','Plantilla Plan de Proyectov1.0 (Copia en conflicto de Viperey perez 2014-02-24).docx',3,'',22,1,'2015-04-14 01:08:18.320435');
INSERT INTO "django_admin_log" VALUES(360,'43','Practica1Curso2013.pdf',3,'',22,1,'2015-04-14 01:08:18.550796');
INSERT INTO "django_admin_log" VALUES(361,'42','Planning.txt',3,'',22,1,'2015-04-14 01:08:18.821001');
INSERT INTO "django_admin_log" VALUES(362,'41','.dropbox',3,'',22,1,'2015-04-14 01:08:19.021492');
INSERT INTO "django_admin_log" VALUES(363,'40','TAREA3 (1).docx',3,'',22,1,'2015-04-14 01:08:19.237277');
INSERT INTO "django_admin_log" VALUES(364,'39','DNI victor 2.png',3,'',22,1,'2015-04-14 01:08:19.426526');
INSERT INTO "django_admin_log" VALUES(365,'38','Starbuck+%5BBluRayRip%5D%5BAC3+5.1+Español+Castellano%5D%5B2012%5D.torrent.added',3,'',22,1,'2015-04-14 01:08:19.702417');
INSERT INTO "django_admin_log" VALUES(366,'37','repository.pulsarunofficial-1.0.1.zip',3,'',22,1,'2015-04-14 01:08:19.889743');
INSERT INTO "django_admin_log" VALUES(367,'36','TAREA3.docx',3,'',22,1,'2015-04-14 01:08:20.079953');
INSERT INTO "django_admin_log" VALUES(368,'35','unnamed.png',3,'',22,1,'2015-04-14 01:08:20.272290');
INSERT INTO "django_admin_log" VALUES(369,'34','CV Chacho Castiella.pdf',3,'',22,1,'2015-04-14 01:08:20.453030');
INSERT INTO "django_admin_log" VALUES(370,'33','CV Ignacio Castiella.pdf',3,'',22,1,'2015-04-14 01:08:20.638266');
INSERT INTO "django_admin_log" VALUES(371,'29','fingers-crossed.jpg',3,'',22,1,'2015-04-14 01:08:20.912146');
INSERT INTO "django_admin_log" VALUES(372,'28','TAREA3 (1).docx',3,'',22,1,'2015-04-14 01:08:21.180378');
INSERT INTO "django_admin_log" VALUES(373,'27','ic_launcher (1).zip',3,'',22,1,'2015-04-14 01:08:21.393564');
INSERT INTO "django_admin_log" VALUES(374,'26','fingers-crossed.jpg',3,'',22,1,'2015-04-14 01:08:21.591003');
INSERT INTO "django_admin_log" VALUES(375,'25','CV Chacho Castiella.pdf',3,'',22,1,'2015-04-14 01:08:21.925309');
INSERT INTO "django_admin_log" VALUES(376,'24','TAREA3.docx',3,'',22,1,'2015-04-14 01:08:22.214217');
INSERT INTO "django_admin_log" VALUES(377,'23','unnamed.png',3,'',22,1,'2015-04-14 01:08:22.482752');
INSERT INTO "django_admin_log" VALUES(378,'22','TAREA3 (1).docx',3,'',22,1,'2015-04-14 01:08:22.674797');
INSERT INTO "django_admin_log" VALUES(379,'21','TAREA3.docx',3,'',22,1,'2015-04-14 01:08:22.882965');
INSERT INTO "django_admin_log" VALUES(380,'133','Tema 2 - Equipo.pdf',3,'',22,1,'2015-04-14 15:09:22.180536');
INSERT INTO "django_admin_log" VALUES(381,'132','Tema 1 - Ciclo de vida.pdf',3,'',22,1,'2015-04-14 15:09:22.322435');
INSERT INTO "django_admin_log" VALUES(382,'131','tema 4.0  - Formalizacion_10.pdf',3,'',22,1,'2015-04-14 15:09:22.501025');
INSERT INTO "django_admin_log" VALUES(383,'130','Tema 3 - Apuntes.txt',3,'',22,1,'2015-04-14 15:09:22.679054');
INSERT INTO "django_admin_log" VALUES(384,'129','Tema 4 - Apuntes.txt',3,'',22,1,'2015-04-14 15:09:22.868913');
INSERT INTO "django_admin_log" VALUES(385,'128','tema1_EnfoqueProyecto.pdf',3,'',22,1,'2015-04-14 15:09:23.057824');
INSERT INTO "django_admin_log" VALUES(386,'127','Tema 1 - Enfoque.pdf',3,'',22,1,'2015-04-14 15:09:23.246946');
INSERT INTO "django_admin_log" VALUES(387,'126','tema4_1_medidas_10.pdf',3,'',22,1,'2015-04-14 15:09:23.436356');
INSERT INTO "django_admin_log" VALUES(388,'125','tema 4.3 - Planificación.pdf',3,'',22,1,'2015-04-14 15:09:23.625163');
INSERT INTO "django_admin_log" VALUES(389,'124','Tema 3 - Fases.pdf',3,'',22,1,'2015-04-14 15:09:23.815342');
INSERT INTO "django_admin_log" VALUES(390,'123','Tema 4 - Apuntes',3,'',22,1,'2015-04-14 15:09:24.003601');
INSERT INTO "django_admin_log" VALUES(391,'122','tema1_CiclosVida.pdf',3,'',22,1,'2015-04-14 15:09:24.193186');
INSERT INTO "django_admin_log" VALUES(392,'121','tema3_Fases.pdf',3,'',22,1,'2015-04-14 15:09:24.370936');
INSERT INTO "django_admin_log" VALUES(393,'120','Tema 5 Gestión del riesgo.pdf',3,'',22,1,'2015-04-14 15:09:24.560292');
INSERT INTO "django_admin_log" VALUES(394,'119','tema 4.1 - Medidas_10.pdf',3,'',22,1,'2015-04-14 15:09:24.749126');
INSERT INTO "django_admin_log" VALUES(395,'118','tema4_Formalizacion_10.pdf',3,'',22,1,'2015-04-14 15:09:24.938655');
INSERT INTO "django_admin_log" VALUES(396,'117','Tema 1 - Requisitos.pdf',3,'',22,1,'2015-04-14 15:09:25.129479');
INSERT INTO "django_admin_log" VALUES(397,'116','Tema 4.4 - Gestion de costes.pdf',3,'',22,1,'2015-04-14 15:09:25.317598');
INSERT INTO "django_admin_log" VALUES(398,'115','tema1_Requisitos.pdf',3,'',22,1,'2015-04-14 15:09:25.507203');
INSERT INTO "django_admin_log" VALUES(399,'114','tema2_Equipo.pdf',3,'',22,1,'2015-04-14 15:09:25.696211');
INSERT INTO "django_admin_log" VALUES(400,'113','Tema 1 Ciclos - Apuntes.txt',3,'',22,1,'2015-04-14 15:09:25.896462');
INSERT INTO "django_admin_log" VALUES(401,'112','tema 4.2 - Estimacion.pdf',3,'',22,1,'2015-04-14 15:09:26.097189');
INSERT INTO "django_admin_log" VALUES(402,'111','Tema 1 - Agiles.txt',3,'',22,1,'2015-04-14 15:09:26.385780');
INSERT INTO "django_admin_log" VALUES(403,'110','Tema 2 - Vision del proyecto.pdf',3,'',22,1,'2015-04-14 15:09:26.541906');
INSERT INTO "django_admin_log" VALUES(404,'109','Tema 5 - Apuntes.txt',3,'',22,1,'2015-04-14 15:09:26.720789');
INSERT INTO "django_admin_log" VALUES(405,'108','Tema 2 - Apuntes.txt',3,'',22,1,'2015-04-14 15:09:27.019707');
INSERT INTO "django_admin_log" VALUES(406,'107','Tema 2 - Inception deck.pdf',3,'',22,1,'2015-04-14 15:09:27.209307');
INSERT INTO "django_admin_log" VALUES(407,'106','Tema 1 - Agiles.pdf',3,'',22,1,'2015-04-14 15:09:27.410122');
INSERT INTO "django_admin_log" VALUES(408,'105','Tema 2 - Inception deck.txt',3,'',22,1,'2015-04-14 15:09:27.611241');
INSERT INTO "django_admin_log" VALUES(409,'6','Capitales.txt',2,'Changed fileType and text.',22,1,'2015-04-14 15:11:38.835676');
INSERT INTO "django_admin_log" VALUES(410,'6','CapitalLetter',2,'Changed lastUpdater.',22,1,'2015-04-14 15:45:39.699342');
INSERT INTO "django_admin_log" VALUES(411,'6','CapitalLetter',2,'Changed fileType.',22,1,'2015-04-14 15:45:48.090539');
INSERT INTO "django_admin_log" VALUES(412,'6','CapitalLetter',2,'Changed uploader.',22,1,'2015-04-14 15:46:09.045313');
INSERT INTO "django_admin_log" VALUES(413,'6','CapitalLetter',2,'No fields changed.',22,1,'2015-04-14 15:50:55.476609');
INSERT INTO "django_admin_log" VALUES(414,'14','File''s info has been updated',1,'',29,1,'2015-04-14 15:53:44.672144');
INSERT INTO "django_admin_log" VALUES(415,'6',' ',2,'Changed name.',22,1,'2015-04-14 16:18:53.853067');
INSERT INTO "django_admin_log" VALUES(416,'7','V',2,'Changed name.',22,1,'2015-04-14 23:18:57.774976');
INSERT INTO "django_admin_log" VALUES(417,'6','asdfasdf',2,'Changed uploader.',22,1,'2015-04-15 01:13:13.885607');
INSERT INTO "django_admin_log" VALUES(418,'6','asdfasdf',2,'Changed lastUpdater.',22,1,'2015-04-15 01:13:19.495508');
INSERT INTO "django_admin_log" VALUES(419,'6','asdfasdf',2,'Changed uploader and lastUpdater.',22,1,'2015-04-15 01:13:25.074086');
INSERT INTO "django_admin_log" VALUES(420,'3','mlmlfemf',2,'Changed name and password.',15,1,'2015-04-15 01:45:34.088111');
INSERT INTO "django_admin_log" VALUES(421,'1','Theory',1,'',33,1,'2015-04-15 02:02:19.935947');
INSERT INTO "django_admin_log" VALUES(422,'2','Practice',1,'',33,1,'2015-04-15 02:02:28.021918');
INSERT INTO "django_admin_log" VALUES(423,'2','Practice',2,'No fields changed.',33,1,'2015-04-15 02:02:29.053474');
INSERT INTO "django_admin_log" VALUES(424,'3','Classwork',1,'',33,1,'2015-04-15 02:02:49.143374');
INSERT INTO "django_admin_log" VALUES(425,'3','Classwork',2,'No fields changed.',33,1,'2015-04-15 02:02:52.361859');
INSERT INTO "django_admin_log" VALUES(426,'4','Bibliography',1,'',33,1,'2015-04-15 02:03:04.631387');
INSERT INTO "django_admin_log" VALUES(427,'5','Exam',1,'',33,1,'2015-04-15 02:03:09.123500');
INSERT INTO "django_admin_log" VALUES(428,'6','Exercise',1,'',33,1,'2015-04-15 02:03:44.054122');
INSERT INTO "django_admin_log" VALUES(429,'24','uploader',3,'',22,1,'2015-04-15 02:04:07.765363');
INSERT INTO "django_admin_log" VALUES(430,'23','uploader',3,'',22,1,'2015-04-15 02:04:07.934786');
INSERT INTO "django_admin_log" VALUES(431,'22','asdfasdf',3,'',22,1,'2015-04-15 02:04:08.124114');
INSERT INTO "django_admin_log" VALUES(432,'21','asdfasdf',3,'',22,1,'2015-04-15 02:04:08.290505');
INSERT INTO "django_admin_log" VALUES(433,'20','Rafael_Palmero_CV',3,'',22,1,'2015-04-15 02:04:08.479194');
INSERT INTO "django_admin_log" VALUES(434,'19','Rafael_Palmero_CV',3,'',22,1,'2015-04-15 02:04:08.658050');
INSERT INTO "django_admin_log" VALUES(435,'18','2010472',3,'',22,1,'2015-04-15 02:04:08.846420');
INSERT INTO "django_admin_log" VALUES(436,'17','2010472',3,'',22,1,'2015-04-15 02:04:09.035758');
INSERT INTO "django_admin_log" VALUES(437,'16','2010472',3,'',22,1,'2015-04-15 02:04:09.202610');
INSERT INTO "django_admin_log" VALUES(438,'15','KOC554U',3,'',22,1,'2015-04-15 02:04:09.382323');
INSERT INTO "django_admin_log" VALUES(439,'14','Babyface',3,'',22,1,'2015-04-15 02:04:09.549446');
INSERT INTO "django_admin_log" VALUES(440,'13','Babyface',3,'',22,1,'2015-04-15 02:04:09.715262');
INSERT INTO "django_admin_log" VALUES(441,'12','[u''Babyface'']',3,'',22,1,'2015-04-15 02:04:09.883022');
INSERT INTO "django_admin_log" VALUES(442,'11','png',3,'',22,1,'2015-04-15 02:04:10.071842');
INSERT INTO "django_admin_log" VALUES(443,'10','aanvragen-formulier-e301-pd-u1-werkloosheidsuitkering-buitenland-1213 (1)',3,'',22,1,'2015-04-15 02:04:10.272416');
INSERT INTO "django_admin_log" VALUES(444,'9','aanvragen-formulier-e301-pd-u1-werkloosheidsuitkering-buitenland-1213.doc',3,'',22,1,'2015-04-15 02:04:10.461314');
INSERT INTO "django_admin_log" VALUES(445,'8','14-15 notas - moodle.xls',3,'',22,1,'2015-04-15 02:04:10.650475');
INSERT INTO "django_admin_log" VALUES(446,'7','V',3,'',22,1,'2015-04-15 02:04:10.838504');
INSERT INTO "django_admin_log" VALUES(447,'6','asdfasdf',3,'',22,1,'2015-04-15 02:04:11.028596');
INSERT INTO "django_admin_log" VALUES(448,'5','IMG_20150208_131443.jpg',3,'',22,1,'2015-04-15 02:04:11.216670');
INSERT INTO "django_admin_log" VALUES(449,'4','IMG_20150208_13130.jpg',3,'',22,1,'2015-04-15 02:04:11.383824');
INSERT INTO "django_admin_log" VALUES(450,'3','IMG_20150208_131313.jpg',3,'',22,1,'2015-04-15 02:04:11.607978');
INSERT INTO "django_admin_log" VALUES(451,'2','IMG_20150208_131325.jpg',3,'',22,1,'2015-04-15 02:04:11.946666');
INSERT INTO "django_admin_log" VALUES(452,'1','IMG_20150208_131323.jpg',3,'',22,1,'2015-04-15 02:04:12.119618');
INSERT INTO "django_admin_log" VALUES(453,'2','Universidad',2,'Changed fileType.',22,1,'2015-04-16 15:54:28.562586');
INSERT INTO "django_admin_log" VALUES(454,'4','qwer',1,'',15,1,'2015-04-26 13:49:35.782876');
INSERT INTO "django_admin_log" VALUES(455,'15','Invalid level',1,'',28,1,'2015-05-10 13:53:58.511988');
INSERT INTO "django_admin_log" VALUES(456,'1','viperey',2,'Changed email.',15,1,'2015-05-10 15:11:51.143386');
INSERT INTO "django_admin_log" VALUES(457,'5','vipvip',2,'Changed confirmedEmail.',15,1,'2015-05-10 15:20:11.129597');
INSERT INTO "django_admin_log" VALUES(458,'5','vipvip',2,'Changed confirmedEmail.',15,1,'2015-05-10 15:21:56.207726');
INSERT INTO "django_admin_log" VALUES(459,'5','vipvip',2,'Changed confirmedEmail.',15,1,'2015-05-10 15:28:54.726126');
INSERT INTO "django_admin_log" VALUES(460,'5','vipvip',2,'Changed confirmedEmail.',15,1,'2015-05-10 15:30:42.153533');
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO "django_content_type" VALUES(1,'admin','logentry');
INSERT INTO "django_content_type" VALUES(2,'auth','permission');
INSERT INTO "django_content_type" VALUES(3,'auth','group');
INSERT INTO "django_content_type" VALUES(4,'auth','user');
INSERT INTO "django_content_type" VALUES(5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(6,'sessions','session');
INSERT INTO "django_content_type" VALUES(9,'rest','level');
INSERT INTO "django_content_type" VALUES(10,'rest','leveltype');
INSERT INTO "django_content_type" VALUES(11,'rest','noteboard');
INSERT INTO "django_content_type" VALUES(13,'rest','bannedhash');
INSERT INTO "django_content_type" VALUES(14,'rest','rol');
INSERT INTO "django_content_type" VALUES(15,'rest','user');
INSERT INTO "django_content_type" VALUES(19,'rest','calendarfrequency');
INSERT INTO "django_content_type" VALUES(21,'rest','year');
INSERT INTO "django_content_type" VALUES(22,'rest','file');
INSERT INTO "django_content_type" VALUES(23,'rest','tag');
INSERT INTO "django_content_type" VALUES(25,'rest','filereportlist');
INSERT INTO "django_content_type" VALUES(26,'rest','filecomments');
INSERT INTO "django_content_type" VALUES(28,'rest','errormessage');
INSERT INTO "django_content_type" VALUES(29,'rest','message');
INSERT INTO "django_content_type" VALUES(30,'rest','calendar');
INSERT INTO "django_content_type" VALUES(31,'rest','calendardate');
INSERT INTO "django_content_type" VALUES(32,'corsheaders','corsmodel');
INSERT INTO "django_content_type" VALUES(33,'rest','filetype');
INSERT INTO "django_content_type" VALUES(34,'sites','site');
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"), "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO "auth_permission" VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES(4,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES(5,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES(6,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES(7,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES(8,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES(9,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES(10,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES(11,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES(12,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES(13,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES(14,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES(15,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES(16,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES(17,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES(18,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES(25,9,'add_level','Can add level');
INSERT INTO "auth_permission" VALUES(26,9,'change_level','Can change level');
INSERT INTO "auth_permission" VALUES(27,9,'delete_level','Can delete level');
INSERT INTO "auth_permission" VALUES(28,10,'add_leveltype','Can add level type');
INSERT INTO "auth_permission" VALUES(29,10,'change_leveltype','Can change level type');
INSERT INTO "auth_permission" VALUES(30,10,'delete_leveltype','Can delete level type');
INSERT INTO "auth_permission" VALUES(31,11,'add_noteboard','Can add note board');
INSERT INTO "auth_permission" VALUES(32,11,'change_noteboard','Can change note board');
INSERT INTO "auth_permission" VALUES(33,11,'delete_noteboard','Can delete note board');
INSERT INTO "auth_permission" VALUES(37,13,'add_bannedhash','Can add banned hash');
INSERT INTO "auth_permission" VALUES(38,13,'change_bannedhash','Can change banned hash');
INSERT INTO "auth_permission" VALUES(39,13,'delete_bannedhash','Can delete banned hash');
INSERT INTO "auth_permission" VALUES(40,14,'add_rol','Can add rol');
INSERT INTO "auth_permission" VALUES(41,14,'change_rol','Can change rol');
INSERT INTO "auth_permission" VALUES(42,14,'delete_rol','Can delete rol');
INSERT INTO "auth_permission" VALUES(43,15,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES(44,15,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES(45,15,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES(55,19,'add_calendarfrequency','Can add calendar frequency');
INSERT INTO "auth_permission" VALUES(56,19,'change_calendarfrequency','Can change calendar frequency');
INSERT INTO "auth_permission" VALUES(57,19,'delete_calendarfrequency','Can delete calendar frequency');
INSERT INTO "auth_permission" VALUES(61,21,'add_year','Can add year');
INSERT INTO "auth_permission" VALUES(62,21,'change_year','Can change year');
INSERT INTO "auth_permission" VALUES(63,21,'delete_year','Can delete year');
INSERT INTO "auth_permission" VALUES(64,22,'add_file','Can add file');
INSERT INTO "auth_permission" VALUES(65,22,'change_file','Can change file');
INSERT INTO "auth_permission" VALUES(66,22,'delete_file','Can delete file');
INSERT INTO "auth_permission" VALUES(67,23,'add_tag','Can add tag');
INSERT INTO "auth_permission" VALUES(68,23,'change_tag','Can change tag');
INSERT INTO "auth_permission" VALUES(69,23,'delete_tag','Can delete tag');
INSERT INTO "auth_permission" VALUES(73,25,'add_filereportlist','Can add file report list');
INSERT INTO "auth_permission" VALUES(74,25,'change_filereportlist','Can change file report list');
INSERT INTO "auth_permission" VALUES(75,25,'delete_filereportlist','Can delete file report list');
INSERT INTO "auth_permission" VALUES(76,26,'add_filecomments','Can add file comments');
INSERT INTO "auth_permission" VALUES(77,26,'change_filecomments','Can change file comments');
INSERT INTO "auth_permission" VALUES(78,26,'delete_filecomments','Can delete file comments');
INSERT INTO "auth_permission" VALUES(82,28,'add_errormessage','Can add error message');
INSERT INTO "auth_permission" VALUES(83,28,'change_errormessage','Can change error message');
INSERT INTO "auth_permission" VALUES(84,28,'delete_errormessage','Can delete error message');
INSERT INTO "auth_permission" VALUES(85,29,'add_message','Can add message');
INSERT INTO "auth_permission" VALUES(86,29,'change_message','Can change message');
INSERT INTO "auth_permission" VALUES(87,29,'delete_message','Can delete message');
INSERT INTO "auth_permission" VALUES(88,30,'add_calendar','Can add calendar');
INSERT INTO "auth_permission" VALUES(89,30,'change_calendar','Can change calendar');
INSERT INTO "auth_permission" VALUES(90,30,'delete_calendar','Can delete calendar');
INSERT INTO "auth_permission" VALUES(91,31,'add_calendardate','Can add calendar date');
INSERT INTO "auth_permission" VALUES(92,31,'change_calendardate','Can change calendar date');
INSERT INTO "auth_permission" VALUES(93,31,'delete_calendardate','Can delete calendar date');
INSERT INTO "auth_permission" VALUES(94,32,'add_corsmodel','Can add cors model');
INSERT INTO "auth_permission" VALUES(95,32,'change_corsmodel','Can change cors model');
INSERT INTO "auth_permission" VALUES(96,32,'delete_corsmodel','Can delete cors model');
INSERT INTO "auth_permission" VALUES(97,33,'add_filetype','Can add file type');
INSERT INTO "auth_permission" VALUES(98,33,'change_filetype','Can change file type');
INSERT INTO "auth_permission" VALUES(99,33,'delete_filetype','Can delete file type');
INSERT INTO "auth_permission" VALUES(100,34,'add_site','Can add site');
INSERT INTO "auth_permission" VALUES(101,34,'change_site','Can change site');
INSERT INTO "auth_permission" VALUES(102,34,'delete_site','Can delete site');
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "username" varchar(30) NOT NULL UNIQUE);
INSERT INTO "auth_user" VALUES(1,'pbkdf2_sha256$20000$9ruSWi5rsWxb$Qu64e0/m6/uQdPEPNYBEtxQAw1u8NdzFJA1CY1ULNFg=','2016-02-18 17:32:45.293045',1,'','','viperey@gmail.com',1,1,'2014-10-19 18:02:05.468449','admin');
CREATE TABLE "django_site" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "domain" varchar(100) NOT NULL UNIQUE);
INSERT INTO "django_site" VALUES(1,'example.com','example.com');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('rest_leveltype',5);
INSERT INTO "sqlite_sequence" VALUES('rest_filetag',1);
INSERT INTO "sqlite_sequence" VALUES('rest_tag',5);
INSERT INTO "sqlite_sequence" VALUES('rest_year',3);
INSERT INTO "sqlite_sequence" VALUES('rest_message',14);
INSERT INTO "sqlite_sequence" VALUES('rest_rol',6);
INSERT INTO "sqlite_sequence" VALUES('rest_calendarregularevent',1);
INSERT INTO "sqlite_sequence" VALUES('rest_calendarfrequency',4);
INSERT INTO "sqlite_sequence" VALUES('rest_calendar',6);
INSERT INTO "sqlite_sequence" VALUES('rest_calendardate',31);
INSERT INTO "sqlite_sequence" VALUES('rest_level',7);
INSERT INTO "sqlite_sequence" VALUES('rest_user',5);
INSERT INTO "sqlite_sequence" VALUES('rest_user_subjects',307);
INSERT INTO "sqlite_sequence" VALUES('rest_noteboard',10);
INSERT INTO "sqlite_sequence" VALUES('rest_filetype',6);
INSERT INTO "sqlite_sequence" VALUES('rest_file',37);
INSERT INTO "sqlite_sequence" VALUES('django_migrations',16);
INSERT INTO "sqlite_sequence" VALUES('django_admin_log',460);
INSERT INTO "sqlite_sequence" VALUES('django_content_type',34);
INSERT INTO "sqlite_sequence" VALUES('auth_permission',102);
INSERT INTO "sqlite_sequence" VALUES('auth_user',1);
INSERT INTO "sqlite_sequence" VALUES('django_site',1);
CREATE INDEX auth_group_permissions_0e939a4f ON "auth_group_permissions" ("group_id");
CREATE INDEX auth_group_permissions_8373b171 ON "auth_group_permissions" ("permission_id");
CREATE INDEX auth_user_groups_e8701ad4 ON "auth_user_groups" ("user_id");
CREATE INDEX auth_user_groups_0e939a4f ON "auth_user_groups" ("group_id");
CREATE INDEX auth_user_user_permissions_e8701ad4 ON "auth_user_user_permissions" ("user_id");
CREATE INDEX auth_user_user_permissions_8373b171 ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX django_session_de54fa62 ON "django_session" ("expire_date");
CREATE INDEX rest_filecomments_cf721968 ON "rest_filecomments" ("idAuthor_id");
CREATE INDEX rest_filecomments_e291f4a8 ON "rest_filecomments" ("idFile_id");
CREATE INDEX rest_filereportlist_e291f4a8 ON "rest_filereportlist" ("idFile_id");
CREATE INDEX rest_filereportlist_72956280 ON "rest_filereportlist" ("idReporter_id");
CREATE INDEX rest_filetags_e291f4a8 ON "rest_filetag" ("idFile_id");
CREATE INDEX rest_filetags_3dcc8d15 ON "rest_filetag" ("idTag_id");
CREATE INDEX "rest_calendarregularevent_e969df21" ON "rest_calendarregularevent" ("author_id");
CREATE INDEX "rest_calendarregularevent_661e0fb9" ON "rest_calendarregularevent" ("lastUpdated_id");
CREATE INDEX "rest_calendarregularevent_b8f3f94a" ON "rest_calendarregularevent" ("level_id");
CREATE INDEX "rest_calendarregularevent_80359b49" ON "rest_calendarregularevent" ("frequency_id");
CREATE INDEX "rest_calendar_e969df21" ON "rest_calendar" ("author_id");
CREATE INDEX "rest_calendar_661e0fb9" ON "rest_calendar" ("lastUpdated_id");
CREATE INDEX "rest_calendar_b8f3f94a" ON "rest_calendar" ("level_id");
CREATE INDEX "rest_calendar_80359b49" ON "rest_calendar" ("frequency_id");
CREATE INDEX "rest_calendardate_dbcd9010" ON "rest_calendardate" ("calendarId_id");
CREATE INDEX "rest_level_403d8ff3" ON "rest_level" ("type_id");
CREATE INDEX "rest_level_410d0aac" ON "rest_level" ("parent_id");
CREATE INDEX "rest_user_subjects_6340c63c" ON "rest_user_subjects" ("user_id");
CREATE INDEX "rest_user_subjects_b8f3f94a" ON "rest_user_subjects" ("level_id");
CREATE INDEX "rest_user_b233ed9f" ON "rest_user" ("rol_id");
CREATE INDEX "rest_noteboard_b8f3f94a" ON "rest_noteboard" ("level_id");
CREATE INDEX "rest_noteboard_e969df21" ON "rest_noteboard" ("author_id");
CREATE INDEX "rest_file_56bb4187" ON "rest_file" ("subject_id");
CREATE INDEX "rest_file_cfde7537" ON "rest_file" ("year_id");
CREATE INDEX "rest_file_69b45c43" ON "rest_file" ("fileType_id");
CREATE INDEX "rest_file_8a3cba94" ON "rest_file" ("uploader_id");
CREATE INDEX "rest_file_a4f875da" ON "rest_file" ("lastUpdater_id");
CREATE INDEX "django_admin_log_417f1b1c" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_e8701ad4" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE UNIQUE INDEX "auth_permission_content_type_id_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_417f1b1c" ON "auth_permission" ("content_type_id");
COMMIT;
