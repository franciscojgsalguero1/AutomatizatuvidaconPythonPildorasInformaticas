import os
import shutil
import time
from asyncio import log
#from asyncio import log
#from sys import deactivate_stack_trampoline
from tkinter import Tk, filedialog
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
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

def esperar_archivo_libre(ruta_archivo, intentos=10, espera=0.5):

    for _ in range(intentos):
        try:
            with open(ruta_archivo, "rb"):
                return True
        except (PermissionError, OSError):
            time.sleep(espera)

    return False

def ordenar_archivos(ruta):
    for archivo in os.listdir(ruta):
        ruta_archivo = ruta_carpeta=os.path.join(ruta,archivo)

        if os.path.isfile(ruta_archivo) and archivo != "log_movimientos.txt":

            if not esperar_archivo_libre(ruta_archivo):
                print(f" No se pudo acceder a {archivo} porque está siendo utilizado")
                continue
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

    # Arreglar esta línea de código , falla al leer
                #with open(os.path.join(ruta, "log_movimientos.txt"), "a", encoding="utf-8"):
                    #log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario: {usuario} - Movido: {archivo} -> {destino}\n")

class ManejadorEventos(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            print(f"Nuevo archivo detectado: {event.src_path}")
            ordenar_archivos(ruta)

for carpeta in set(extensiones.values()):
    ruta_carpeta=os.path.join(ruta,carpeta)

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

ordenar_archivos(ruta)

manejador_eventos=ManejadorEventos()
observador=Observer()
observador.schedule(manejador_eventos, ruta, recursive=False)
observador.start()

print(f"Vigilando la carpeta: {ruta}")
print("Presiona Ctrl+C para detener el programa")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Deteniendo vigilancia")
    observador.stop()

observador.join()