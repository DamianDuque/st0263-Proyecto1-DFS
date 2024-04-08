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

## **Parte 2, Definición de la arquitectura:** 

#### **Links a los diagramas:** 

Nota: El enlace del draw.io cuenta con 4 páginas dentro de las cuales se puede navegar haciendo clic en cada una en la zona inferior izquierda de la pantalla. 

[https://app.diagrams.net/#G1QsR62IPo64Cy1O6ZEqbIRJc4tsTwLNg1#%7B"pageI d"%3A"u2NyXphamRmL1Mq-LfcO"%7D ](https://app.diagrams.net/#%7B"pageId"%3A"u2NyXphamRmL1Mq-LfcO"%7D)

#### **Tipo de arquitectura.** 

Se establece una arquitectura de tipo cliente-servidor, donde se identifica un cliente, bien sea un computador u otra instancia de AWS; y un servidor, donde se tiene un Namenode leader, el cual atiende las solicitudes iniciales del cliente y retorna la información respectiva. 

#### **Tipo de comunicación.** 

Se establecen los siguientes tipos de comunicación según los elementos implicados y los contextos o casos específicos: 

- Cliente <-> Namenode: gRPC (HTTP/2).
- Cliente <-> Datanode: gRPC (HTTP/2).
- Datanode <-> Datanode: gRPC (HTTP/2).
- Namenode <-> Datanode: gRPC (HTTP/2). 

### **Middlewares usados.** 

Para efectos del proyecto 1, se establece el uso de gRPC, para las comunicaciones previamente mencionadas. 

#### **Nodos involucrados.** 

Se tiene los siguientes nodos involucrados en el sistema de archivos: 

- **Namenode leader:** encargado de llevar a cabo la comunicación inicial con el cliente, la cual involucra los procesos de lectura, escritura e inserción de ficheros (chunks agrupados). Manda al cliente la información relacionada con la  localización  de  los  datanodes  (URLs),  la  ubicación  de  los  chunks respectivos, y la disponibilidad de datanodes para escribir o insertar. Así, este almacena toda esa información a manera de metadatos. 
- **Namenode follower:** encargado de relevar al namenode leader cuando este falle, se desconecte o no funcione por algún motivo. Por lo tanto, en tales casos realizará las mismas acciones que el namenode leader. 
- **Datanode leader:** encargado de almacenar y replicar en los nodos follower un chunk que le fue asignado por el cliente. De igual forma, un datanode leader  puede  ser  al  mismo  tiempo  un  datanode  follower  de  otro  chunk distinto, en tanto para ese caso no le fue asignada la responsabilidad de replicación, sino solo la de almacenaje. 
- **Datanode follower:** encargado de recibir y almacenar una réplica de un chunk, la cual le es entregada por el datanode leader, o por algún otro datanode follower del mismo chunk. 

### **Procesos y acciones en el sistema.** 

Se tienen tres procesos o acciones que se realizan en el sistema de archivos, los cuales  son  **lectura,**  **escritura**  e  **inserción**  de  archivos/ficheros.  Se  describen detalladamente a continuación: 


**Proceso de lectura:**  

1. Un cliente se comunica con el namenode leader solicitando la lectura de determinado archivo indicando el nombre de archivo.
1. El namenode leader le envía al cliente la lista de ubicaciones de los chunks que componen el archivo, el índice de cada chunk, y su orden en el archivo completo, respectivamente.
1. Con la información recibida, el cliente se dirige posteriormente a cada uno de los datanodes líderes para solicitar el chunk respectivo que poseen.
1. Los  datanodes  líderes  le  envían  respectivamente  los  chunks solicitados.
1. El cliente, una vez tiene todos los chunks de determinado archivo que estaba buscando, pasa a recomponerlo, y posteriormente a leerlo.
####
**Proceso de escritura:**

1. El cliente se comunica con el namenode leader para solicitarle la escritura en un determinado archivo (previamente este debe tener su respectivo permiso de escritura). 
1. El namenode leader le entrega al cliente la ubicación de los datanodes líderes que poseen los chunks del archivo y el índice de los chunks del archivo.
1. El cliente se comunica con cada uno de los datanodes líderes para escribir en el archivo, según el chunk que posee. 
1. Una vez el cliente haya escrito en el chunk, el datanode leader se comunica con el datanode follower del chunk para sincronizar los cambios realizados por el cliente.
1. Ese datanode follower a su vez se comunica con el siguiente datanode follower del mismo chunk para propagar el cambio hecho por el cliente. Así hasta que llegue al último datanode follower que posee una réplica de ese chunk.
1. El último datanode follower con dicha réplica, una vez haya aplicado correctamente los cambios, se encarga de enviarle un mensaje de ACK al datanode follower que le compartió los cambios. 
1. Así, de abajo hacia arriba el mensaje de ACK se va transmitiendo hasta que llega al datanode leader, el cual nuevamente comparte el ACK pero esta vez al cliente.
1. Con dicho ACK final el cliente confirma la replicación correcta del cambio  o escritura  realiza  en el  chunk. Esto  se  repite para  cada escritura sobre un chunk específico.
####
**Proceso de inserción.** 
1. El cliente se comunica con el namenode leader para solicitarle la inserción o creación de un determinado archivo (previamente este debe tener su respectivo permiso de escritura). 
1. El namenode leader le entrega al cliente la ubicación de los datanodes disponibles para inserción que serán líderes de los chunks respectivos del archivo.
1. El cliente se comunica con cada uno de los datanodes líderes para crear en ellos el chunk que le corresponde. 
1. Una vez el cliente haya insertado en el chunk, el datanode leader se comunica con otro datanode  que pasará a ser follower, al pasarle una réplica del chunk respectivo.
1. Ese datanode follower a su vez se comunica con el siguiente datanode que también será follower del mismo chunk para propagar las réplicas del  chunk  almacenado. Así  hasta  que  llegue  al  último  datanode follower que poseerá una réplica de ese chunk.
6. El último datanode follower con dicha réplica, una vez haya creado correctamente el chunk, se encarga de enviarle un mensaje de ACK al datanode follower que le compartió la réplica.
6. Así, de abajo hacia arriba el mensaje de ACK se va transmitiendo hasta que llega al datanode leader, el cual nuevamente comparte el ACK pero esta vez al cliente.
6. Con dicho ACK final el cliente confirma la replicación correcta del chunk insertado del archivo. Esto se repite para cada inserción de cada chunk específico.
6. Una  vez  se  hayan  insertado  todos  los  chunks  del  archivo  en  lo datanodes líderes, y sus réplicas en los datanodes followers, cada datanode sea leader o follower se comunica con el namenode leader pasándole el índice del chunk que posee, y el archivo al cual pertenece dicho chunk. De tal forma, el namenode leader actualiza su tabla de metadatos con los nuevos chunks ingresados.
6. Una  vez  hechas  las actualizaciones en  la  tabla de  metadatos,  el namenode leader le envía a cada datanode que le envío dicha info un mensaje OK de confirmación.



## grpc-file-transfer

SSL secured file transfer gRPC client and server written in Python language.
Original Repo: https://github.com/r-sitko/grpc-file-transfer/blob/master/server/main.py


### Prerequisitos

* Python3
* pip3

# Instrucciones para ejecutar el proyecto

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
	
- **open**:  abrir un archivo *test_file.txt* existente dentro del sistema. Los archivos descargados quedan almacenados en el directorio *client/resources/downloaded_files*:
    ```bash
    python -m client.main open -out client/resources/downloaded_files -f file.txt        
    ```
        
- **create**: crear un archivo nuevo *test_file.txt*:
    ```bash
    python -m client.main create -out client/resources/partitioned_files -in client/resources/complete_files -f file.txt   
    ```
        
- **append**: agregar datos a un archivo existente *test_file.txt* (por default en un directorio constante)
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
  


      

