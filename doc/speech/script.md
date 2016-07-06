Dos bloques.

Negocio y tecnico.

Negocio.

Un storytelling de un alumno.

Noticias y documentos: los busca en google o termina dando vueltas por el moodle buscando algo. P,ej: el horario de tutorías.
El calendario: termina usando el excel.
Asignaturas: tiene varios moodles, es dificil saber a veces cual es cual.

Aparte. Los dropbox de asignatura o trabajo. Un lio de la hostia. Fomentar la educacion por repeticion no por reflexion.

Es tiempo, es hastío, es ineficiente, es costoso.

Benancio esta hasta el gorro de esta mierda.
Bueno vale, Benancio soy yo, he pasado por esto y me gustaría pensar que nadie más va a pasar por esto.

Vale, pongamos solución a esto. Un sitio, centralizamos, abrimos a los estudiantes, los involucramos.

Vale, suena bien. Hablemos de código.

Bien, he aquí el segundo pilar del proyecto. Moodle en sí como plataforma.

Es monolítico y propio de principio a fin.
No va a ser una crítica como tal a Moodle, porque estar está y funciona.
Es una reflexión en como el mundo del software ha evolucionado y como esa evolucion afecta a una "reescritura" de moodle en terminos teoricos.
PHP!!!! En realidad no tanto PHP sino lo que a veces representa, lo monolitico.
Si se empezase de cero...errores a cometer, velocidad, personal, etc.

Foto de la arquitectura de Moodle.

Vale, esto ha cambiado bastante ultimamente, echemos un vistazo a que hay de nuevo.
Algo sobre el acoplamiento del front y el back.

Con respecto al front, como queda libre de logica en su mayoría y son dummies. Pintan cosas, enlazan datos, reaccionan a cambios. Poca lógica más.
SPA. Importante. Peso.
Al apoyar en FW, el codigo es mucho mas de enlace, mucho mas dummie. Mas ligero, diapo con codigo al respecto.
API Rest. Un contrato publico, menos oscuro en las consecuencias.
Ligero y primer paso a las aplicaciones moviles.
Mostrar o mencionar Postman.

Una diapo a modo de ejemplo de como Django se come algunos componentes que Moodle tiene que mantener.
Un back más seguro, se prueba y desarrolla mejor. Desacoplar implica tener capas de ataque en las pruebas mas pequeñas.
Menos efectos laterales entre front y back.
En pruebas de integracion, la caja negra son varias pero pequeñas.

La idea de que a mismos recursos podriamos ser commiters en django (p.ej) y ayudar al resto del mundo.

Hablemos de desplegar, provisionar, hacer copias de seguridad.
Lo primero. https://docs.moodle.org/31/en/Category:Installation ESTE PUTO MONSTRUO. No por moodle en si, es el enfoque.

Gestores de dependencias y de tareas. Imprescindible. Para simplificar el proceso, para reducir la friccion a la hora de mantener los sistemas.
Actuan de capa intermedia de confianza para simplificar todo.
Siendo justos, p.ej. moodle ha comenzado recientemente a integrar algunos de estos aspectos: https://github.com/moodle/moodle/blob/master/package.json
Febrero de 2015.
el uso de FW compartimenta los efectos de ejecutar codigo.

Entonces. Tenemos el problema, tenemos los aspectos tecnicos del desarrollo software del mundo moderno. El señor cangrejo. Mucho swag y mucho hype.

Vale, comenzamos a construir.
Andamiaje con Python, Django, sus plugins.
Miramos las capas, lo que Django da, se negocia, algunas partes de hacen de 0 por diversas necesidades, se ajusta el FW.
Resultado de las 3/2.5 capas hechas. Depende de si se mira por organización de codigo y nomenclatura o funcionalidad real.
Repaso rapido a las capas. ¿Dará tiempo?
Datos de provision, backups.
Pip y los scripts para casi todo.

Vamos al front. Js, Angular, CSS, compass.
Repaso a las capas. Mas rapido que en el back.
Bower, NPM. Los plugins de angular mediante los gestores.
Grunt y demas.


Terminado el tema tecnico. Vamos a los resultados.
Entonces un repaso por las funcionalidades básicas.
Noticias, el tema de los niveles de vista y el sistema de filtrado.
  No pagina, evita un sistema de busqueda en servidor y reutiliza funcionalidades de FW de frontal.

Calendario. Eventos únicos o recurrentes.

Asignaturas, pasar por el arbol, ir a una, tener un par de ficheros subidos, pruebas de edicion, etc.
Subir un fichero, hacer una prueba de filtrado, borrar, etc.
El tema de los colores en las etiquetas.
Si consigo hacer un checkout decente y que funcione...edicion de asignaturas.   

Basicamente con esto está todo.

Conclusiones.
Doble conclusion. Comenzar con la tecnica. El enfoque más actual, que salio bien la eleccion de lenguaje y FW. Que la API está justificada. Que hay pruebas.
Que despliega, provisiona, etc.
Sencillo de mantener.
El front. Principalmente que es ligero, que carece de logica, que está bien estructurado. Está bajo control.

Que es un buen resultado a nivel de un proceso de ingenieria de software.
Es decir, se parte de un problema, se toman las abstracciones, se llevan a codigo adaptando el desarrollo a necesidades (adquiriendo conociemientos), no al reves. No se parte del conocimienot para hacer algo X. Prueba de que no sabia python cuando comence.
Los FW han demostrado cumplir con su proposito.
Que ha sido relativamente agil, pero que al ser uno es postureo decirlo, pero si ha sido incremental y que el tener competencias definidas permite hacer procesos incrementales sobre el codiog.

A nivel de logica.
Enlazando al tema del proceso de ingenieria de software, que la conclusion es que se entrega algo que representa una solucion a problemas reales en la escuela.
Que como ejercicio teorico esta bien, pero esto no es para produccion, sin embargo es un toque de atención para la situacion de la escuela y la universidad.
Y que es dificil de entender y probablemente de justificar que una escuela de programacion no colabore en el mundo del software libre mas visiblemente.
