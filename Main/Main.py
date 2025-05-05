import os
import shutil
from asyncio import log
from sys import deactivate_stack_trampoline
from tkinter import Tk, filedialog
from datetime import datetime
import getpass
# Crear carpetas en destino si no existen
import os.path

#ruta = "C/Users/franc/Desktop/inventado"

# tipos=["Imágenes", "PDFs", "Vídeos", "Documentos_Word", "Documentos_txt"]

usuario = getpass.getuser()

ventana = Tk()
ventana.withdraw()

ruta=filedialog.askdirectory(title="Seleccione la carpeta a ordenar")

extensiones= {
    ".jpg":"Imágenes",
    ".png":"Imágenes",
    ".pdf":"PDFs",
    ".mp4":"Vídeos",
    ".docx":"Documentos_Word",
    ".txt":"Documentos_txt",
}

for carpeta in set(extensiones.values()):
    ruta_carpeta=os.path.join(ruta,carpeta)

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

for archivo in os.listdir(ruta):
    ruta_archivo = ruta_carpeta=os.path.join(ruta,archivo)

    if os.path.isfile(ruta_archivo):
        nombre, ext = os.path.splitext(archivo)
        ext=ext.lower()

        if ext in extensiones:
            # destino = os.path.join(ruta,extensiones[ext], archivo)

            # Obtener la fecha de última modificación
            fecha_mod=datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
            subcarpeta_fecha=fecha_mod.strftime("%Y-%m") # Formatea estilo "2025-04"

            # Crear subcarpeta si no existe
            carpeta_tipo= os.path.join(ruta, extensiones[ext])
            carpeta_fecha=os.path.join(carpeta_tipo, subcarpeta_fecha)

            if not os.path.exists(carpeta_fecha):
                os.makedirs(carpeta_fecha)

            # Ruta destino final

            destino = os.path.join(carpeta_fecha, archivo)

            shutil.move(ruta_archivo, destino)

            with open(os.path.join(ruta, "log_movimientos.txt"), "a", encoding="utf-8"):
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario: {usuario} - Movido: {archivo} -> {destino}\n")
