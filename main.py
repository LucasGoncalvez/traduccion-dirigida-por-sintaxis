import anlex
from ansic import AnalizadorSintactico
import sys

def main():
    ruta_archivo = 'fuente.txt'
    ruta_salida = 'output.txt'

    try:
        #Analizador Lexico
        resultado, valido = anlex.analizar_archivo(ruta_archivo)
        anlex.guardar_resultado(resultado, ruta_salida)
        if not valido:
            print("Error léxico. Revise el archivo {}".format(ruta_archivo))
            sys.exit()
        # Análisis sintáctico
        ansic = AnalizadorSintactico(resultado)
        errores, valido = ansic.analizar_archivo()
        if not valido:
            for error in errores:
                print(error)
        #
        print("Análisis sintáctico completado.")
    except IOError as e:
        print(f"Error al abrir el archivo: {e}")
    except Exception as e:
        print(f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    main()