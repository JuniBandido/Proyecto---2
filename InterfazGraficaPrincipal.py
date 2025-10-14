import tkinter as tk
from tkinter import messagebox

ventanaLogin = tk.Tk()
ventanaLogin.attributes('-fullscreen', True)
ventanaLogin.config(bg="gray")

textologn = tk.Label(ventanaLogin, text="INICIAR SESION", font=("Times New Roman", 28, "bold"), bg="gray")
textologn.pack(pady=50)

textocodigo = tk.Label(ventanaLogin, text="Ingresa tu código", font=("Arial", 20), bg="gray")
textocodigo.pack(pady=0)

entradalogn = tk.Entry(ventanaLogin, width=35, font=("Arial", 15))
entradalogn.pack(pady=0)

espacio = tk.Label(ventanaLogin, text="", bg="gray")
espacio.pack(pady=25)

textocontrasenia = tk.Label(ventanaLogin, text="Ingresa tu contraseña", font=("Arial", 20), bg="gray")
textocontrasenia.pack(pady=0)

entradacontrasenia = tk.Entry(ventanaLogin, width=35, show="*", font=("Arial", 15))
entradacontrasenia.pack(pady=0)

def botonCerrar(ventana):
    boton_cerrar = tk.Button(ventana, text="X", command=ventana.destroy, bg="red", fg="white")
    boton_cerrar.place(x=1520, y=0)

botonCerrar(ventanaLogin)

def iniciarSesion():
    if entradalogn.get() == "EST1619125" and entradacontrasenia.get() == "123":
        ventanaMenu = tk.Tk()
        ventanaMenu.attributes('-fullscreen', True)
        ventanaMenu.config(bg="gray")

        textopaginaLogin = tk.Label(ventanaMenu, text="Bienvenido", font=("Times New Roman", 40), bg="gray")
        textopaginaLogin.pack(pady=60)

        textopaginaLogin2 = tk.Label(ventanaMenu, text="Este es la pagina de login", font=("Times New Roman", 40), bg="gray")
        textopaginaLogin2.pack(pady=60, padx=30)

        botonCerrar(ventanaMenu)

        ventanaLogin.destroy()
    else:
        messagebox.showerror("Error", "Codigo o contraseña incorrectos")

botonlogn = tk.Button(ventanaLogin, text="Iniciar sesión", font=("Arial", 20), bg="red", command=iniciarSesion)
botonlogn.pack(pady=50)

ventanaLogin.mainloop()