import os
import shutil
import threading
import time
import threading
from asyncio import log
from tkinter import Tk, filedialog, Button, Label, dialog
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
import getpass
# Crear carpetas en destino si no existen
import os.path

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

class ManejadorEventos(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            print(f"Nuevo archivo detectado: {event.src_path}")
            ordenar_archivos(ruta)

for carpeta in set(extensiones.values()):
    ruta_carpeta=os.path.join(ruta,carpeta)

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

def iniciar_vigilancia():
    observador.start()

def detener_vigilancia():
    observador.stop()
    observador.join()
    ventana.quit()

if ruta != '':
    ordenar_archivos(ruta)

    manejador_eventos=ManejadorEventos()
    observador=Observer()
    observador.schedule(manejador_eventos, ruta, recursive=False)

    ventana.deiconify()
    ventana.title("Vigilancia de carpeta")
    ventana.geometry("400x150")

    Label(ventana, text=f"Vigilando la carpeta: \n {ruta}", wraplength=350).pack(pady=10)
    Button(ventana, text="Detener vigilancia y salir", command=detener_vigilancia).pack(pady=10)

    hilo_vigilancia=threading.Thread(target=iniciar_vigilancia, daemon=True)
    hilo_vigilancia.start()
    ventana.mainloop()

