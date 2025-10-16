import tkinter as tk
from tkinter import messagebox
import sqlite3

administradores = {"123": {"nombre": "Juan", "codigo": "123"}}

def iniciarSesionAdministradores():
    if entradaVP.get() in administradores and entradacontrasenia.get() == administradores[entradaVP.get()]['codigo']:
        ventanaMenu = tk.Tk()
        ventanaMenu.attributes('-fullscreen', True)
        ventanaMenu.config(bg="gray")

        textopaginaLogin = tk.Label(ventanaMenu, text=f"Perfil de: {administradores[entradaVP.get()]['nombre']}", font=("Times New Roman", 10), bg="gray")
        textopaginaLogin.place(relx=0, rely=0)

        textopaginaLogin2 = tk.Label(ventanaMenu, text="Menu de opciones", font=("Times New Roman", 20), bg="gray")
        textopaginaLogin2.place(relx=0, rely=0.1)

        botonCerrar(ventanaMenu)

        ventanaPrincipal.destroy()
    else:
        messagebox.showerror("Error", "Codigo o contraseña incorrectos")

def botonCerrar(ventana):
    boton_cerrar = tk.Button(ventana, text="X", command=ventana.destroy, bg="red", fg="white", width=5, height=2)
    boton_cerrar.place(relx=1.0, x=-50, y=10, anchor="ne")

ventanaPrincipal = tk.Tk()
ventanaPrincipal.attributes('-fullscreen', True)
ventanaPrincipal.config(bg="gray")

textoVentanaPrincipal = tk.Label(ventanaPrincipal, text="INICIAR SESION", font=("Times New Roman", 28, "bold"), bg="gray")
textoVentanaPrincipal.pack(pady=50)

texto2VentanaPrincipal = tk.Label(ventanaPrincipal, text="Ingresa tu código", font=("Arial", 20), bg="gray")
texto2VentanaPrincipal.pack(pady=0)

entradaVP = tk.Entry(ventanaPrincipal, width=35, font=("Arial", 15))
entradaVP.pack(pady=0)

espacio = tk.Label(ventanaPrincipal, text="", bg="gray")
espacio.pack(pady=25)

textocontrasenia = tk.Label(ventanaPrincipal, text="Ingresa tu contraseña", font=("Arial", 20), bg="gray")
textocontrasenia.pack(pady=0)

entradacontrasenia = tk.Entry(ventanaPrincipal, width=35, show="*", font=("Arial", 15))
entradacontrasenia.pack(pady=0)

botonCerrar(ventanaPrincipal)

botonlogn = tk.Button(ventanaPrincipal, text="Iniciar sesión", font=("Arial", 20), bg="red", command=iniciarSesionAdministradores)
botonlogn.pack(pady=50)

ventanaPrincipal.mainloop()