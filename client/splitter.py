import os
import logging

def hadoop_style_split(filename, in_path, out_path, chunk_size):
    """
    Divide un archivo grande en chunks más pequeños, almacenándolos
    en un directorio con el nombre del archivo original.

    :param filename: El nombre del archivo a dividir.
    :param chunk_size: El tamaño de cada chunk en bytes.
    """

    
    
    # Crea el directorio si no existe
    

    logger = logging.getLogger(__name__)    
    directorio_origen = f"{in_path}/{filename}"
    directorio_destino = f"{out_path}/{filename}"
    chunk_num = 1
    with open(directorio_origen, 'rb') as archivo:
        if not os.path.exists(directorio_destino):
            os.makedirs(directorio_destino)
        chunk = archivo.read(chunk_size)
        
        while chunk:
            nombre_parte = f"{directorio_destino}/part{chunk_num:04d}"
            with open(nombre_parte+".txt", 'wb') as archivo_parte:
                archivo_parte.write(chunk)
                #if chunk_num == 1:
                    #print(chunk)
            #print(f"Se creó el chunk {nombre_parte}")
            
            chunk_num += 1
            chunk = archivo.read(chunk_size)


if __name__ == "__main__":
    filename = "Infografia.pdf"  # Nombre del archivo
    chunk_size = 1024 * 1024  # Para bloques de 1MB
    hadoop_style_split(filename, chunk_size)