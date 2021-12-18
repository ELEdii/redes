import os
import xmlrpc.client
import datetime

gestorArchivos = xmlrpc.client.ServerProxy('http://192.168.0.5:8000')

def SeleccionarArchivo(ruta, accion, esDirectorio = False):
    archivos = gestorArchivos.ObtenerContenido(ruta)
    
    while(True):
        i = 0
        files = []
        directorios = []
        print("Archivos disponibles: ")
        for archivo in archivos:
            if( "." in archivo ):
                files.append(archivo)
            else:
                directorios.append(archivo)

            if(not esDirectorio and "." in archivo):
                print( "\t" + str( len(files) ) + ". " + archivo)
            elif(esDirectorio and "." not in archivo):
                print( "\t" + str( len(directorios) ) + ". " + archivo)

        if( (len(files) == 0 and not esDirectorio) or (len(directorios) == 0 and esDirectorio) ):
            input ("\t No hay archivos en este directorio. Pulsa enter para continuar ...")
            return ""

        if(esDirectorio):
            aux = directorios
        else:
            aux = files

        opcion = input( "\t Ingresa el numero del archivo que deseas " + accion + ": ")
        if( opcion.isdigit() ):
            numArchivo = int(opcion)
            if(numArchivo > 0 and numArchivo <= len(aux)):
                if(esDirectorio):
                    return directorios[numArchivo - 1]
                return ruta + files[numArchivo - 1]

        print("\t Selecciona una opción valida")

ruta = "/"
while(True):
    os.system("cls")
    aArchivos = []
    aDirectorio = []
    for archivo in gestorArchivos.ObtenerContenido(ruta):
        if( "." in archivo ):
            aArchivos.append(archivo)
        else:
            aDirectorio.append(archivo)
    
    print("Te encuentras en la ruta : " + ruta)
    for directorio in aDirectorio:
        print("\t" + directorio)           
    for archivo in aArchivos:
        print("\t" + archivo)

    print("\nOperaciones de archivos:")
    print("\t1. Crear archivo")
    print("\t2. Ver archivo")
    print("\t3. Modificar contenido del archivo")
    print("\t4. Renombrar archivo")
    print("\t5. Borrar archivo")
    print("Operaciones de directorios:")
    print("\t6. Crear directorio")
    print("\t7. Abrir directorio")
    print("\t8. Borrar directorio")
    print("\t9. Renombrar directorio")
    print("\t10. Directorio anterior")
    print("11. Salir")
    
    opcion = input(" Ingresa una opción: ")

    if( opcion == "1"):
        nombre = input( "Ingresa el nombre del archivo de texto: ")
        input( gestorArchivos.CrearArchivo(nombre.replace(" ", ""), ruta) )

    elif( opcion == "2"):
        archivo = SeleccionarArchivo(ruta, "ver")
        if( archivo != ""):                    
            print( gestorArchivos.AbrirArchivo(archivo) )
            input("\tPulsa enter para continuar ... ")

    elif( opcion == "3"):
        archivo = SeleccionarArchivo(ruta, "modificar")
        if( archivo != ""):
            nuevoContenido = input("\t Ingresa el nuevo nombre para el archivo " + archivo + ": ")
            print( gestorArchivos.ModificarArchivo(archivo, nuevoContenido) )

    elif( opcion == "4"):
        archivo = SeleccionarArchivo(ruta, "renombrar")
        if( archivo != ""):
            nombre = input("\t Ingresa el nuevo nombre para el archivo " + archivo + ": ")            
            print(gestorArchivos.RenombrarArchivo(ruta, archivo, nombre))

    elif( opcion == "5"):
        archivo = SeleccionarArchivo(ruta, "eliminar")
        if( archivo != ""):      
            opcion = input("\t Eliminar archivo? Y/n: ")
            if( opcion.lower() == "y"):
                gestorArchivos.BorrarArchivo(archivo)

    elif( opcion == "6"):
        nombre = input( "\tIngresa el nombre del directorio: ")
        input( gestorArchivos.CrearDirectorio(ruta, nombre) )

    elif( opcion == "7"):
        directorio = SeleccionarArchivo(ruta, "abrir", True)
        if(directorio != ""):
            ruta = ruta + directorio + "/"

    elif( opcion == "8"):
        directorio = SeleccionarArchivo(ruta, "eliminar", True)

        if(directorio != ""):
            opcion = input("\t Eliminar directorio? Y/n: ")
            if( opcion.lower() == "y"):
                gestorArchivos.BorrarDirectorio(ruta+directorio, True)

    elif( opcion == "9"):
        directorio = SeleccionarArchivo(ruta, "renombrar", True)
        nuevoDirectorio = input( "\tIngresa el nuevo nombre para " + directorio + " : ")
        gestorArchivos.CrearDirectorio(ruta, nuevoDirectorio)
        gestorArchivos.RenombrarDirectorio(ruta + nuevoDirectorio, ruta + directorio, True)

    elif( opcion == "10"):
        ruta = gestorArchivos.RegresarDirectorio(ruta)

    elif( opcion == "11"):
        break
    else:
        print("Ingresa una opción valida")
        input("Pulsa enter para continuar")
print("Saliendo ... ")