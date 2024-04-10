## **Proyecto 1 -  Tópicos Especiales de Telemática** 

**Integrantes:** 

- Esteban Trujillo Carmona 
- Viviana Hoyos Sierra
- Damian Duque Lopez
- Valentina Morales Villada 
 

## **Parte 1, Marco teórico y Conceptos clave:** 

**Sistemas Distribuidos de Archivos basados en Bloques:**

- La unidad básica de almacenamiento y transferencia de datos es el bloque. 
- Los archivos se dividen en bloques de tamaño fijo que se distribuyen en diferentes nodos del sistema. 
- Cada bloque de un archivo puede estar replicado en múltiples nodos para garantizar la tolerancia a fallos y la disponibilidad de los datos. 
- La lectura y escritura de archivos se realiza a nivel de bloque, lo que permite una distribución eficiente de la carga de trabajo y una mayor escalabilidad. 
- Ejemplos de sistemas distribuidos de archivos por bloques incluyen el Google File System (GFS) y el Hadoop Distributed File System (HDFS). 

**Sistemas Distribuidos de Archivos basados en Objetos:**

- La unidad básica de almacenamiento y acceso es el archivo completo en lugar de bloques individuales. 
- Estos sistemas están diseñados para un enfoque Write-Once-Read-Many (WORM), lo que significa que los archivos se escriben una vez y se leen muchas veces. 
- No  admiten  la  actualización  parcial  de  archivos,  por  lo  que  se  debe reemplazar todo el archivo en caso de modificaciones. 
- Los  sistemas  de  archivos  por  objetos  suelen  ser  altamente  escalables, redundantes y eficientes en términos de rendimiento. 
- Aunque  los  clientes  ven  los  archivos  como  entidades  completas,  en  el backend se pueden utilizar mecanismos de particionamiento para mejorar la escalabilidad y el rendimiento. 
- Ejemplos de sistemas distribuidos de archivos por objetos incluyen Amazon S3 y otros servicios de almacenamiento en la nube. 

**GFS (Google File System)** 

Es un sistema de archivos distribuido, escalable y de alto rendimiento desarrollado por Google para sus necesidades específicas de almacenamiento de datos a gran escala. Se basa en la idea de dividir los datos en grandes bloques (chunk) y distribuirlos en miles de servidores independientes. Suele utilizarse para almacenar grandes cantidades de datos en aplicaciones como almacenamiento de archivos en Google drive y correos electrónicos en Gmail. 

**Características principales:**

- Escalabilidad 
- Alto rendimiento 
- Disponibilidad 
- Consistencia 

**Algunas desventajas de GFS pueden ser:** 

- Complejidad 
- Alto costo cuando se implementa a gran escala 

**HDFS (Hadoop Distributed File System)**

Es  un  sistema  de  archivos  distribuido  de  código  abierto  que  se  utiliza  para almacenar  grandes  conjuntos  de  datos  en  clústeres  de  computadoras.  Es  un componente central del ecosistema de Hadoop, una plataforma de software para el procesamiento de Big data. 

Características principales: 

- Escalabilidad 
- Alto rendimiento 
- Disponibilidad 
- Simplicidad 
- Costo 

**Algunas desventajas de HDFS pueden ser:**

- No es eficiente si se utiliza para cantidades pequeñas de datos. 
- No es adecuado para aplicaciones de alta latencia o que requieran acceso rápido a los datos. 

**Comparación y evaluación de características entre Sistemas por Bloques y por Objetos:** 



|Características |Sistemas por Bloques |Sistemas por objetos |
| - | - | - |
|*Modelo de datos* |Organiza los datos en bloques de tamaño fijo (chunks o particiones)|Organiza los datos en objetos, cada uno con metadatos |
|*Escalabilidad* |Escalabilidad vertical limitada|Escalabilidad horizontal y vertical |
|*Latencia* |Baja latencia en operaciones de lectura y escritura debido al acceso directo que se tiene a los datos|Mayor latencia debido al acceso a través de metadatos, requiriendo más tiempo para acceder a los datos. |
|*Tamaño máximo de archivo* |Es limitado por el tamaño del bloque|No hay un límite para el tamaño de los objetos|
|*Operaciones* |Eficiente para operaciones de lectura y escritura|Más eficiente para operaciones de lectura y objetos grandes|
|*Metadatos* |Almacenados en un sistema de metadatos distribuido|Almacenados junto con el objeto en sí|
|*Consistencia* |Puede implementarse dentro del sistema, variando en dificultad dependiendo del nivel que se desea garantizar |Puede implementarse dentro del sistema, variando en dificultad dependiendo del nivel que se desea garantizar |

