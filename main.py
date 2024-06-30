import anlex
from ansic import AnalizadorSintactico
from traductor_a_xml import TraductorJsonAXml
import sys

def main():
    ruta_archivo = 'fuente.txt'
    ruta_salida = 'output.txt'
    ruta_xml_salida = 'xml_traducido.xml'
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
            sys.exit()
               # Traducción dirigida por sintaxis
        with open(ruta_xml_salida, 'w', encoding='utf-8') as output_file:
            traductor = TraductorJsonAXml(resultado, output_file)
            traductor.traducir()
        
        print(f"Traducción completada. El archivo '{ruta_xml_salida}' ha sido generado.")
    
    except IOError as e:
        print(f"Error al abrir el archivo: {e}")
    except Exception as e:
        print(f"Se produjo un error: {str(e)}")
        print(f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    main()