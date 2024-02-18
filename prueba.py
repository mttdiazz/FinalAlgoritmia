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

def consultaUnica(relacion,pl):   #relacion(X)
    query=relacion + "(X)"
    res_query=list(pl.query(query))
    res=[]
    for item in res_query:
        final=bytes_a_string(item["X"])
        res.append(final)
    return res

def eliminar_repetidos(lista):
    nueva=[]
    for item in lista:
        if item not in nueva:
            nueva.append(item)
    return nueva


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

def mostrar_resultado(respuestas,pl,categorias):


    #intento 1: interseccion
    res=[]
    consolas=respuestas.pop(0)
    juegos_posibles=[]
    generos=[]
    for c in consolas:
        c=consultaY("console",'"'+c+'"',pl)[0]
        juegos_posibles.extend(consultaX("consola",c,pl))
    juegos_posibles=eliminar_repetidos(juegos_posibles)  #los juegos soportados por las consolas elegidas
    for i in range(len(respuestas)):
        generos.extend(consultaY(categorias[i+1],'"'+respuestas[i]+'"',pl))
    generos=eliminar_repetidos(generos)
    for g in generos:
        aux=consultaX("genero",g,pl)
        print(g + ": ")
        print(aux)
        for juego in aux:
            if juego in juegos_posibles:  #los juegos del genero elegido que estan en las consolas elegidas
                res.append(juego)
    
    print(res)


def mostrar_preguntas(categorias,pl,respuestas,i,cant):  #recursividad indirecta + clausuras -> revisar!!!!
    
    def listbox(opciones,respuestas):
        rsp=[]
        l=ttk.Label(root,text="Selecciona una o varias opciones")
        l.place(x=150,y=70)
        widgets.append(l)
        list = tk.Listbox(root, selectmode = "multiple") 
        list.pack(expand = "YES", fill = "x")  
        widgets.append(list)  
        list.insert(tk.END, *opciones) 

        def send():
            indices = list.curselection()
            if len(indices)==0:
                messagebox.showerror("Error", "Debes seleccionar al menos una opción.")
            else:
                l.destroy()
                for index in indices:
                    rsp.append(list.get(index))
                respuestas.append(rsp)
                for w in widgets:
                    w.destroy()
                mostrar_preguntas(categorias,pl,respuestas,i+1,cant)

        enviar=ttk.Button(frm,text="Enviar",command=send)
        enviar.pack(pady=100)
        widgets.append(enviar)
        
        

    def radiobuttons(opciones,respuestas): 
        respuesta = tk.StringVar()
        for opcion in opciones:
                radio_button = ttk.Radiobutton(root, text=opcion, variable=respuesta, value=opcion)
                radio_button.pack(anchor=tk.W, padx=70)
                widgets.append(radio_button)

        def enviar_respuesta():
            if respuesta.get() == "":
                messagebox.showerror("Error", "Debes seleccionar una opción.")
            else:
                respuestas.append(respuesta.get())
                
                for w in widgets:
                    w.destroy()
                mostrar_preguntas(categorias,pl,respuestas,i+1,cant)

        boton_enviar = ttk.Button(root, text="Enviar", command=enviar_respuesta)
        boton_enviar.pack(anchor=tk.W,padx=80,pady=10)
        widgets.append(boton_enviar)


    if i<cant:
        widgets=[]
        pregunta=consultaX("pregunta",categorias[i],pl)[0]
        l1=ttk.Label(root,text="Pregunta "+str(i+1)+" de "+str(cant))
        l1.place(x=50,y=10)
        l2=ttk.Label(root,text=pregunta)
        l2.place(x=50,y=30)
        widgets.append(l1)
        widgets.append(l2)
        opciones=eliminar_repetidos(consultaX(categorias[i],"_",pl))
        
        if (i==0):   #hagamos que la pregunta de consola sea la 1era
            listbox(opciones,respuestas)
        else:
            radiobuttons(opciones,respuestas)


    else:    #finalizar cuestionario
        mostrar_resultado(respuestas,pl,categorias)

def inicio():
    pl = Prolog()
    pl.consult("juegos.pl")
    categorias=consultaUnica("caracteristica",pl)  
    respuestas=[]
    cant=len(categorias)
    boton.destroy()  
    texto1.destroy()
    mostrar_preguntas(categorias,pl,respuestas,0,cant)
     
     

root = tk.Tk()
root.title("Cuestionario") 
root.geometry('500x500')   #tamaño de la ventana (anchoXalto)
frm = ttk.Frame(root)   
frm.pack(fill=tk.BOTH, expand=True) 
texto1=ttk.Label(frm, text="GamerBot")  #titulo
texto1.pack(pady=10) 
boton=ttk.Button(frm, text="Iniciar cuestionario", command=inicio) #boton de inicio
boton.place(x=150, y=300)  #necesita una referencia (anchor), por omisión esquina superior izq. Mide en pixels


def on_closing():
        if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
            root.quit()
    
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


