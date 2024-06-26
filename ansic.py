from tablaSimbolos import simbolos
EOF = None


class AnalizadorSintactico:
    def __init__(self, lexemas):
        self.lexemas = lexemas
        self.posicion_actual = -1
        self.token_actual = None
        self.errores = []
        self.get_token()

    def get_token(self):
        if self.posicion_actual < len(self.lexemas)-1:
            self.posicion_actual += 1
            self.token_actual = self.lexemas[self.posicion_actual][1]  # Guarda solo el componente léxico
        else:
            self.token_actual = EOF

    def analizar_archivo(self):
        conjunto_sgte = [EOF]
        self.json(conjunto_sgte)
        return self.errores, len(self.errores) == 0

    def json(self, synchset):
        conjunto_prim = [simbolos["{"], simbolos["["]]  # ["L_LLAVE", "L_CORCHETE"]
        if not self.token_actual in synchset:
            if self.token_actual in conjunto_prim:
                self.element()
            else:
                self.error()
            
    def element(self):
        conjunto_prim = [simbolos["{"], simbolos["["]]
        conjunto_sgte = [simbolos[","], simbolos["]"], simbolos["}"], EOF]
        self.check_input(conjunto_prim, conjunto_sgte)
        if(self.token_actual == simbolos["{"]):
            self.object()
        elif(self.token_actual == simbolos["["]):
            self.array()
        else:
            self.error()
        self.check_input(conjunto_sgte, conjunto_prim)
        
    def object(self):
        conjunto_prim = [simbolos["{"]]
        conjunto_sgte = [simbolos[","], simbolos["]"], simbolos["}"], EOF]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos["{"]:
                self.match(simbolos["{"])
                if self.token_actual == simbolos["}"]:
                    self.match(simbolos["}"])
                elif self.token_actual == simbolos["string"]:
                    self.attribute_list()
                    self.match(simbolos["}"])
                else:
                    self.error()
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    def array(self):
        conjunto_prim = [simbolos["["]]
        conjunto_sgte = [simbolos[","], simbolos["]"], simbolos["}"], EOF]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos["["]:
                self.match(simbolos["["])
                if self.token_actual == simbolos["]"]:
                    self.match(simbolos["]"])
                elif self.token_actual in [simbolos["{"], simbolos["["]]:
                    self.element_list()
                    self.match(simbolos["]"])
                else:
                    self.error()
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    def element_list(self):
        conjunto_prim = [simbolos["{"], simbolos["["]]
        conjunto_sgte = [simbolos["]"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual in conjunto_prim:
                self.element()
                self.element_list_aux()
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    def element_list_aux(self):
        '''Nuevo NT de la gramática corregida.'''
        conjunto_prim = [simbolos[","]]
        conjunto_sgte = [simbolos["]"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos[","]:
                self.match(simbolos[","])
                self.element()
                self.element_list_aux()
            self.check_input(conjunto_sgte, conjunto_prim)

    def attribute_list(self):
        conjunto_prim = [simbolos["string"]]
        conjunto_sgte = [simbolos["}"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos["string"]:
                self.attribute()
                self.attribute_list_aux()
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    def attribute_list_aux(self):
        conjunto_prim = [simbolos[","]]
        conjunto_sgte = [simbolos["}"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos[","]:
                self.match(simbolos[","])
                self.attribute()
                self.attribute_list_aux()
            self.check_input(conjunto_sgte, conjunto_prim)

    def attribute(self):
        conjunto_prim = [simbolos["string"]]
        conjunto_sgte = [simbolos[","], simbolos["}"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos["string"]:
                self.attribute_name()
                self.match(simbolos[":"])
                self.attribute_value()
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    def attribute_name(self):
        conjunto_prim = [simbolos["string"]]
        conjunto_sgte = [simbolos[":"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual == simbolos["string"]:
                self.match(simbolos["string"])
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    def attribute_value(self):
        conjunto_prim = [simbolos["{"], simbolos["["], simbolos["string"], simbolos["number"], 
                         simbolos["true"], simbolos["false"], simbolos["null"]]
        conjunto_sgte = [simbolos[","], simbolos["}"]]
        if not self.token_actual in conjunto_sgte:
            self.check_input(conjunto_prim, conjunto_sgte)
            if self.token_actual in conjunto_prim:
                if self.token_actual == simbolos["{"] or self.token_actual == simbolos["["]:
                    self.element()
                elif self.token_actual == simbolos["string"]:
                    self.match(simbolos["string"])
                elif self.token_actual == simbolos["number"]:
                    self.match(simbolos["number"])
                elif self.token_actual == simbolos["true"]:
                    self.match(simbolos["true"])
                elif self.token_actual == simbolos["false"]:
                    self.match(simbolos["false"])
                elif self.token_actual == simbolos["null"]:
                    self.match(simbolos["null"])
            else:
                self.error()
            self.check_input(conjunto_sgte, conjunto_prim)

    # Funciones para Panic Mode
    def error(self):
        self.errores.append(f"Error sintáctico en token {self.token_actual} en línea {self.lexemas[self.posicion_actual][0]}")

    def check_input(self, firsts, follows):
        if self.token_actual not in firsts:
            self.error()
            self.scanto(firsts + follows)

    def scanto(self, synchset):
        while self.token_actual not in (synchset):
            self.get_token()

    def match(self, expected_token):
        if self.token_actual == expected_token:
                self.get_token()
        else:
            self.error()