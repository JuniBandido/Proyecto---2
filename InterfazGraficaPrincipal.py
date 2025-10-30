import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class VentanaLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de sesión")
        self.config(bg="gray10")
        self.state("zoomed")

        self.imagen = tk.PhotoImage(file="LogoYimsaWeb-1.png")
        imagenEtiqueta = tk.Label(self, image=self.imagen)
        imagenEtiqueta.pack()

        tk.Frame(self, bg="white", width=300, height=600).place(x=90, y=90)

        tk.Label(self, text="Código de Usuario:", font=("Times New Roman", 20), bg="white").place(x=100, y=100)
        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.place(x=100, y=140)

        tk.Label(self, text="Contraseña:", font=("Times New Roman", 20), bg="white").place(x=100, y=180)
        self.entry_contraseña = ttk.Entry(self, show="*")
        self.entry_contraseña.place(x=100, y=220)

        ttk.Button(self, text="Iniciar sesión", command=self.verificar_login).place(x=100, y=280)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM administradores WHERE codigo = ? AND contrasenia = ?", (usuario, contraseña))
        resultado_admin = cursor.fetchone()

        cursor.execute("SELECT * FROM empleados WHERE codigo = ? AND contrasenia = ?", (usuario, contraseña))
        resultado_empleado = cursor.fetchone()

        conexion.close()

        if resultado_admin:
            self.withdraw()
            VentanaPrincipalAdministradores(self, usuario)
        elif resultado_empleado:
            self.withdraw()
            VentanaPrincipalEmpleados(self, usuario)
        else:
            messagebox.showerror("Error", "Código o Contraseña incorrectos")

class VentanaPrincipalEmpleados(tk.Toplevel):
    def __init__(self, ventana_login, usuario):
        super().__init__()
        self.title("Panel Principal Empleado")
        self.state("zoomed")
        self.ventana_login = ventana_login  # Guarda referencia

        tk.Label(self,text="Ventana de empleados").place(x=100, y=100)

        ttk.Button(self, text="Cerrar sesión", command=self.cerrar_sesion).place(x=100, y=600)

    def cerrar_sesion(self):
        self.destroy()
        self.ventana_login.deiconify()
        self.ventana_login.state("zoomed")
        self.ventana_login.entry_usuario.delete(0, tk.END)
        self.ventana_login.entry_contraseña.delete(0, tk.END)

class VentanaPrincipalAdministradores(tk.Toplevel):
    def __init__(self, ventana_login, usuario):
        super().__init__()
        self.title("Panel Principal Administradores")
        self.state("zoomed")
        self.ventana_login = ventana_login  # Guarda referencia

        tk.Label(self, text=f"Bienvenido, {usuario}", font=("Arial", 24)).place(x=100, y=100)
        ttk.Button(self, text="Cerrar sesión", command=self.cerrar_sesion).place(x=100, y=200)

        ttk.Button(self, text="Ingresar usuarios", width=20, command=self.ingresar_nuevo).place(x=800, y=100)
        ttk.Button(self, text="Ingresar Productos", width=20, command=self.ingresar_productos).place(x=800, y=200)

    def ingresar_nuevo(self):
        IngresarUsuarioNuevo(self.ventana_login)

    def ingresar_productos(self):
        RegistrarProductos(self.ventana_login)

    def cerrar_sesion(self):
        self.destroy()
        self.ventana_login.deiconify()
        self.ventana_login.state("zoomed")
        self.ventana_login.entry_usuario.delete(0, tk.END)
        self.ventana_login.entry_contraseña.delete(0, tk.END)

class RegistrarProductos(tk.Toplevel):
    def __init__(self, ventana_login):
        super().__init__()
        self.title("Agregar Productos")
        self.state("zoomed")
        self.ventana_login = ventana_login

        tk.Label(text="Ingresa productos")
        nombreProducto = ttk.Entry()
        nombreProducto.place(x=100, y=200)

        ttk.Button(self, text="Atrás", width=20, command=self.destroy).place(x=800, y=300)

class IngresarUsuarioNuevo(tk.Toplevel):
    def __init__(self, ventana_login):
        super().__init__()
        self.title("Agregar nuevos miembros a la empresa")
        self.state("zoomed")
        self.ventana_login = ventana_login

        tk.Label(self, text="Ingresa el nombre del nuevo usuario").place(x=100, y=100)
        condigoNuevo = tk.Entry(self)
        condigoNuevo.place(x=100, y=130)

        tk.Label(self, text="Ingresa la contraseña del nuevo usuario").place(X=100, Y=200)
        contraseñaNuevo = tk.Entry(self)
        contraseñaNuevo.place(x=100, y=230)

        ttk.Button(self, text="Volver", command=self.destroy).place(x=100, y=200)

if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()
