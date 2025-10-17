#Proyecto 2 de Programacion Avanzada
#Universidad Rafael Landivar
#Tienda de Materiales Electricos

from collections import deque


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

