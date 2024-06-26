import re
simbolos = {
    "[": "L_CORCHETE",
    "]": "R_CORCHETE",
    "{": "L_LLAVE",
    "}": "R_LLAVE",
    ",": "COMA",
    ":": "DOS_PUNTOS",
    "string": "LITERAL_CADENA", 
    "number": "LITERAL_NUM",
    "true": "PR_TRUE",
    "false": "PR_FALSE",
    "null": "PR_NULL",
    "eof": "EOF",
    }
exp_reg = {
    "[": "[",
    "]": "]",
    "{": "{",
    "}": "}",
    ",": ",",
    ":": ":",
    "string": '".*"', 
    "number": "[0-9]+(\.[0-9]+)?((e|E)(\+|-)?[0-9]+)?",
    "true": "true|TRUE",
    "false": "false|FALSE",
    "null": "null|NULL"
}

def encuentra_coincidencia(cadena,expresion_regular):
    patron = re.compile(expresion_regular)
    # Buscar la expresión regular en la cadena
    if patron.fullmatch(cadena):
        return True
    else:
        return False