**Glosario general:**

GRPC:  Framework  de  comunicación  de  servicios  remotos  de  código  abierto desarrollado por Google que permite la comunicación eficiente entre aplicaciones distribuidas. 

API REST: Interfaz de programación de aplicaciones que utiliza el protocolo HTTP para realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) en recursos de forma uniforme y sin estado. 

Filezilla: Cliente FTP que permite realizar la transferencia de archivos mediante una interfaz gráfica de usuario que facilita la gestión de archivos y la navegación entre directorios en el servidor. 

FTP (File Transfer Protocol): Protocolo utilizado para la transferencia de archivos entre sistemas dentro de una red que permite subir y descargar archivos desde un servidor a su propia máquina. 

Query: Solicitud específica enviada a un sistema con unos criterios preestablecidos, que espera por una respuesta específica. 

Chunk: Se refiere a un bloque, que contiene una parte de información específica de un archivo. 

Cluster:  Conjunto  de  computadoras  interconectadas  que  trabajan  juntas  para realizar tareas complejas o procesar grandes volúmenes de datos. 

Namenode:  Componente  central  del  sistema  de  archivos  distribuido  Hadoop, responsable de la gestion del espacio de nombres del sistema de archivos y la asignación de bloques de datos a los datanodes. 

Datanode: Nodos en un sistema de archivos distribuido Hadoop que almacenan y gestionan los bloques de datos reales. 

Read: Operación de lectura de datos desde una fuente de almacenamiento, como un archivo o una base de datos. 

Write: Operación de escritura de datos en una fuente de almacenamiento, como un archivo o una base de datos. 

Insert: Acción de añadir nuevos datos a una fuente de almacenamiento, como una base de datos. 

Write sync: Técnica de sincronización que asegura que los datos escritos se han almacenado en el dispositivo de almacenamiento antes de confirmar la operación de escritura. 

Ack sync: Confirmación de sincronización que indica que los datos escritos han sido almacenados en el dispositivo de almacenamiento y están disponibles para su posterior lectura. 

Filename: Representa el nombre dado a un archivo para identificarlo dentro de un sistema de archivos. 

## **Parte 2, Diseño e implementación:** 


#### **Servicios**

Se tienen en cuenta dos servicios principales para el sistema: 

 - **FileTransfer:** Permite la transferencia de archivos entre cliente y datanodes leaders. Las operaciones que se realizan son lectura (read) y escritura (write), ambas operaciones consisten en una request de parte del cliente y una respuesta del datanode leader.
 - **NamenodeService:** Se refiere al servicio central del sistema, se comunica con todos los nodos del sistema y con el cliente. Entre las operaciones que realiza están las primitivas de un sistema de archivos open, create, ls (listar archivos) y algunas operaciones adicionales como heartbeat (para chequear el estado de los datanodes), report (reportar los chunks una vez sean recibidos) y get_followers (para el datanode leader de cada cluster a la hora de realizar la replicación de sus chunks).


#### **Tipo de arquitectura.** 

Se establece una arquitectura de tipo cliente-servidor, donde se identifica un cliente, bien sea un computador u otra instancia de AWS; y un servidor, donde se tiene un Namenode, el cual atiende las solicitudes iniciales del cliente y retorna la información respectiva. 

