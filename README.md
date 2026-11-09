# Examen Segundo Parcial: Pipeline de datos contenerizado

**Alumno:** Dana Morales
**Matrícula:** 125055192
**Pregunta asignada:** Ticket promedio (ingreso promedio por registro) por tienda.

## Cómo reproducir

1. Copiar `.env.example` a `.env` y poner una contraseña real.
2. Generar el dataset: `python3 generar_dataset.py 125055192` (el CSV queda en la raíz y no se sube a Git).
3. Levantar todo: `docker compose up --build -d`
4. Correr el job en Hadoop:
   - `docker compose exec -u hadoop hadoop bash`
   - `cd ~/mapreduce`
   - `hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -input /data/input/ventas_125055192.csv -output /data/output/resultado -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py`
5. Copiar el resultado: `docker cp hadoop-nodo:/data/output/resultado/part-00000 evidencias/hadoop_out.txt`
6. Cargar a la BD: `docker compose exec api python /scripts/cargar_resultados.py`
7. Probar la API: `http://localhost:5000/resultados` y `http://localhost:5000/resultados/T001`

## SSH entre contenedores

- Dentro de hadoop: `docker compose exec -u hadoop hadoop ssh localhost whoami`
- Desde api hacia hadoop (la llave se copia en tiempo de ejecución, no queda en la imagen ni en Git):
  `docker compose exec api ssh -o StrictHostKeyChecking=no hadoop@hadoop whoami`

## Tiempos medidos

| Método | Tiempo real |
|---|---|
| Hadoop Streaming (standalone) | 23.464 s |
| Python secuencial | 8.432 s |

Los resultados coinciden (`diff` sin diferencias).

## Comparativa de rendimiento

Para este dataset de ~352 MB el script secuencial (8.4 s) fue más rápido que Hadoop Streaming (23.5 s). Hadoop en modo standalone corre en una sola máquina, así que no obtiene paralelismo real entre nodos, pero sí paga costos fijos: arrancar la JVM, planificar el job, lanzar procesos Python para el mapper y el reducer, ordenar (shuffle) y escribir archivos intermedios. El script secuencial lee el archivo una vez y acumula en memoria sin ese sobrecosto. MapReduce conviene cuando los datos no caben en una máquina o están distribuidos en HDFS entre varios nodos, donde el paralelismo compensa esos costos.

## Evidencias

Capturas en `evidencias/`: `hadoop version`, `ssh localhost`, `ssh api→hadoop`, salida del job con tiempo, `diff`, respuesta de la API y persistencia tras `docker compose down` / `up`.

## Teoría

**1. Modos de Hadoop.** En standalone todo corre en un solo proceso Java, sin demonios y sin HDFS. En pseudo-distribuido los demonios (NameNode, DataNode, etc.) corren en una sola máquina, simulando un clúster. En totalmente distribuido los demonios se reparten en varios nodos. HDFS se usa en pseudo-distribuido y en distribuido.

**2. Volumen vs COPY.** (a) La imagen no se infla con 352 MB. (b) Los datos se pueden cambiar sin reconstruir la imagen. (c) La imagen se puede compartir sin incluir los datos. (d) Con `:ro` el contenedor no puede modificar el original.

**3. `down` vs `down -v`.** `docker compose down` elimina contenedores y redes, pero el volumen nombrado `pgdata` se conserva, así que los datos de la base siguen ahí. `docker compose down -v` también elimina los volúmenes, y los datos de la base se pierden.

**4. MapReduce vs secuencial.** Con 352 MB, los costos fijos de Hadoop (JVM, planificación, shuffle, archivos intermedios) superan el beneficio, como mostraron mis tiempos (23.5 s contra 8.4 s). Conviene con datos de decenas o cientos de GB, que no caben en una máquina, y con un clúster con HDFS donde el
