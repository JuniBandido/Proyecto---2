import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

administradores = {"123": {"nombre": "Junior (José Noguera)", "codigo": "123"}}

def iniciarSesionAdministradores():
    if entradaIngresaCodigoLogin.get() in administradores and entradaIngresaClaveLogin.get() == administradores[entradaIngresaCodigoLogin.get()]['codigo']:
        ventanaMenu = tk.Tk()
        ventanaMenu.attributes('-fullscreen', True)
        ventanaMenu.config(bg="#292421")

        textopaginaLogin = tk.Label(ventanaMenu, text=f"Perfil de: {administradores[entradaIngresaCodigoLogin.get()]['nombre']}", font=("Times New Roman", 20),fg="ivory1", bg="#292421")
        textopaginaLogin.pack()

        textopaginaLogin2 = tk.Label(ventanaMenu, text="Menu de opciones", font=("Times New Roman", 20),fg="ivory1", bg="#292421")
        textopaginaLogin2.pack(pady=20)

        botonCerrar(ventanaMenu)

        ventanaLogin.destroy()

    else:
        messagebox.showerror("Error", "Codigo o contraseña incorrectos")

def botonCerrar(ventana):
    boton_cerrar = tk.Button(ventana, text="X", command=ventana.destroy, bg="red", fg="white", width=5, height=2)
    boton_cerrar.place(relx=1.0, x=-50, y=10, anchor="ne")

ventanaLogin = tk.Tk()
ventanaLogin.attributes('-fullscreen', True)
ventanaLogin.config(bg="#292421")

imagenLogo = tk.PhotoImage(file="LogoYimsaWeb-1.png")
imagen = ttk.Label(image=imagenLogo)
imagen.pack(side="top")

textoIniciarSesionLogin = tk.Label(ventanaLogin, text="INICIAR SESION", font=("Times New Roman", 28, "bold"), bg="#292421", fg="ivory1")
textoIniciarSesionLogin.pack(pady=50)

textoIngresaCodigoLogin = tk.Label(ventanaLogin, text="Ingresa tu código", font=("Arial", 20), bg="#292421", fg="ivory1")
textoIngresaCodigoLogin.pack(pady=0)

entradaIngresaCodigoLogin = tk.Entry(ventanaLogin, width=35, font=("Arial", 15))
entradaIngresaCodigoLogin.pack(pady=0)

espacioEnBlanco = tk.Label(ventanaLogin, text="", bg="#292421")
espacioEnBlanco.pack(pady=25)

textoIngresaClaveLogin = tk.Label(ventanaLogin, text="Ingresa tu contraseña", font=("Arial", 20), bg="#292421", fg="ivory1")
textoIngresaClaveLogin.pack(pady=0)

entradaIngresaClaveLogin = tk.Entry(ventanaLogin, width=35, show="*", font=("Arial", 15))
entradaIngresaClaveLogin.pack(pady=0)

botonCerrar(ventanaLogin)

botonlogin = tk.Button(ventanaLogin, text="Iniciar sesión", font=("Arial", 20), bg="red", command=iniciarSesionAdministradores)
botonlogin.pack(pady=50)

ventanaLogin.mainloop()