from pyswip import Prolog

#funciones consulta prolog
def consultaX(relacion,x,pl): #los parametros son strings que definen la consulta -> relacion(X,y)
    query=relacion + "(" + x + ",Y)"
    res_query=list(pl.query(query))
    res=[]
    for item in res_query:
        final=item["Y"]
        if type(final)==bytes:
            final=final.decode("utf-8")   #pasar de byte-string a string
        res.append(final)
    return res

def consultaY(relacion,y,pl): 
    query=relacion + "(X," + y +")"
    res_query=list(pl.query(query))
    res=[]
    for item in res_query:
        final=item["X"]
        if type(final)==bytes:
            final=final.decode("utf-8")   #pasar de byte-string a string
        res.append(final)

    return res

def consultaANY(relacion,pl): #por si acaso
    query=relacion + "(X,Y)"
    res=[]
    res_query=list(pl.query(query))
    for item in res_query:
        final=[item["X"],item["Y"]]
        if type(final[0])==bytes:
            final[0]=final[0].decode("utf-8")   
        if type(final[1])==bytes:
            final[1]=final[1].decode("utf-8")   
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


main()