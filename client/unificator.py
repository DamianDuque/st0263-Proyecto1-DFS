import os

def unificator(split_dir):
    """
    Une los archivos divididos, previamente almacenados en un directorio, en un solo archivo.

    :param split_dir: El directorio donde se almacenan los archivos divididos.
    """
    if not os.path.exists(split_dir):
        print("No se encontro el archivo dividido")
        return 0
    
    filenamecomps = split_dir.split("_")[0].split(".")
    finalFilename = filenamecomps[0]+"-reconstructed."+filenamecomps[1]
    print(finalFilename)


    parts = sorted(os.listdir(split_dir))
    with open(finalFilename, 'wb') as archivo_destino:
        for parte in parts:
            path_parte = os.path.join(split_dir, parte)
            with open(path_parte, 'rb') as archivo_parte:
                archivo_destino.write(archivo_parte.read())
            print(f"Se agregó la parte {parte} al archivo {finalFilename}")

if __name__ == "__main__":
    split_dir = "Magic.mp4_dir"
    unificator(split_dir)