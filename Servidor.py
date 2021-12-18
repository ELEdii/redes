import os
import sys
import shutil
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

HOME = os.getcwd() + "/Index"

with SimpleXMLRPCServer(('192.168.0.5', 8000),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def CrearArchivo(nombre, r):
        ruta = HOME + r
        print("Crear archivo: " + r + nombre)
        try:
            with open(ruta + nombre + ".txt", "x") as archivo:
                return("\t" + "El archivo " + nombre + " se ha creado")
        except:
            return("\t" + "Error al crear el archivo" + nombre )

    def ObtenerContenido(r):
        try:
            ruta = HOME + r
            return os.listdir(ruta)
        except:
            return os.listdir(HOME)
    
    def RenombrarArchivo(r, nombreArchivo, nuevoNombre):
        nombreArchivo = HOME + nombreArchivo        
        return CopiarArchivo(nombreArchivo, HOME + r + "/" + nuevoNombre + ".txt", "renombrado")

    def ModificarArchivo(r, nuevoContenido):
        nombreArchivo = HOME + r
        try:
            with open(nombreArchivo, "w") as archivo:
                archivo.write(nuevoContenido)
                response = "El archivo se ha modificado correctamente" 
        except:
            response = "Error al modificar el archivo"
        return response

    def BorrarArchivo(r):
        nombreArchivo = HOME + r
        os.remove(nombreArchivo)
        return "El archivo se ha eliminado"

    def CrearDirectorio(r, nombre):     
        ruta = HOME + r
        if( not os.path.exists(ruta + nombre + "/") ):
            os.mkdir(ruta + nombre + "/")
            return( "\t" + "El directorio " + nombre + " se ha creado")
        else:
            return( "\t" + "Error al crear el directorio " + nombre)

    def BorrarDirectorio(r, borrar = False):
        if(borrar):
            ruta = HOME + r
        else:
            ruta = r
        print(ruta)
        contenidos = os.listdir(ruta)
        
        for contenido in contenidos:
            if("." in contenido):
                os.remove(ruta + "/" + contenido)
            else:            
                BorrarDirectorio(ruta + "/" + contenido)
        os.rmdir(ruta)
        return "Directorio eliminado"

    def RenombrarDirectorio(nuevoDirectorio, r, borrar = False):
        if(borrar):
            nuevo = HOME + nuevoDirectorio
        else:
            nuevo = nuevoDirectorio
        contenidos = os.listdir(HOME + r)

        for contenido in contenidos:
            if("." in contenido):
                print( CopiarArchivo(HOME + r + "/" + contenido, nuevo + "/" + contenido, "renombrado") )
            else:
                CrearDirectorio( nuevo.replace(HOME,"") + "/",contenido)
                RenombrarDirectorio(nuevo + "/" + contenido, r + "/" + contenido)
        os.rmdir(HOME + r)
        return "Directorio renombrado"

    def CopiarArchivo(original, copia, accion = ""):
        contenido = ""
        try:
            with open(original, "r") as archivo1:
                contenido = archivo1.read()

            with open(copia, "w") as archivo2:
                archivo2.write(contenido)
            os.remove(original)
            response = "El archivo " + copia + " se ha " + accion
        except:
            response = "Error al " + accion + " el archivo " + original
        return response

    def ListarDirectorio(r):
        ruta = HOME + r
        print( "Archivos en el directorio " + ( ruta.replace(HOME, "") ) )
        return( "\t" + str(os.listdir(ruta)) )

    def AbrirArchivo(ruta):
        nombreArchivo = HOME + ruta
        try:
            with open(nombreArchivo, "r") as archivo:
                contenido = archivo.read()
                response  = ( "\tContenido: " + "\n\t\t'" + contenido.replace("\n","\n\t")+ "'")
        except:
            response = "\tError al abrir el archivo: " + nombreArchivo
        return response

    def RegresarDirectorio(ruta):
        print("Regresar")    
        if( ruta.replace(HOME,"") != "/"):
            arrayRuta = ruta.replace(HOME,"").split("/")
            rActual = ""
            for i in range(0, len(arrayRuta) - 2):
                rActual = rActual + arrayRuta[i] + "/"
            return rActual
        return "/"

    def SeleccionarArchivo(archivos, accion, esDirectorio = False):
        while(True):
            i = 0
            files = []
            directorios = []
            
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
                    return files[numArchivo - 1]
            print("\t Selecciona una opción valida")
    
    server.register_function(ObtenerContenido, 'ObtenerContenido')
    server.register_function(CrearArchivo, 'CrearArchivo')
    server.register_function(RenombrarArchivo, 'RenombrarArchivo')
    server.register_function(ModificarArchivo, 'ModificarArchivo')
    server.register_function(BorrarArchivo, 'BorrarArchivo')
    server.register_function(CrearDirectorio, 'CrearDirectorio')
    server.register_function(BorrarDirectorio, 'BorrarDirectorio')
    server.register_function(RenombrarDirectorio, 'RenombrarDirectorio')
    server.register_function(CopiarArchivo, 'CopiarArchivo')
    server.register_function(ListarDirectorio, 'ListarDirectorio')
    server.register_function(AbrirArchivo, 'AbrirArchivo')
    server.register_function(RegresarDirectorio, 'RegresarDirectorio')
    server.register_function(SeleccionarArchivo, 'SeleccionarArchivo')

    server.serve_forever()