![image](https://github.com/DamianDuque/st0263-Proyecto1-DFS/assets/83479274/04273c11-765a-473a-95f0-efa60f528e63)


#### **Tipo de comunicación.** 

Se establecen los siguientes tipos de comunicación según los elementos implicados y los contextos o casos específicos: 

- Cliente <-> Namenode: gRPC (HTTP/2).
- Cliente <-> Datanode Leader: gRPC (HTTP/2).
- Datanode Leader <-> Datanode Follower: gRPC (HTTP/2).
- Namenode <-> Datanode: gRPC (HTTP/2). 

### **Middlewares usados.** 

Para efectos del proyecto 1, se establece el uso de gRPC, para las comunicaciones previamente mencionadas. 

#### **Nodos involucrados.** 

Se tiene los siguientes nodos involucrados en el sistema de archivos: 

- **Namenode leader:** encargado de llevar a cabo la comunicación inicial con el cliente, la cual involucra los procesos de lectura, escritura e inserción de ficheros (chunks agrupados). Manda al cliente la información relacionada con la  localización  de  los  datanodes  (URLs),  la  ubicación  de  los  chunks respectivos, y la disponibilidad de datanodes para escribir o insertar. Así, este almacena toda esa información a manera de metadatos. 
- **Datanode leader:** encargado de almacenar los chunks de los archivos que le envía el cliente. Además de ser el líder de su clúster, realiza las réplicas de los chunks que tiene almacenados en los followers que tiene asignados a su clúster, esto se hace cada vez que el cliente realiza una operación, ya sea de escritura o inserción (append).
- **Datanode follower:** encargado de recibir y almacenar una réplica de un chunk, la cual le es entregada por su datanode leader. En esta versión del sistema, los datanodes followers solo tienen las réplicas de los archivos que tiene el líder de su clúster.

### **Retos**

Para el diseño e implementación de un sistema de archivos distribuido basado en HDFS, se asumen unos retos importantes y que son clave para la eficiencia del sistema y su buen funcionamiento, a continuación se darán más detalles de cómo se abordaron estos.

#### **Particionamiento** 
Para solucionar este reto inicial se comenzó por definir si el tamaño de los bloques iba a ser fijo o variable, en este caso decidimos que fuera fijo ya que esto facilita el particionamiento de los archivos, sin importar su tamaño total. El cliente es el encargado de particionar el archivo y luego se enfoca en enviar los chunks del archivo a los datanodes leaders disponibles (vivos) que el namenode le proporcionó. 

El criterio que usa el cliente para distribuir estos chunks en los datanodes leaders se basa en el algoritmo de planificación Round Robin, que distribuye los chunks de manera equitativa entre los nodos disponibles, esto se tiene en cuenta para la escritura.
El criterio de elección de chunks para la lectura es simplemente aleatorio dentro de la tabla de índices que tiene el namenode. 

Adicional a esto, el cliente al hacer lectura de un archivo toma los chunks de datanodes aleatorios, sin importar si son leaders o followers, unifica los chunks del archivo y reconstruye el archivo a partir de estos.


#### **Tolerancia a fallos** 

Primero se creó un criterio para elegir los datanodes leaders de cada clúster, este consistía en que en un sistema de dos clústers, los dos primeros datanodes en inicializarse, serían los datanodes leaders de cada uno de los clústers, y cuando se llegue a inicializar un tercer datanode, este sería asignado como follower a alguno de los datanodes leaders que ya existen. A continuación se muestra como se hace esta asignación gráficamente.

![mimi2](https://github.com/DamianDuque/st0263-Proyecto1-DFS/assets/83479274/a4b59a5a-1dab-4c1d-80ed-3af14e5facd5)


Para la tolerancia a fallos, tenemos en cuenta varios casos. Tenemos un hilo que está corriendo concurrentemente con el sistema que sirve para verificar cuáles datanodes están vivos recorriendo la lista de datanodes disponibles, se guarda el tiempo del último heartbeat que hizo el datanode y si ha pasado un tiempo mayor al ttl después del último heartbeat se cambia el estado del datanode de vivo a muerto. Luego si ese que justo murió resulta que tambien era leader de su clúster se procede con el protocolo de elección de nuevo leader dentro del clúster, teniendo como candidatos a todos los datanodes vivos y finalmente se escoje al primero de esta lista.

Ese nuevo leader toma el rol de leader (ya que antes era follower) y se actualiza su rol para que el namenode lo tenga en cuenta en su lista de leaders para la próxima vez que un cliente quiera hacer escritura de un archivo. Hay que tener en cuenta que cuando el leader muere, guarda su id y el id de su clúster para que a la hora de reiniciarse este pueda llegar como follower a su clúster original y recuperar sus archivos fácilmente.
De igual manera, cuando cae un follower, deja guardado su id y el de su clúster para una vez reiniciado volver fácilmente a su clúster original, pero esta vez no cambiaría su rol, seguiría de follower.


#### **Replicación** 
Este reto fue importante ya que implicaba otras características dentro del sistema como la consistencia de datos y la tolerancia a fallos. 

En cuanto a la replicación, la realiza el datanode leader siempre que el cliente hace una operación de escritura o inserción. Para esto le pide al namenode la lista de los followers que tiene en su clúster para realizarle write a cada uno de los followers dentro de esa lista. Además de esto cumpliríamos con otro reto que se refiere a la consistencia de datos, la cual en este caso es eventual, ya que aunque se pueda tardar un poco de tiempo en visualizarse los cambios por diferentes factores, eventualmente los datos serán consistentes a través de todos los nodos del clúster. 


#### **Mantenimiento de la red**

Este reto se refiere en general a quienes debe conocer cada nodo del sistema.
 - El cliente solo conoce al namenode y hace un binding dinámico con los datanodes, ya que cada que va a hacer lectura o escritura de algún archivo, se comunica con datanodes diferentes.
 - El namenode por otro lado es el nodo principal del sistema, por lo que debe conocer a todos los nodos dentro del sistema, ya sean leaders o followers.
 - El datanode leader conoce al namenode, ya que siempre está mandándole ping para que este sepa que está vivo, y conoce al cliente de forma dinámica, solo cuando este está realizando operaciones de lectura y escritura. 

Adicional a esto en cuanto al diseño del sistema de archivos y directorios cada datanode almacena los archivos dentro de una carpeta /resources y dentro de esta tendrá los chunks de los archivos que el cliente le envíe. Cabe aclarar que en este sistema de archivos un archivo se trata como un directorio cuyos archivos son las particiones del archivo original. Este es un ejemplo:

```
datanode
├── resources
│   └── file.txt
│       ├── partition0001.txt
│       └── partition0002.txt
│       └── partition0003.txt
│       └── partition0004.txt
```


### **Procesos y acciones en el sistema.** 

Se tienen tres procesos o acciones que se realizan en el sistema de archivos, los cuales  son  **lectura,**  **escritura**  e  **inserción**  de  archivos/ficheros.  Se  describen detalladamente a continuación: 



[Link a los diagramas](https://drive.google.com/file/d/1sfBs_RcWt6Z0fTkYj7gB9jmrc1EWevTQ/view?usp=sharing)


#### **Proceso de lectura:** _open_ 

1. Un cliente se comunica con el namenode leader solicitando la lectura de determinado archivo indicando el nombre de archivo.
1. El namenode le envía al cliente la lista de ubicaciones de los datanodes que tienen los chunks que componen el archivo y el nombre de cada chunk con la localización.
1. Con la información recibida, el cliente se dirige posteriormente a cada uno de los datanodes para solicitar el chunk respectivo que poseen.
1. Los  datanodes  le  envían  respectivamente  los  chunks solicitados al cliente.
1. El cliente, una vez tiene todos los chunks de determinado archivo que estaba buscando, pasa a recomponerlo, y posteriormente a leerlo.
####
#### **Proceso de escritura:** _create_

1. El cliente se comunica con el namenode leader para solicitarle la escritura en un determinado archivo. 
1. El namenode le entrega al cliente la ubicación de los datanodes líderes que están disponibles es decir vivos.
1. El cliente se comunica con los datanodes líderes para escribir los chunks del archivo.
1. Por cada chunk escrito dentro de un datanode el cliente recibe un reporte de que el chunk fue escrito con éxito.
1. Con un reporte final el cliente confirma la escritura del archivo en el sistema. 
1. Una vez el cliente haya escrito los chunks, el datanode leader le pide al namenode una lista de los followers que este tiene en su clúster.
1. El datanode leader se comunica con los datanodes followers de su cluster para replicar los chunks que acaba de escribir.
1. Por cada chunk escrito dentro de un datanode el namenode recibe un reporte de que el chunk fue escrito con éxito en los followers. 
1. El namenode actualiza su tabla de metadatos con los nuevos chunks ingresados.
6. Una  vez  hechas  las actualizaciones en  la  tabla de  metadatos,  el namenode le envía a cada datanode un mensaje OK de confirmación.

####
#### **Proceso de inserción.** _append_
1. El cliente se comunica con el namenode leader para solicitarle la inserción de un chunk a un archivo existente en el sistema. 
1. El namenode leader le entrega al cliente la ubicación de los datanodes disponibles para inserción que serán líderes de sus clusters.
1. El cliente se comunica con los datanodes líderes para crear en ellos el chunk que le corresponde.
1. Por cada chunk escrito dentro de un datanode el namenode recibe un reporte de que el chunk fue escrito con éxito. 
1. Con un reporte final el cliente confirma la escritura del chunk en el sistema. 
1. Una vez el cliente haya escrito los chunks, el datanode leader le pide al namenode una lista de los followers que este tiene en su clúster.
1. El datanode leader se comunica con los datanodes followers de su cluster para replicar los chunks que acaba de escribir.
1. Por cada chunk escrito dentro de un datanode el namenode recibe un reporte de que el chunk fue escrito con éxito. 
6. Una  vez  se  hayan  insertado  todos  los  chunks  del  archivo  en  lo datanodes líderes, y sus réplicas en los datanodes followers, el namenode actualiza su tabla de metadatos con los nuevos chunks ingresados.
6. Una  vez  hechas  las actualizaciones en  la  tabla de  metadatos,  el namenode leader le envía a cada datanode un mensaje OK de confirmación.


### **Especificaciones adicionales**

Algunas especificaciones que vale la pena mencionar.

- Se configuraron archivos .env para cada nodo del sistema (namenode, datanode, cliente) en donde se agregan las configuraciones de cada nodo, es decir, el bootstrap.
- Funciones del NamenodeService: 
   - heartbeat, se hace cada cierto tiempo desde los datanodes al namenode, para indicarle que está vivo. 
   - report, se utiliza para reportar cada uno de los chunks al namenode o al cliente depende del caso, para confirmar la escritura o inserción de un chunk en un datanode.
   - get_followers, se usa para generar la lista de datanodes followers de un datanode leader en un cluster específico.


# **Instrucciones para ejecutar el proyecto**

### Prerequisitos

* Python3
* pip3

1. Instalar los requerimientos del proyecto:
- Ir al directorio principal del proyecto.
- Usar 'pip' para instalar la lista de requerimientos necesarios.

```bash
pip3 install -r requirements.txt
```   
        
2. Ejecutar el namenode en una consola:
    ```bash
    python namenode/main.py
	```
	
3. Ejecutar el namenode en una consola:
    ```bash
    python namenode/main.py
    ```

A continuación, están los comandos para realizar las operaciones soportadas por el sistema de archivos. 
	
- **open**:  abrir un archivo *file.txt* existente dentro del sistema. Los archivos descargados quedan almacenados en el directorio *client/resources/downloaded_files*:
    ```bash
    python -m client.main open -out client/resources/downloaded_files -f file.txt        
    ```
        
- **create**: crear un archivo nuevo *file.txt*:
    ```bash
    python -m client.main create -out client/resources/partitioned_files -in client/resources/complete_files -f file.txt   
    ```
        
- **append**: agregar bloques nuevos *b.txt* a un archivo existente *a.txt* (por default en un directorio constante)
    ```bash
    python -m client.main append -out client/resources/partitioned_files -in client/resources/complete_files -f b.txt -fdfs a.txt
    ```
        
- **ls**: listar los archivos dentro del sistema:
    ```bash
    python -m client.main ls 
    ```
        
- **help**: mostrar ayuda sobre los comandos:
    ```bash
    python -m client.main  -h
    ```
  

# **Referencias**

### grpc-file-transfer

SSL secured file transfer gRPC client and server written in Python language.
Original Repo: https://github.com/r-sitko/grpc-file-transfer/blob/master/server/main.py



Link del video 

