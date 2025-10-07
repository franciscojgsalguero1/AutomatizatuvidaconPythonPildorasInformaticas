import os
# si utilizas mac o linux
#import stat

import tkinter as tk
from tkinter import filedialog, messagebox

def seleccionar_carpeta():
    ruta=filedialog.askdirectory()
    entrada_carpeta.insert(0, ruta)

def renombrar_archivos():

    carpeta=entrada_carpeta.get()
    prefijo=entrada_prefijo.get()
    extensiones=tuple(entrada_extensiones.get().split(","))

    archivos=[]

    for f in os.listdir(carpeta):
        if f.endswith(extensiones):
            archivos.append(f)

    # Creación del archivo para deshacer renombrado (archivo tipo .bat y .sh)
    ruta_deshacer=os.path.join(carpeta, "deshacer.bat")
    #deshacer.sh
    with open(ruta_deshacer, "w", encoding="utf-8") as deshacer_mem:
        # ruta_deshacer.write("#!/bin/bash\n")
        # ruta_deshacer.write(f'cd "{carpeta}" || exis\n\n')
        for i, nombre_actual in enumerate(archivos, start=1):
            extension_actual=os.path.splitext(nombre_actual)[1]
            nuevo_nombre=f"{prefijo}{i:03}{extension_actual}"
            ruta_actual=os.path.join(carpeta, nombre_actual)
            ruta_nueva=os.path.join(carpeta, nuevo_nombre)
            os.rename(ruta_actual, ruta_nueva)
            # deshacer_mem.write(f'mv "{nuevo_nombre}" "{nombre_actual}"\n')
            deshacer_mem.write(f'rename "{nuevo_nombre}" "{nombre_actual}"\n')
        # para que el archivo .bat desaparezca después de ejecutar el archivo con doble click
        deshacer_mem.write("del \"%~f0\n")
    messagebox.showinfo("Éxito", f"Renombrado completo. Puedes deshacer los cambios en el .bat generado: \n {ruta_deshacer}")

# ------------- INTERFAZ GRÁFICA -------------------

ventana=tk.Tk()
ventana.title("Renombrando archivos")
ventana.geometry("400x260")
ventana.resizable(False, False)

tk.Label(ventana, text="Carpeta de trabajo: ").pack(pady=5)
frame_carpeta=tk.Frame(ventana)
frame_carpeta.pack()
entrada_carpeta=tk.Entry(frame_carpeta, width=40)
entrada_carpeta.pack(side=tk.LEFT, padx=5)
tk.Button(frame_carpeta, text="Examinar", command=seleccionar_carpeta).pack(side=tk.LEFT)

tk.Label(ventana, text="Prefijo de los archivos").pack(pady=5)
entrada_prefijo=tk.Entry(ventana, width=30)
entrada_prefijo.insert(0, "imagen_")
entrada_prefijo.pack()

tk.Label(ventana, text="Extensiones (separadas por comas): ").pack(pady=5)
entrada_extensiones=tk.Entry(ventana, width=30)
entrada_extensiones.insert(0, ".jpg,.png")
entrada_extensiones.pack()

tk.Button(ventana, text="Renombrar_archivos", command=renombrar_archivos, bg="#04ba04", fg="white", padx=10).pack(pady=15)

ventana.mainloop()