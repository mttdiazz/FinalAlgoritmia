class AutomataNombre:
    def __init__(self):
        print(self)
        self.estado_actual = 'inicial'
        self.estados_aceptacion = {'aceptacion'}
        self.transiciones = {
            'inicial': {'mayuscula': 'intermedio', 'minuscula': 'intermedio'},
            'intermedio': {'minuscula': 'intermedio', 'otro': 'error'},
            'error': {'': 'error'}  # Estado de error, se queda en el mismo estado
        }

    def transicion(self, caracter):
        #print("Transicion: Self - {} Caracter: {}".format(self,caracter))
        if caracter.isupper():
            return 'mayuscula'
        elif caracter.islower():
            return 'minuscula'
        else:
            return 'otro'

    def validar_nombre(self, nombre):
        self.estado_actual = 'inicial'  # Reiniciamos al estado inicial
        for caracter in nombre:
            #print("Validar nombre: Caracter - "+caracter)
            entrada = self.transicion(caracter)
            #print("Validar: Entrada - "+entrada)
            if ((entrada not in self.transiciones[self.estado_actual]) or entrada=='otro'):
                self.estado_actual = 'error'
                break
            self.estado_actual = self.transiciones[self.estado_actual][entrada]
        #print('Validar: Estado Actual - '+self.estado_actual)
        if self.estado_actual in self.transiciones and not entrada == 'otro':
            self.estado_actual = self.estados_aceptacion
            return True
        else:
            return False


#if __name__ == "__main__":
    #automata = AutomataNombre()
     #nombre = input("Ingrese un nombre: ")
    #print('Nombre: '+nombre)
    #if automata.validar_nombre(nombre):
        #print("El nombre es válido.")
    #else:
        #print("El nombre no es válido.") """
