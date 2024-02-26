from pyswip import Prolog
from automata import AutomataNombre
from welcome_GUI import get_name
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
import operator
import webbrowser

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


""" def ordenar_mas_apariciones(lista):
    res=[]
    aux={}
    while len(lista)!=0:
        item=lista[0]
        cant=lista.count(item)
        aux[item]=cant
        while item in lista:
            lista.remove(item)
    aux=sorted(aux.items(), reverse=True,key=operator.itemgetter(1)) #ordenar el diccionario de mayor a menor
    for juego in aux:
        res.append(juego[0])
    return res """
def ordenar_mas_apariciones(lista): #con automata
    res=[]
    aux={}
    max=1
    for item in lista:
        if item in res:  #estado 1
            cant=aux[item]+1
            res.remove(item)
            if cant>max:  #estado 3
                index=0
                max=cant
            else:         #estado 4
                referencia=list(aux.keys())[list(aux.values()).index(cant)]
                index=res.index(referencia)
            res.insert(index,item)
            aux[item]+=1

        else: #estado 2
            res.append(item)
            aux[item]=1
    
    #aceptacion
    return res
def open_link(event, link):
    webbrowser.open_new(link)

def mostrar_resultados(juegos):
    pl=Prolog()
    pl.consult("descripciones.pl")
    y_var=70
    root.geometry('510x700')  
    results_title='Estos son los resultados:'
    results_title_label=ttk.Label(root,text=results_title, foreground="black", font=("Helvetica", 12, "bold"))
    results_title_label.place(x=110, y=10)
    for juego in juegos:
        descripcion = consultaX("descripcion", '"' + juego + '"', pl)
        if descripcion:
            game_name = juego
            game_description=descripcion[0]
            game_link = descripcion[1]
            game_title_text = "{}:".format(game_name)
            game_bullet_text = "\u2022 {}".format(game_link)  # Bullet point unicode character
            game_title_label = ttk.Label(root, text=game_title_text, foreground="black", font=("Helvetica", 10, "bold"))
            game_description_label=ttk.Label(root,text=game_description,foreground="black", font=("Helvetica", 10))
            game_bullet_label = ttk.Label(root, text=game_bullet_text, cursor="hand2", foreground="black", font=("Helvetica", 10, "underline"))
            game_bullet_label.bind("<Button-1>", lambda e, link=game_link: open_link(e, link))
            game_title_label.place(x=60,y=y_var)
            y_var+=30
            game_description_label.place(x=50,y=y_var)
            y_var+=120
            game_bullet_label.place(x=50,y=y_var)
            y_var+=40


        



def calcular_resultado(respuestas,pl,categorias):

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
        
        for juego in aux:
            if juego in juegos_posibles:  #los juegos del genero elegido que estan en las consolas elegidas
                res.append(juego)
    
    final=ordenar_mas_apariciones(res)  #los 3 juegos que mas aparecen

    if len(final)==0:
        final=juegos_posibles

    if len(final)>3:
        final=final[0:3]
    mostrar_resultados(final)

    


def mostrar_preguntas(categorias,pl,respuestas,i,cant): 
    
    def listbox(opciones,respuestas):
        rsp=[]
        l=ttk.Label(root,text="Selecciona una o varias opciones")
        l.place(x=150,y=90)
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
        enviar.pack(pady=130,ipadx=10,ipady=10,padx=100)
        widgets.append(enviar)
        
        

    def radiobuttons(opciones,respuestas): 
        respuesta = tk.StringVar()
        y_var=150
        for opcion in opciones:
                radio_button = ttk.Radiobutton(root, text=opcion, variable=respuesta, value=opcion)
                #radio_button.pack(anchor=tk.W, padx=70,ipady=10)
                radio_button.place(y=y_var,x=70)
                y_var+=40
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
        #boton_enviar.pack(anchor=tk.W,padx=80,pady=10,ipadx=10,ipady=10)
        boton_enviar.place(x=200,y=y_var,height=30,width=80)
        widgets.append(boton_enviar)


    if i<cant:
        widgets=[]
        pregunta=consultaX("pregunta",categorias[i],pl)[0]
        l1=ttk.Label(root,text="Pregunta "+str(i+1)+" de "+str(cant))
        l1.place(x=50,y=10)
        l2=ttk.Label(root,text=pregunta,font=("Helvetica", 16, "bold"))
        l2.place(x=60,y=50)
        widgets.append(l1)
        widgets.append(l2)
        opciones=eliminar_repetidos(consultaX(categorias[i],"_",pl))
        
        if (i==0):   #hagamos que la pregunta de consola sea la 1era
            listbox(opciones,respuestas)
        else:
            radiobuttons(opciones,respuestas)


    else:    #finalizar cuestionario
        calcular_resultado(respuestas,pl,categorias)

def inicio():
    pl = Prolog()
    pl.consult("juegos.pl")
    categorias=consultaUnica("caracteristica",pl)  
    respuestas=[]
    cant=len(categorias)
    boton.destroy()  
    texto1.destroy()
    texto2_ttk.destroy()
    mostrar_preguntas(categorias,pl,respuestas,0,cant)
     
     
def iniciarGUI(lista):
    def callback(name):
        #print("Name: " + name)
        automata = AutomataNombre()
        if automata.validar_nombre(name):
            print("El nombre es válido.")
            lista.append(name)
        else:
            print("El nombre no es válido.")
    
    # Comienza el flujo del programa
    name = get_name(callback)
lista_nombres=[]
# Obtener el nombre y usarlo en el código
iniciarGUI(lista_nombres)
#print("Nombre obtenido:", lista_nombres)
while len(lista_nombres)==0:
    iniciarGUI(lista_nombres)

nombre_validado=lista_nombres[0]

root = tk.Tk()
root.title("Cuestionario") 
root.geometry('510x500')   #tamaño de la ventana (anchoXalto)
frm = ttk.Frame(root)   
frm.pack(fill=tk.BOTH, expand=True) 
texto1=ttk.Label(frm, text="GamerBot",font=("Helvetica", 20, "bold"))  #titulo
texto1.pack(pady=10,ipady=40,anchor=tk.N)
texto="Bienvenido: "+nombre_validado+"! \nCuando estes listo, inicia el cuestionario."
print(nombre_validado)
texto2_ttk=ttk.Label(frm, text=texto,font=("Helvetica", 11))
texto2_ttk.place(x=100,y=160)
boton=ttk.Button(frm, text="Iniciar cuestionario", command=inicio) #boton de inicio
boton.place(x=170, y=300,width=140,height=50)  #necesita una referencia (anchor), por omisión esquina superior izq. Mide en pixels

def on_closing():
        if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
            root.quit()
    
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


