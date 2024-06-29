from tablaSimbolos import simbolos
EOF = None


class TraductorJsonAXml:
    def __init__(self, lexemas):
        self.lexemas = lexemas
        self.posicion_actual = -1
        self.token_actual = None # [0] es número de línea en el archivo, [1] es el token, [2] es el valor
        self.traduccion = None
        self.get_token()

    def get_token(self):
        if self.posicion_actual < len(self.lexemas)-1:
            self.posicion_actual += 1
            self.token_actual = self.lexemas[self.posicion_actual]
        else:
            self.token_actual = EOF

    def traducir(self):
        self.json()
        return self.traduccion

    def json(self):
        self.element()

    def element(self):
        if(self.token_actual[1] == simbolos["{"]):
            self.object()
        elif(self.token_actual[1] == simbolos["["]):
            self.array()
        
    def object(self):
        if self.token_actual[1] == simbolos["{"]:
            self.match(simbolos["{"])
            if self.token_actual[1] == simbolos["}"]:
                self.match(simbolos["}"])
            elif self.token_actual[1] == simbolos["string"]:
                self.attribute_list()
                self.match(simbolos["}"])

    def array(self):
        if self.token_actual[1] == simbolos["["]:
            self.match(simbolos["["])
            if self.token_actual[1] == simbolos["]"]:
                self.match(simbolos["]"])
            elif self.token_actual[1] in [simbolos["{"], simbolos["["]]:
                print("\n<item>")
                self.element_list()
                self.match(simbolos["]"])
                print("</item>")

    def element_list(self):
        if self.token_actual[1] in [simbolos["{"], simbolos["["]]:
            self.element()
            self.element_list_aux()

    def element_list_aux(self):
        if self.token_actual[1] == simbolos[","]:
            self.match(simbolos[","])
            print("</item>")
            print("<item>")
            self.element()
            self.element_list_aux()

    def attribute_list(self):
        if self.token_actual[1] == simbolos["string"]:
            self.attribute()
            self.attribute_list_aux()

    def attribute_list_aux(self):
        if self.token_actual[1] == simbolos[","]:
            self.match(simbolos[","])
            self.attribute()
            self.attribute_list_aux()

    def attribute(self):
        if self.token_actual[1] == simbolos["string"]:
            value_name = self.token_actual[2].replace('"', '')
            print("<", end='')
            print(value_name, end='') # sin comillas debe ser
            print(">", end='')
            #
            self.attribute_name()
            self.match(simbolos[":"])
            self.attribute_value()
            #
            print("</", end='')
            print(value_name, end='') # sin comillas debe ser
            print(">")

    def attribute_name(self):
        if self.token_actual[1] == simbolos["string"]:
            self.match(simbolos["string"])

    def attribute_value(self):
        if self.token_actual[1] == simbolos["{"] or self.token_actual[1] == simbolos["["]:
            self.element()
        elif self.token_actual[1] == simbolos["string"]:
            print(self.token_actual[2], end='')
            self.match(simbolos["string"])
        elif self.token_actual[1] == simbolos["number"]:
            print(self.token_actual[2], end='')
            self.match(simbolos["number"])
        elif self.token_actual[1] == simbolos["true"]:
            print(self.token_actual[2], end='')
            self.match(simbolos["true"])
        elif self.token_actual[1] == simbolos["false"]:
            print(self.token_actual[2], end='')
            self.match(simbolos["false"])
        elif self.token_actual[1] == simbolos["null"]:
            print(self.token_actual[2], end='')
            self.match(simbolos["null"])

    #
    def match(self, expected_token):
        if self.token_actual[1] == expected_token:
                self.get_token()