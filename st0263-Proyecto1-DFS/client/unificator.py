import os
import logging

def unificator(split_dir, filename):
    """
    Une los archivos divididos, previamente almacenados en un directorio, en un solo archivo.

    :param split_dir: El directorio donde se almacenan los archivos divididos.
    """

    logger = logging.getLogger(__name__)  
    directorio_destino = f"{split_dir}/{filename}"


    if not os.path.exists(directorio_destino):
        print("No se encontro el archivo dividido")
        return 0
    
    filenamecomps = directorio_destino.split(".", 1)
    finalFilename = filenamecomps[0]+"-reconstructed."+filenamecomps[1]
    


    parts = sorted(os.listdir(directorio_destino))
    with open(finalFilename, 'wb') as archivo_destino:
        for parte in parts:
            path_parte = os.path.join(directorio_destino, parte)
            with open(path_parte, 'rb') as archivo_parte:
                archivo_destino.write(archivo_parte.read())
        return finalFilename

if __name__ == "__main__":
    split_dir = "Magic.mp4_dir"
    unificator(split_dir)