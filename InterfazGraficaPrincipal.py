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
        textopaginaLogin.grid(row=0, column=0)

        textopaginaLogin2 = tk.Label(ventanaMenu, text="Menu de opciones", font=("Times New Roman", 20),fg="ivory1", bg="#292421")
        textopaginaLogin2.grid(row=2, column=0, pady= 80)

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
imagen.grid(row=0, column=0)

textoIniciarSesionLogin = tk.Label(ventanaLogin, text="INICIAR SESION", font=("Times New Roman", 28, "bold"), bg="#292421", fg="ivory1")
textoIniciarSesionLogin.grid(row=1, column=0, pady=90)

textoIngresaCodigoLogin = tk.Label(ventanaLogin, text="Ingresa tu código", font=("Arial", 20), bg="#292421", fg="ivory1")
textoIngresaCodigoLogin.grid(row=2, column=0)

entradaIngresaCodigoLogin = tk.Entry(ventanaLogin, width=35, font=("Arial", 15))
entradaIngresaCodigoLogin.grid(row=4, column=0)

espacioEnBlanco = tk.Label(ventanaLogin, text="", bg="#292421")
espacioEnBlanco.grid(row=5, column=0, pady=45)

textoIngresaClaveLogin = tk.Label(ventanaLogin, text="Ingresa tu contraseña", font=("Arial", 20), bg="#292421", fg="ivory1")
textoIngresaClaveLogin.grid(row=6, column=0)

entradaIngresaClaveLogin = tk.Entry(ventanaLogin, width=35, show="*", font=("Arial", 15))
entradaIngresaClaveLogin.grid(row=7,column=0)

botonCerrar(ventanaLogin)

botonlogin = tk.Button(ventanaLogin, text="Iniciar sesión", font=("Arial", 20), bg="red", command=iniciarSesionAdministradores)
botonlogin.grid(row=8, column=0, pady=60)

ventanaLogin.mainloop()