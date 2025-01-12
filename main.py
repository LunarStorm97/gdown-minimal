import os
import requests
import sys

def convertir_a_link_directo(link):
    # Verifica si el enlace es de Google Drive
    if "drive.google.com" not in link:
        return None, "El enlace proporcionado no es válido para Google Drive."

    try:
        # Extrae el ID del archivo
        if "id=" in link:
            file_id = link.split("id=")[1].split("&")[0]
        else:
            file_id = link.split("/d/")[1].split("/")[0]

        # Enlace directo de descarga
        link_directo = f"https://drive.google.com/uc?export=download&id={file_id}"
        return link_directo, None

    except IndexError:
        return None, "El enlace proporcionado no tiene un formato válido."

def obtener_nombre_archivo(link_directo):
    try:
        # Hace una solicitud a la cabecera del archivo para obtener el nombre
        respuesta = requests.head(link_directo, allow_redirects=True)
        contenido_disposicion = respuesta.headers.get("content-disposition")
        if contenido_disposicion:
            nombre = contenido_disposicion.split("filename=")[-1].strip('"')
            return nombre
        else:
            return "archivo_descargado"
    except Exception as e:
        return f"Error al obtener el nombre del archivo: {e}"

def descargar_archivo(link_directo, nombre_archivo):
    os.system(f"wget -O '{nombre_archivo}' '{link_directo}'")

# Entrada desde la línea de comandos
link_google_drive = sys.argv[1]
link_directo, error = convertir_a_link_directo(link_google_drive)

if error:
    print(error)
else:
    nombre_archivo = obtener_nombre_archivo(link_directo)
    print(f"Descargando archivo como: {nombre_archivo}")
    descargar_archivo(link_directo, nombre_archivo)
    print("Descarga completada.")
