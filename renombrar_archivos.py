import os
# si utilizas mac o linux
#import stat

carpeta="C:/Users/franc/Desktop/AutomatizatuvidaconPython"
prefijo="imagen_"
extensiones= (".jpg", ".png")

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
print(f"Renombrado completo. Ejecuta el .bat que hay en la carpeta para revertir cambios en '{ruta_deshacer}'")
