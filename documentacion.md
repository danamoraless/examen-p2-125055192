## Parte E. Teoría

**1. Modos de Hadoop.**
En modo *standalone* todo corre en un solo proceso Java, sin demonios y usando el sistema de archivos local; es el que usé en el examen. En modo *pseudo-distribuido* los demonios (NameNode, DataNode, ResourceManager, NodeManager) corren en una sola máquina, cada uno en su proceso, simulando un clúster. En modo *totalmente distribuido* esos demonios se reparten en varias máquinas reales. HDFS se usa en pseudo-distribuido y en totalmente distribuido; en standalone no.

**2. Volumen vs `COPY`.**
(a) El CSV pesa ~352 MB y con `COPY` inflaría la imagen y cada capa del build. (b) Con un volumen el dato se puede cambiar o regenerar sin reconstruir la imagen. (c) La imagen queda reutilizable y se puede compartir sin los datos, lo cual evita subir el CSV al repositorio. (d) Con `:ro` el contenedor solo puede leer, así que no puede alterar el dataset original.

**3. `down` vs `down -v`.**
`docker compose down` elimina los contenedores y la red, pero el volumen nombrado `pgdata` se conserva, así que los datos de la base siguen ahí al volver a levantar. `docker compose down -v` además elimina los volúmenes, por lo que se pierden los datos de la base y hay que volver a cargarlos con `cargar_resultados.py`.

**4. MapReduce vs script secuencial.**
Con 352 MB, Hadoop paga costos fijos: arrancar la JVM, planificar el job, lanzar procesos Python para mapper y reducer, hacer el shuffle/sort y escribir archivos intermedios. En mis mediciones, Hadoop tardó 23.5 s y el script secuencial 8.4 s. MapReduce conviene cuando los datos son de decenas o cientos de GB, no caben en una sola máquina, y hay un clúster con HDFS donde el procesamiento se paraleliza entre nodos.

**5. `CMD` vs `ENTRYPOINT`, y `COPY` vs `ADD`.**
`ENTRYPOINT` define el ejecutable fijo del contenedor; `CMD` define el comando o los argumentos por defecto y se puede sobrescribir al hacer `docker run`. `COPY` solo copia archivos locales a la imagen; `ADD` además descomprime archivos tar locales y acepta URLs. Se recomienda `COPY` salvo que se necesite lo extra de `ADD`.
