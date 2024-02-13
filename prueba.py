from pyswip import Prolog

import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk

def questionario(callback):
    root=tk.Tk()
    root.title("Test Questionario")
    style=ttk.Style()
    style.theme_use('aqua')

    def on_closing():
        root.quit()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def bytes_a_string(bytestring): #pasar de byte-string a strings
    if type(bytestring)==bytes:
        bytestring=bytestring.decode("utf-8")
    return bytestring

#funciones consulta prolog
def consultaX(relacion,x,pl): #los parametros son strings que definen la consulta -> relacion(X,y)
    query=relacion + "(" + x + ",Y)"
    res_query=list(pl.query(query))
    res=[]
    for item in res_query:
        final=bytes_a_string(item["Y"])
        res.append(final)
    return res

def consultaY(relacion,y,pl): 
    query=relacion + "(X," + y +")"
    res_query=list(pl.query(query))
    res=[]
    for item in res_query:
        final=bytes_a_string(item["X"])
        res.append(final)
    return res

def consultaANY(relacion,pl): #por si acaso
    query=relacion + "(X,Y)"
    res=[]
    res_query=list(pl.query(query))
    for item in res_query:
        final=[bytes_a_string(item["X"]),bytes_a_string(item["Y"])]   
        res.append(final)
    return res




def main():
    pl = Prolog()
    pl.consult("juegos.pl")
    print("Juegos de PC: \n")
    print(consultaX("consola","pc",pl))

    print("\n\nGenero del FIFA:\n")
    print(consultaY("genero",'"FIFA"',pl))  #no es lo mismo "" que '', hay que ser consistente con lo que esta en el .pl

    print("\n\nPreguntas:\n")
    print(consultaANY("pregunta",pl))


#main()
    

def mostrar_preguntas(root, preguntas):
    respuestas=[]
    for pregunta in preguntas:
        opciones=consultaX(pregunta,"_",pl)
        

        #mostrar las opciones

        #guardar la seleccion
        respuestas.append()
    return respuestas



root = tk.Tk()
root.title("Cuestionario") 
root.geometry('400x350')   #tamaño de la ventana (anchoXalto)
frm = ttk.Frame(root)   
frm.pack(fill=tk.BOTH, expand=True) 
#frm.grid()
texto1=ttk.Label(frm, text="GamerBot")  #titulo
texto1.pack(pady=10) 
boton=ttk.Button(frm, text="Iniciar cuestionario", command=root.destroy) #boton de inicio
boton.place(x=0, y=0)  #otra alternativa a grid. Necesita una referencia (anchor), por omisión esquina superior izq. Mide en pixels




def listbox(root,opciones):
    respuestas=[]
    list = tk.Listbox(root, selectmode = "multiple") 
    list.pack(expand = "YES", fill = "both") 
    for each_item in range(len(opciones)): 
        list.insert("end", opciones[each_item]) 

    #append las respuestas
    return respuestas

def radiobuttons(root,opciones):  #completar
    respuesta = tk.StringVar()
    for opcion in opciones:
            radio_button = ttk.Radiobutton(root, text=opcion, variable=respuesta, value=opcion)
                
            radio_button.pack(anchor=tk.W, padx=70)

    def enviar_respuesta():
        if respuesta.get() == "":
                messagebox.showerror("Error", "Debes seleccionar una opción.")
        else:
             respuesta=
    boton_enviar = ttk.Button(root, text="Enviar", command=enviar_respuesta)
    return respuesta

#preguntas=consultaX("pregunta","_",pl)


def on_closing():
        if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
            root.quit()
    
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


