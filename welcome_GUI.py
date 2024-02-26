import tkinter as tk
from tkinter import ttk

def get_name(callback):
    def submit_name():
        name = name_var.get()
        root.destroy()
        name_returned = callback(name)  # Llama a la función de retorno de llamada
        return name_returned  # Devuelve el nombre retornado por la función de retorno de llamada
    
    root = tk.Tk()
    root.title("Ingrese su nombre:")

    def on_closing():
        root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    mainframe = ttk.Frame(root, padding="20")
    mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    name_label = ttk.Label(mainframe, text="NAME: ")
    name_label.grid(column=0, row=0, sticky=tk.W)
    name_var = tk.StringVar()  # StringVar to store DNI
    name_entry = ttk.Entry(mainframe, textvariable=name_var)
    name_entry.grid(column=1, row=0, sticky=tk.W)
    submit_button = ttk.Button(mainframe, text="Submit", command=submit_name)
    submit_button.grid(column=1, row=3, sticky=tk.W)

    root.mainloop()
