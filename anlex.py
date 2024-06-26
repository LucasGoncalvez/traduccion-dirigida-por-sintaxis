import tablaSimbolos

def analizar_archivo(ruta_archivo):
    num_linea = 0
    resultado = []
    valido = True
    MSG_ERROR = "<Lexema invalido>"
    with open(ruta_archivo, 'r') as archivo:
        c = archivo.read(1)  # lee un solo caracter del archivo
        num_linea = 1
        while c != '':  # mientras haya caracteres para leer
            lexema = ""
            if c == " " or c == "\t":
                pass
            elif c == "\n":
                num_linea += 1
                pass
            elif c.isdigit(): # si es un número
                while True:
                    lexema = lexema + c
                    c = archivo.read(1)
                    if not c.isdigit() and c != "." and c != "e": 
                        break
                if c != '':
                    if tablaSimbolos.encuentra_coincidencia(lexema,tablaSimbolos.exp_reg["number"]):
                        resultado.append([num_linea, tablaSimbolos.simbolos["number"]])
                    else:
                        valido = False
                        resultado.append([num_linea, MSG_ERROR])
                    continue 
                else:
                    break

            elif c == '"': # clave o cadena
                while True:
                    lexema = lexema + c
                    c = archivo.read(1)
                    if c == '"' or c == '': 
                        lexema = lexema + c
                        break
                    elif c == "\n":
                        break
                if c != '':
                    if tablaSimbolos.encuentra_coincidencia(lexema,tablaSimbolos.exp_reg["string"]):
                        resultado.append([num_linea, tablaSimbolos.simbolos["string"]])
                    else:
                        valido = False
                        resultado.append([num_linea, MSG_ERROR]) 
                    pass
                else:
                    break
            elif c == "t" or c == "T": # true True
                lexema = lexema + c
                c = archivo.read(3)
                lexema = lexema + c
                if tablaSimbolos.encuentra_coincidencia(lexema, tablaSimbolos.exp_reg["true"]):
                    resultado.append([num_linea, tablaSimbolos.simbolos["true"]])
                else:
                    valido = False
                    resultado.append([num_linea, MSG_ERROR])       
                if c == '':
                    break
                pass
            elif c == "f" or c == "F": # false FALSE
                lexema = lexema + c
                c = archivo.read(4)
                lexema = lexema + c
                if tablaSimbolos.encuentra_coincidencia(lexema, tablaSimbolos.exp_reg["false"]):
                    resultado.append([num_linea, tablaSimbolos.simbolos["false"]])
                else:
                    valido = False
                    resultado.append([num_linea, MSG_ERROR])
                if c == '':
                    break       
                pass
            elif c == "n" or c == "N": # null NULL
                lexema = lexema + c
                c = archivo.read(3)
                lexema = lexema + c
                if tablaSimbolos.encuentra_coincidencia(lexema, tablaSimbolos.exp_reg["null"]):
                    resultado.append([num_linea, tablaSimbolos.simbolos["null"]])
                else:
                    valido = False
                    resultado.append([num_linea, MSG_ERROR])
                if c == '':
                    break      
                pass
            elif c == "{":
                resultado.append([num_linea, tablaSimbolos.simbolos["{"]])
                pass
            elif c == "[":
                resultado.append([num_linea, tablaSimbolos.simbolos["["]])
                pass
            elif c == "}":
                resultado.append([num_linea, tablaSimbolos.simbolos["}"]])
                pass
            elif c == "]":
                resultado.append([num_linea, tablaSimbolos.simbolos["]"]])
                pass
            elif c == ",":
                resultado.append([num_linea, tablaSimbolos.simbolos[","]])
                pass
            elif c == ":":
                resultado.append([num_linea, tablaSimbolos.simbolos[":"]])
                pass
            c = archivo.read(1)  # Lee el siguiente caracter del archivo
        if c == '':
            print("Analizacion finalizada")
    
    return resultado, valido

def guardar_resultado(resultado, ruta_salida):
    lineas = {}
    for numero_linea, contenido in resultado:
        if numero_linea in lineas:
            lineas[numero_linea].append(contenido)
        else:
            lineas[numero_linea] = [contenido]
    # Imprimir el contenido de cada línea en orden
    with open(ruta_salida, 'w') as salida:
        for linea in sorted(lineas):
            salida.write(' '.join(lineas[linea]) + "\n")
