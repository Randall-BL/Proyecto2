from tkinter import *
import os

def CargarImagen(nombre):
    root = os.path.join('Imagenes',nombre)
    image = PhotoImage(file=root)
    return image
def about():#Funcion para la ventana creditos
    ventanabout.deiconify()

def VentanaSalonFama():
    ventanaFama.deiconify()

PantallaIncial = Tk()
PantallaIncial.title("Battle Ship")
PantallaIncial.geometry("600x600")
PantallaIncial.resizable(height=NO, width=NO)
C_menu=Canvas(PantallaIncial, width=1200, height=900, bg='black')
C_menu.place(x=0, y=0)
C_menu.fondo=CargarImagen('FondoPrincipal.png')
imgCanvas= C_menu.create_image(0,0, anchor=NW, image= C_menu.fondo)
"""
FondoPrincipal = CargarImagen("FondoPrincipal.png")
Fondo = Label(PantallaIncial, image=FondoPrincipal)
Fondo.place(x=0, y=0)"""

NombreLabel = Label(PantallaIncial, text= "Ingrese el nombre de marine", bg="white")
NombreLabel.place(x=225, y=230)
NombreJugador = Entry(PantallaIncial, bg="white", fg="black", justify="center")
NombreJugador.place(x=240, y=260)

ventanabout=Toplevel(PantallaIncial)#Ventanda de creditos
ventanabout.title("About")
ventanabout.geometry("1200x900+390+40")
ventanabout.resizable(width= NO, height=NO)
C_about=Canvas(ventanabout,width=1200, height=900,bg="Pink")
C_about.place(x=0, y=0)
C_about.fondo=CargarImagen("About.png")
imgAbout=C_about.create_image(0,0, anchor=NW, image=C_about.fondo)
ventanabout.withdraw()

ventanaFama=Toplevel(PantallaIncial)#Ventanda de creditos
ventanaFama.title("About")
ventanaFama.geometry("1200x900+390+40")
ventanaFama.resizable(width= NO, height=NO)
C_fama=Canvas(ventanaFama,width=1200, height=900,bg="Pink")
C_fama.place(x=0, y=0)
C_fama.fondo=CargarImagen("About.png")
imgFama=C_fama.create_image(0,0, anchor=NW, image=C_fama.fondo)
ventanaFama.withdraw()










PlayAbout=Button(C_menu,width=6,height=2,bg="Pink",text="Crèditos",command=about).place(x=200, y=300)
SalonFamaButton=Button(C_menu,width=6,height=2,bg="Pink",text="TopScores",command=VentanaSalonFama).place(x=500, y=300)




PantallaIncial.mainloop()
