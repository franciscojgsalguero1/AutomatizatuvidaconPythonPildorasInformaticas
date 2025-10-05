import os

carpeta="C:/Users/franc/Desktop/AutomatizatuvidaconPython"
prefijo="imagen_"
extensiones= (".jpg", ".png")

archivos=[]

for f in os.listdir(carpeta):
    if f.endswith(extensiones):
        archivos.append(f)

for i, nombre_actual in enumerate(archivos, start=1):
    extension_actual=os.path.splitext(nombre_actual)[1]
    nuevo_nombre=f"{prefijo}{i:03}{extension_actual}"
    ruta_actual=os.path.join(carpeta, nombre_actual)
    ruta_nueva=os.path.join(carpeta, nuevo_nombre)
    os.rename(ruta_actual, ruta_nueva)