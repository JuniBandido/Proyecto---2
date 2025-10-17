#Proyecto 2 de Programacion Avanzada
#Universidad Rafael Landivar
#Tienda de Materiales Electricos

from collections import deque
from datetime import datetime


#ESTRUCTURAS DE DATOS - CLASES BASE

class Product: #Clase para representar un producto en el inventario
    def __init__(self, code, name, category, price, quantity, brand="", description=""):
        self._code = code
        self._name = name
        self._category = category
        self._price = price
        self._quantity = quantity
        self._brand = brand
        self._description = description
 #Getters - Acceso controlado a atributos
    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    @property
    def brand(self):
        return self._brand

    @property
    def description(self):
        return self._description

    #Setters - Modificación controlada con validaciones
    @name.setter
    def name(self, value):
        if value and len(value) > 0:
            self._name = value
        else:
            raise ValueError("El nombre no puede estar vacío")

    @price.setter
    def price(self, value):
        if value >= 0:
            self._price = value
        else:
            raise ValueError("El precio no puede ser negativo")

    @quantity.setter
    def quantity(self, value):
        if value >= 0:
            self._quantity = value
        else:
            raise ValueError("La cantidad no puede ser negativa")

    @description.setter
    def description(self, value):
        self._description = value

    def reduce_stock(self, amount):
        #Metodo para reducir stock de forma ordenada
        if amount <= self._quantity: self._quantity -= amount; return True
        return False

    def add_stock(self, amount):
       #Metodo para agregar stock
        if amount > 0: self._quantity += amount; return True
        return False

    def __str__(self):
        return f"{self._code} - {self._name} ({self._brand}) - Q{self._price:.2f} - Stock: {self._quantity}"

class User:
    #Clase para representar usuarios del sistema

    def __init__(self, username, password, role, full_name):
        self._username, self._password, self._role, self._full_name = username, password, role, full_name
        self._active = True

    # Getters
    @property
    def username(self):
        return self._username

    @property
    def role(self):
        return self._role

    @property
    def full_name(self):
        return self._full_name

    @property
    def active(self):
        return self._active

    # Setters
    @active.setter
    def active(self, value):
        self._active = value

    @full_name.setter
    def full_name(self, value):
        if value and len(value) > 0: self._full_name = value

    def verify_password(self, password):
        #Metodo público para verificar password sin exponer el atributo privado
        return self._password == password

    def change_password(self, old_password, new_password):
        #Permite cambiar la contraseña de forma segura
        if self.verify_password(old_password): self._password = new_password; return True
        return False

    def __str__(self):
        return f"{self._username} - {self._full_name} ({self._role})"

class Sale:
    #Clase para representar una venta

    def __init__(self, sale_id, username, products, total):
        self._sale_id = sale_id
        self._username = username
        self._products = products
        self._total = total
        self._date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def sale_id(self):
        return self._sale_id

    @property
    def username(self):
        return self._username

    @property
    def products(self):
        return self._products.copy()  # Retorna copia para evitar modificación externa

    @property
    def total(self):
        return self._total

    @property
    def date(self):
        return self._date

    def __str__(self): return f"Venta #{self._sale_id} - {self._date} - Q{self._total:.2f}"

