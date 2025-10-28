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

    #Estructuras lineales: pilas y colas

class Stack:
    #Implementacion de pila
    def __init__(self):
        self._items = []
    def push(self, item):
        self._items.append(item)
    def pop(self):
        return self._items.pop() if not self.is_empty() else None
    def peek(self):
        return self._items[-1] if not self.is_empty() else None
    def is_empty(self):
        return len(self._items) == 0
    def size(self):
        return len(self._items)
    def clear(self):
        self._items = []
    def show_all(self):
        return self._items.copy()  # Aca retornamos la copia para proteger sus datos

class Queue:
    #Implementacion de cola
    def __init__(self):
        self._items = deque()
    def enqueue(self, item):
        self._items.append(item)
    def dequeue(self):
        return self._items.popleft() if not self.is_empty() else None
    def front(self):
        return self._items[0] if not self.is_empty() else None
    def is_empty(self):
        return len(self._items) == 0
    def size(self):
        return len(self._items)
    def clear(self):
        self._items.clear()
    def show_all(self):
        return list(self._items)  # Retorna copia

#Sistema principal, gestor de inventario
class InventorySystem:
    #Sistema principal de gestion de inventario
    def __init__(self):
        self._products = []
        self._users = []
        self._sales = [] #Para los datos
        self._sale_counter = 1 #Contador para los ID de ventas
        self._action_history = Stack()  #Historial de acciones
        self._pending_tasks = Queue() #Historial de tareas pendientes
        self._current_user = None #Usuario actual
        self._initialize_default_data()

    def _initialize_default_data(self): #Es protegido para solo llamarlo internamente
        #Creamos usuarios
        self._users.extend([
            User("admin", "admin123", "administrador", "Administrador Principal"),
            User("vendedor", "vend123", "dependiente", "Juan Perez")])
        #Creamos productos de prueba
        productos_ejemplo = [
            Product("BOMB-LED-9W", "Bombillo LED 9W", "Iluminación", 25.50, 50, "Philips", "Luz día 6500K E27"),
            Product("TUBO-LED-4P", "Tubo LED 4 Pies", "Iluminación", 45.00, 30, "Sylvania", "Blanco frío 18W T8"),
            Product("LAMP-LED-PANEL", "Panel LED 600x600", "Iluminación", 180.00, 15, "Osram", "36W para cielo falso"),
            Product("SPOT-LED-5W", "Spot LED Empotrable", "Iluminación", 32.00, 40, "Technolite", "5W 3000K GU10"),
            Product("TOMA-DOBLE-15A", "Tomacorriente Doble 15A", "Accesorios", 18.75, 100, "Steck","Blanco polar 250V"),
            Product("APAG-SIMPLE-15A", "Apagador Simple 15A", "Accesorios", 12.50, 80, "Legrand", "Blanco mate"),
            Product("BREAKER-20A", "Breaker 20A 1P", "Accesorios", 45.00, 60, "Square D", "Para tablero principal"),
            Product("CAJA-RECT-4x2", "Caja Rectangular 4x2", "Accesorios", 8.00, 120, "Conductores", "Para apagadores"),
            Product("CABLE-TW-12", "Cable TW Calibre 12", "Cables", 3.50, 500, "Condumex", "75m rollo negro"),
            Product("CABLE-THWN-10", "Cable THWN Calibre 10", "Cables", 5.25, 300, "Camesa", "75m rollo rojo"),
            Product("CABLE-PAR-TRENZ", "Cable Par Trenzado CAT6", "Cables", 1.20, 200, "Belden", "305m caja datos"),
            Product("CABLE-COAX-RG6", "Cable Coaxial RG6", "Cables", 0.85, 150, "Commscope", "Para TV y video"),
            Product("TUBO-EMT-1/2", "Tubo EMT 1/2", "Canalización", 35.00, 80, "Camesa", "3 metros galvanizado"),
            Product("TUBO-PVC-3/4", "Tubo PVC 3/4", "Canalización", 28.50, 70, "Durman", "3 metros schedule 40"),
            Product("DUCTO-FLEX-1/2", "Ducto Flexible 1/2", "Canalización", 15.75, 90, "Electroduct","Metálico 2 metros"),
            Product("CANALETA-40x20", "Canaleta 40x20mm", "Canalización", 12.00, 110, "Panduit", "PVC blanco 2m"),
            Product("VENT-TECHO-48", "Ventilador de Techo 48", "Ventilación", 450.00, 12, "Hunter", "Madera 5 aspas"),
            Product("VENT-BAÑO-100", "Ventilador de Baño 100CFM", "Ventilación", 185.00, 25, "Broan","Extractor silencioso"),
            Product("VENT-PEDESTAL-16", "Ventilador Pedestal 16", "Ventilación", 220.00, 18, "Lasko", "3 velocidades"),
            Product("VENT-TUBO-4", "Ventilador de Tubo 4", "Ventilación", 95.00, 30, "S&P", "Para ductos 100CFM"),
            Product("CONEC-HEMBRA-15A", "Conector Hembra 15A", "Conectores", 4.50, 200, "Ideal", "Para cable #12-14"),
            Product("TERMINAL-ANILLO-12", "Terminal Anillo #12", "Conectores", 0.25, 500, "3M", "Estañado para 12-10"),
            Product("CINTA-AISL-NEG", "Cinta Aislante Negra", "Conectores", 12.00, 75, "Scotch", "3/4 x 20m"),
            Product("TAPA-TOMA-BCO", "Tapa para Tomacorriente", "Conectores", 2.00, 300, "Steck","Blanco seguridad niños"),
            Product("SENS-MOV-PIR", "Sensor de Movimiento PIR", "Automatización", 120.00, 25, "Leviton","180° interior/exterior"),
            Product("TIMER-DIGI-7D", "Timer Digital 7 Días", "Automatización", 85.00, 20, "Intermatic","Programable 40A"),
            Product("DIMMER-LED-600W", "Dimmer para LED 600W", "Automatización", 65.00, 35, "Lutron","Control intensidad"),
            Product("CONTROL-MOTOR", "Control para Motor 1HP", "Automatización", 150.00, 15, "Siemens","Reversa y protección")
        ]
        for producto in productos_ejemplo: self.add_product(producto)

    @property
    def current_user(self):
        return self._current_user  # Getter para usuario actual

    #GESTION DE USUARIOS
    def login(self, username, password):
        #Inicia sesion de usuario
        for user in self._users:
            if user.username == username and user.verify_password(password):
                if user.active:
                    self._current_user = user
                    self._action_history.push(f"Ingresar: {username}")
                    return True, f"Bienvenido {user.full_name}"
                else:
                    return False, "Usuario inactivo"
        return False, "Usuario o contraseña incorrectos"

    def logout(self):
        #cierre de sesion
        if self._current_user:
            self._action_history.push(f"Cierre de sesion: {self._current_user.username}")
            self._current_user = None

    def add_user(self, user):
        #SOLO ADMIN AGREGA NUEVO USUARIOS
        if not self._validate_admin_permission(): return False, "No tiene permisos"
        if any(u.username == user.username for u in self._users): return False, "Usuario ya existe"
        self._users.append(user)
        self._action_history.push(f"Usuario creado: {user.username}")
        return True, "Usuario creado exitosamente"

    def list_users(self):
        #Lista todos los usuarios y retorna copia para proteger datos
        return self._users.copy() if self._validate_admin_permission() else []

    def _validate_admin_permission(self):
        #Valida permisos de administrador
        return self._current_user and self._current_user.role == "administrador"

    #GESTION PRODUCTOS
    def add_product(self, product):
        #Agrega un producto al inventario
        if any(p.code == product.code for p in self._products): return False, "Código ya existe"
        self._products.append(product)
        if self._current_user: self._action_history.push(f"Producto agregado: {product.code}")
        return True, "Producto agregado exitosamente"

    def search_product_by_code(self, code):
        #Busqueda secuencial por codigo
        for product in self._products:
            if product.code == code:
                return product
        return None

    def search_products_sequential(self, key, value):
        #Busqueda secuencial flexible
        results = []
        for product in self._products:
            try:
                item_value = getattr(product, key)
                if isinstance(item_value, str) and isinstance(value, str):
                    if value.lower() in item_value.lower():
                        results.append(product)
                elif item_value == value:
                    results.append(product)
            except AttributeError:
                continue
        return results

    def list_products(self):
        return self._products.copy()  # Retorna copia para protección

    def update_product(self, code, **kwargs):
        #Actualiza un producto existente
        if not self._validate_admin_permission(): return False, "No tiene permisos"
        product = self.search_product_by_code(code)
        if not product: return False, "Producto no encontrado"
        try:
            if 'name' in kwargs: product.name = kwargs['name']
            if 'price' in kwargs: product.price = kwargs['price']
            if 'quantity' in kwargs: product.quantity = kwargs['quantity']
            if 'description' in kwargs: product.description = kwargs['description']
            self._action_history.push(f"Producto actualizado: {code}")
            return True, "Producto actualizado exitosamente"
        except ValueError as e:
            return False, str(e)

    def delete_product(self, code):
        #Elimina un producto del inventario
        if not self._validate_admin_permission(): return False, "No tiene permisos"
        product = self.search_product_by_code(code)
        if product:
            self._products.remove(product)
            self._action_history.push(f"Producto eliminado: {code}")
            return True, "Producto eliminado exitosamente"
        return False, "Producto no encontrado"

    def get_products_by_category(self, category):
        #Obtiene productos por categoría
        return [p for p in self._products if p.category.lower() == category.lower()]

    #ALGORITMOS DE ORDENAMIENTO (QUICKSORT)
    def quick_sort_products(self, products=None, key='name'):
        #QuickSort recursivo para ordenar productos
        if products is None:
            products = self._products.copy()

        if len(products) <= 1:
            return products

        #Elegir pivote
        pivot = products[len(products) // 2]
        pivot_value = getattr(pivot, key)

        # Particion
        left = []
        middle = []
        right = []

        for product in products:
            current_value = getattr(product, key)
            if current_value < pivot_value:
                left.append(product)
            elif current_value == pivot_value:
                middle.append(product)
            else:
                right.append(product)

        #Recursividad
        return self.quick_sort_products(left, key) + middle + self.quick_sort_products(right, key)

    def get_products_sorted_by_name(self):
        # Obtiene productos ordenados por nombre usando QuickSort
        return self.quick_sort_products(key='name')

    def get_products_sorted_by_stock(self):
        # Obtiene productos ordenados por stock usando QuickSort
        return self.quick_sort_products(key='quantity')

    def get_products_sorted_by_price(self):
        # Obtiene productos ordenados por precio usando QuickSort
        return self.quick_sort_products(key='price')

    def get_products_sorted_by_category(self):
        # Obtiene productos ordenados por categoria usando QuickSort
        return self.quick_sort_products(key='category')

    #METODOS DE BUSQUEDA BINARIA
    def binary_search_products(self, key, value):
        #Busqueda binaria para productos ordenados
        sorted_products = self.quick_sort_products(key=key)

        low, high = 0, len(sorted_products) - 1
        results = []

        while low <= high:
            mid = (low + high) // 2
            current_product = sorted_products[mid]
            current_value = getattr(current_product, key)

            if current_value == value:
                #Encontramos coincidencia, buscar adyacentes
                results.append(current_product)

                #Buscar hacia izquierda
                left = mid - 1
                while left >= 0 and getattr(sorted_products[left], key) == value:
                    results.append(sorted_products[left])
                    left -= 1

                #Buscar hacia derecha
                right = mid + 1
                while right < len(sorted_products) and getattr(sorted_products[right], key) == value:
                    results.append(sorted_products[right])
                    right += 1

                return results
            elif current_value < value:
                low = mid + 1
            else:
                high = mid - 1

        return results

    def binary_search_by_name(self, name):
        #Busqueda binaria por nombre
        return self.binary_search_products('name', name)

    def binary_search_by_category(self, category):
        #Busqueda binaria por categoria
        return self.binary_search_products('category', category)

    def binary_search_by_price(self, price):
        #Busqueda binaria por precio exacto
        return self.binary_search_products('price', float(price))

    #METODOS DE BUSQUEDA SECUENCIAL
    def search_products_by_name(self, name):
        #Busqueda secuencial por nombre
        return self.search_products_sequential('name', name)

    def search_products_by_category(self, category):
        #Busqueda secuencial por categoria
        return self.search_products_sequential('category', category)

    def search_products_by_brand(self, brand):
        #Busqueda secuencial por marca
        return self.search_products_sequential('brand', brand)

    #GESTION VENTAS
    def create_sale(self, product_codes_quantities):
        #Crea una nueva venta
        if not self._current_user: return False, "Debe iniciar sesión"
        #Validar productos y stock primero
        for code, quantity in product_codes_quantities:
            product = self.search_product_by_code(code)
            if not product: return False, f"Producto {code} no encontrado"
            if product.quantity < quantity: return False, f"Stock insuficiente para {product.name}"
        #Procesar venta
        sale_products, total = [], 0
        for code, quantity in product_codes_quantities:
            product = self.search_product_by_code(code)
            product.reduce_stock(quantity)
            subtotal = product.price * quantity
            sale_products.append(
                {'code': product.code, 'name': product.name, 'quantity': quantity, 'price': product.price,
                 'subtotal': subtotal})
            total += subtotal
        #Crear y registrar venta
        sale = Sale(self._sale_counter, self._current_user.username, sale_products, total)
        self._sales.append(sale)
        self._sale_counter += 1
        self._action_history.push(f"Venta registrada: #{sale.sale_id}")
        return True, f"Venta registrada exitosamente. Total: Q{total:.2f}"

    def list_sales(self):
        return self._sales.copy()

    def get_sales_by_user(self, username):
        return [s for s in self._sales if s.username == username]

    #Reportes y Estadisticas
    def get_total_sales(self):
        return sum(sale.total for sale in self._sales)

    def get_low_stock_products(self, threshold=5):
        return [p for p in self._products if p.quantity <= threshold]

    def get_sales_statistics(self):
        #Obtiene estadísticas generales de ventas
        if not self._sales: return {'total_sales': 0, 'total_amount': 0, 'average_sale': 0}
        total_amount = self.get_total_sales()
        return {'total_sales': len(self._sales), 'total_amount': total_amount,
                'average_sale': total_amount / len(self._sales)}

    def get_action_history(self, limit=10):
        #Obtiene el historial de acciones recientes
        history = self._action_history.show_all()
        return history[-limit:] if len(history) > limit else history

# FUNCIONES DE MENÚ E INTERFAZ
def show_menu(title, options, user=None):
    print(f"          {title}{f' - {user.full_name}' if user else ''}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
def main_menu():
    show_menu("SISTEMA DE GESTIÓN - TIENDA DE MATERIAL ELECTRICO", ["Iniciar Sesión", "Salir"])

def admin_menu(user):
    show_menu("MENÚ ADMINISTRADOR",
              ["Gestionar Usuarios", "Registrar Producto", "Consultar Inventario",
               "Editar Producto", "Eliminar Producto", "Ordenar Productos ",
               "Búsqueda Avanzada", "Generar Reportes", "Ver Estadísticas",
               "Ver Historial", "Cerrar Sesión"], user)

def employee_menu(user):
    show_menu("MENÚ EMPLEADO",
              ["Consultar Inventario", "Buscar Producto", "Ordenar Productos",
               "Búsqueda Avanzada", "Registrar Venta", "Ver Historial Ventas",
               "Cerrar Sesión"], user)

def manage_users(system):
    while True:
        show_menu("GESTIÓN DE USUARIOS", ["Listar Usuarios", "Crear Nuevo Usuario", "Volver"])
        option = input("\nSeleccione una opción: ")
        if option == "1":
            users = system.list_users()
            print("\n--- LISTA DE USUARIOS ---")
            if users:
                for i, user in enumerate(users, 1):
                    status = "Activo" if user.active else "Inactivo"
                    print(f"{i}. {user.username} - {user.full_name} - {user.role} - {status}")
            else:
                print("No hay usuarios para mostrar")
        elif option == "2":
            print("\n--- CREAR NUEVO USUARIO ---")
            username, password, full_name = input("Usuario: "), input("Contraseña: "), input("Nombre completo: ")
            role = "administrador" if input("Rol (1=Admin, 2=Empleado): ") == "1" else "empleado"
            success, msg = system.add_user(User(username, password, role, full_name))
            print(f"\n{msg}")
        elif option == "3":
            break
        else:
            print("\nOpción no válida")

def register_product(system):
    print("\n--- REGISTRAR PRODUCTO ---")
    try:
        product = Product(
            input("Código: ").upper(), input("Nombre: "), input("Categoría: "),
            float(input("Precio: ")), int(input("Cantidad: ")), input("Marca: "), input("Descripción: ")
        )
        success, msg = system.add_product(product)
        print(f"\n{msg}")
    except ValueError:
        print("\nError: Precio o cantidad inválidos")

def view_inventory(system):
    print("\n--- INVENTARIO ---")
    products = system.list_products()
    if products:
        for i, p in enumerate(products, 1):
            print(
                f"\n{i}. Código: {p.code}\n   Nombre: {p.name}\n   Marca: {p.brand}\n   Categoría: {p.category}\n   Precio: Q{p.price:.2f}\n   Stock: {p.quantity}")
            if p.description: print(f"   Descripción: {p.description}")
    else:
        print("No hay productos")

def edit_product(system):
    print("\n--- EDITAR PRODUCTO ---")
    product = system.search_product_by_code(input("Código: ").upper())
    if not product: print("Producto no encontrado"); return
    print(f"Editando: {product}")
    updates = {}
    if name := input(f"Nombre [{product.name}]: "): updates['name'] = name
    if price := input(f"Precio [{product.price}]: "): updates['price'] = float(price)
    if quantity := input(f"Cantidad [{product.quantity}]: "): updates['quantity'] = int(quantity)
    if description := input(f"Descripción [{product.description}]: "): updates['description'] = description
    if updates:
        success, msg = system.update_product(product.code, **updates)
        print(msg)
    else:
        print("No se realizaron cambios")

def delete_product(system):
    print("\n--- ELIMINAR PRODUCTO ---")
    product = system.search_product_by_code(input("Código: ").upper())
    if not product: print("Producto no encontrado"); return
    print(f"Producto: {product}")
    if input("¿Confirmar eliminación? (s/n): ").lower() == 's':
        success, msg = system.delete_product(product.code)
        print(msg)
    else:
        print("Operación cancelada")

def search_product(system):
    print("\n--- BUSCAR PRODUCTO ---")
    option = input("Buscar por: 1=Código, 2=Nombre, 3=Categoría: ")
    if option == "1":
        product = system.search_product_by_code(input("Código: ").upper())
        if product: print(f"Encontrado: {product}"); return
    elif option == "2":
        results = system.search_products_by_name(input("Nombre: "))
    elif option == "3":
        results = system.get_products_by_category(input("Categoría: "))
    else:
        print("Opción inválida")
        return
    if results:
        print(f"Se encontraron {len(results)} productos:")
        for p in results: print(f" - {p}")
    else:
        print("No se encontraron productos")


def sort_products_menu(system):
    print("\n--- ORDENAR PRODUCTOS ---")
    print("1. Ordenar por Nombre")
    print("2. Ordenar por Stock")
    print("3. Ordenar por Precio")
    print("4. Ordenar por Categoría")
    print("5. Volver")

    option = input("Seleccione opción: ")

    if option == "1":
        products = system.get_products_sorted_by_name()
        print("\n PRODUCTOS ORDENADOS POR NOMBRE:")
    elif option == "2":
        products = system.get_products_sorted_by_stock()
        print("\n PRODUCTOS ORDENADOS POR STOCK:")
    elif option == "3":
        products = system.get_products_sorted_by_price()
        print("\n PRODUCTOS ORDENADOS POR PRECIO:")
    elif option == "4":
        products = system.get_products_sorted_by_category()
        print("\n PRODUCTOS ORDENADOS POR CATEGORÍA:")
    elif option == "5":
        return
    else:
        print("Opción inválida")
        return

    for i, product in enumerate(products, 1):
        print(f"{i}. {product}")


def advanced_search_menu(system):
    print("\n--- BÚSQUEDA AVANZADA ---")
    print("1. Buscar por Nombre")
    print("2. Buscar por Categoría")
    print("3. Buscar por Precio Exacto")
    print("4. Buscar por Nombre")
    print("5. Buscar por Categoría")
    print("6. Volver")

    option = input("Seleccione opción: ")

    if option == "1":
        name = input("Nombre exacto a buscar: ")
        results = system.binary_search_by_name(name)
        method = "BÚSQUEDA BINARIA"
    elif option == "2":
        category = input("Categoría exacta a buscar: ")
        results = system.binary_search_by_category(category)
        method = "BÚSQUEDA BINARIA"
    elif option == "3":
        try:
            price = float(input("Precio exacto a buscar: "))
            results = system.binary_search_by_price(price)
            method = "BÚSQUEDA BINARIA"
        except ValueError:
            print("Precio inválido")
            return
    elif option == "4":
        name = input("Nombre a buscar: ")
        results = system.search_products_by_name(name)
        method = "BÚSQUEDA SECUENCIAL"
    elif option == "5":
        category = input("Categoría a buscar: ")
        results = system.search_products_by_category(category)
        method = "BÚSQUEDA SECUENCIAL"
    elif option == "6":
        return
    else:
        print("Opción inválida")
        return

    if results:
        print(f"\n Se encontraron {len(results)} productos ({method}):")
        for product in results:
            print(f"   - {product}")
    else:
        print(f"\n No se encontraron productos ({method})")


def register_sale(system):
    print("\n--- REGISTRAR VENTA ---")
    products_to_sell = []
    while True:
        code = input("Código producto (o 'fin'): ").upper()
        if code == 'FIN': break
        product = system.search_product_by_code(code)
        if not product: print("Producto no encontrado"); continue
        print(f"Producto: {product.name} - Stock: {product.quantity}")
        try:
            quantity = int(input("Cantidad: "))
            if quantity <= 0: print("Cantidad debe ser > 0"); continue
            if quantity > product.quantity: print(f"Stock insuficiente. Disponible: {product.quantity}"); continue
            products_to_sell.append((code, quantity))
            print("Producto agregado")
        except ValueError:
            print("Cantidad inválida")
    if not products_to_sell: print("Venta cancelada - sin productos"); return
    # Resumen de venta
    print("\n--- RESUMEN VENTA ---")
    total = 0
    for code, quantity in products_to_sell:
        product = system.search_product_by_code(code)
        subtotal = product.price * quantity
        total += subtotal
        print(f"{product.name} x{quantity} = Q{subtotal:.2f}")
    print(f"TOTAL: Q{total:.2f}")
    if input("¿Confirmar venta? (s/n): ").lower() == 's':
        success, msg = system.create_sale(products_to_sell)
        print(msg)
    else:
        print("Venta cancelada")


def reports_statistics(system):
    print("\n--- REPORTES Y ESTADÍSTICAS ---")
    stats = system.get_sales_statistics()
    print(
        f"Ventas: Total={stats['total_sales']}, Monto=Q{stats['total_amount']:.2f}, Promedio=Q{stats['average_sale']:.2f}")
    print("\n--- PRODUCTOS STOCK BAJO ---")
    low_stock = system.get_low_stock_products(10)
    if low_stock:
        for p in low_stock: print(f"! {p.name} - Stock: {p.quantity}")
    else:
        print("Todo el stock está bien")
    print("\n--- HISTORIAL ACCIONES ---")
    history = system.get_action_history(10)
    if history:
        for i, action in enumerate(reversed(history), 1): print(f"{i}. {action}")
    else:
        print("No hay acciones")


def sales_history(system):
    print("\n--- HISTORIAL VENTAS ---")
    sales = system.list_sales()
    if sales:
        for sale in sales:
            print(f"\n{sale}\nVendedor: {sale.username}\nProductos:")
            for item in sale.products: print(f" - {item['name']} x{item['quantity']} = Q{item['subtotal']:.2f}")
    else:
        print("No hay ventas")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def run_system():
    system = InventorySystem()
    print("\n" + "=" * 60)
    print("     SISTEMA DE GESTIÓN - TIENDA ELECTRÓNICOS")
    print("=" * 60)
    print("Usuarios prueba: admin/admin123 o vendedor/vend123")

    while True:
        if not system.current_user:
            main_menu()
            option = input("\nSeleccione opción: ")
            if option == "1":
                user, pwd = input("Usuario: "), input("Contraseña: ")
                success, msg = system.login(user, pwd)
                print(f"\n{msg}")
            elif option == "2":
                print("\n¡Hasta pronto!")
                break
            else:
                print("\nOpción no válida")
        else:
            if system.current_user.role == "administrador":
                admin_menu(system.current_user)
                option = input("\nSeleccione opción: ")
                ops = [manage_users, register_product, view_inventory, edit_product,
                       delete_product, sort_products_menu, advanced_search_menu,
                       reports_statistics, reports_statistics, reports_statistics,
                       lambda s: s.logout()]
                if 1 <= int(option) <= len(ops):
                    if option == "11":
                        system.logout()
                        print("Sesión cerrada")
                    else:
                        ops[int(option) - 1](system)
                else:
                    print("Opción no válida")
            else:
                employee_menu(system.current_user)
                option = input("\nSeleccione opción: ")
                ops = [view_inventory, search_product, sort_products_menu,
                       advanced_search_menu, register_sale, sales_history,
                       lambda s: s.logout()]
                if 1 <= int(option) <= len(ops):
                    if option == "7":
                        system.logout()
                        print("Sesión cerrada")
                    else:
                        ops[int(option) - 1](system)
                else:
                    print("Opción no válida")


# Iniciar el sistema
run_system()