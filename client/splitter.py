import os
import logging

def append_file_contents(file1, file2):
    with open(file1, 'ab') as f1:
        with open(file2, 'rb') as f2:
            f1.write(f2.read())
            return


def delete_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    
    # Iterate through each file and delete it
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

def hadoop_style_split(filename, in_path, out_path, chunk_size, second_filename=None, second_in_path=None):
    """
    Divide un archivo grande en chunks más pequeños, almacenándolos
    en un directorio con el nombre del archivo original.

    :param filename: El nombre del archivo a dividir.
    :param chunk_size: El tamaño de cada chunk en bytes.
    """

    
    
    # Crea el directorio si no existe
    

    logger = logging.getLogger(__name__)    
    directorio_origen = f"{in_path}/{filename}"
    chunk_num = 1

    if second_filename and second_in_path:
        chunk_num = int(filename[-5])
        directorio_destino = f"{out_path}/{second_filename}"
        if not os.path.exists(directorio_destino):
            os.makedirs(directorio_destino)
        delete_files_in_folder(directorio_destino)
        directorio_origen = f"{in_path}/{filename}"
        directorio_origen2 = f"{second_in_path}/{second_filename}"
        append_file_contents(directorio_origen, directorio_origen2)
        
        with open(directorio_origen, 'rb') as full_file:

            
            chunk = full_file.read(chunk_size)
            
            while chunk:
                nombre_parte = f"{directorio_destino}/part{chunk_num:04d}"
                with open(nombre_parte+".txt", 'wb') as archivo_parte:
                    archivo_parte.write(chunk)
                    #if chunk_num == 1:
                        #print(chunk)
                #print(f"Se creó el chunk {nombre_parte}")
                
                chunk_num += 1
                chunk = full_file.read(chunk_size)


    else:
        directorio_destino = f"{out_path}/{filename}"
        with open(directorio_origen, 'rb') as archivo:
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)
            delete_files_in_folder(directorio_destino)
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
    chunk_size = 1024 * 1024 * 128# Para bloques de 1MB
    hadoop_style_split(filename, chunk_size)