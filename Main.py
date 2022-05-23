from tkinter import *
import os

def CargarImagen(nombre):
    root = os.path.join('Imagenes',nombre)
    image = PhotoImage(file=root)
    return image

PantallaIncial = Tk()
PantallaIncial.title("Battle Ship")
PantallaIncial.geometry("600x600")
PantallaIncial.resizable(height=NO, width=NO)
FondoPrincipal = CargarImagen("FondoPrincipal.png")
Fondo = Label(PantallaIncial, image=FondoPrincipal)
Fondo.place(x=0, y=0)
NombreLabel = Label(PantallaIncial, text= "Ingrese el nombre de marine", bg="white")
NombreLabel.place(x=225, y=230)
NombreJugador = Entry(PantallaIncial, bg="white", fg="black", justify="center")
NombreJugador.place(x=240, y=260)
PantallaIncial.mainloop()
