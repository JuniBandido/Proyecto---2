# Proyecto 2 de Programacion Avanzada
# Universidad Rafael Landivar
# Tienda de Materiales Electricos

from collections import deque
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import tkinter.simpledialog as simpledialog
import re  # Para validación de NIT


# ESTRUCTURAS DE DATOS - CLASES BASE

class Product:
    def __init__(self, code, name, category, price, quantity, brand="", description=""):
        self._code = code
        self._name = name
        self._category = category
        self._price = price
        self._quantity = quantity
        self._brand = brand
        self._description = description

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
        if amount <= self._quantity:
            self._quantity -= amount
            return True
        return False

    def add_stock(self, amount):
        if amount > 0:
            self._quantity += amount
            return True
        return False

    def __str__(self):
        return f"{self._code} - {self._name} ({self._brand}) - Q{self._price:.2f} - Stock: {self._quantity}"


class User:
    def __init__(self, username, password, role, full_name):
        self._username = username
        self._password = password
        self._role = role
        self._full_name = full_name
        self._active = True

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

    @active.setter
    def active(self, value):
        self._active = value

    @full_name.setter
    def full_name(self, value):
        if value and len(value) > 0:
            self._full_name = value

    def verify_password(self, password):
        return self._password == password

    def change_password(self, old_password, new_password):
        if self.verify_password(old_password):
            self._password = new_password
            return True
        return False

    def __str__(self):
        return f"{self._username} - {self._full_name} ({self._role})"


class Sale:
    def __init__(self, sale_id, username, products, total, nit=""):
        self._sale_id = sale_id
        self._username = username
        self._products = products
        self._total = total
        self._date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._nit = nit

    @property
    def sale_id(self):
        return self._sale_id

    @property
    def username(self):
        return self._username

    @property
    def products(self):
        return self._products.copy()

    @property
    def total(self):
        return self._total

    @property
    def date(self):
        return self._date

    @property
    def nit(self):
        return self._nit

    def __str__(self):
        nit_info = f" - NIT: {self._nit}" if self._nit else ""
        return f"Venta #{self._sale_id} - {self._date} - Q{self._total:.2f}{nit_info}"


class Stack:
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
        return self._items.copy()


class Queue:
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
        return list(self._items)


class InventorySystem:
    def __init__(self):
        self._products = []
        self._users = []
        self._sales = []
        self._sale_counter = 1
        self._action_history = Stack()
        self._pending_tasks = Queue()
        self._current_user = None
        self._initialize_database()
        self._initialize_default_data()

    def _initialize_database(self):
        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    codigo TEXT PRIMARY KEY,
                    nombre TEXT,
                    categoria TEXT,
                    precio REAL,
                    cantidad INTEGER,
                    marca TEXT,
                    descripcion TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS administradores (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    full_name TEXT,
                    active BOOLEAN DEFAULT 1
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    full_name TEXT,
                    active BOOLEAN DEFAULT 1
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    sale_id INTEGER PRIMARY KEY,
                    username TEXT,
                    total REAL,
                    date TEXT,
                    nit TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas_detalles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER,
                    product_code TEXT,
                    product_name TEXT,
                    quantity INTEGER,
                    price REAL,
                    subtotal REAL,
                    FOREIGN KEY (sale_id) REFERENCES ventas(sale_id)
                )
            """)

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error inicializando base de datos: {e}")

    def _load_users_from_db(self):
        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            self._users = []

            cursor.execute("SELECT username, password, full_name, active FROM administradores")
            admins_data = cursor.fetchall()
            for username, password, full_name, active in admins_data:
                user = User(username, password, "administrador", full_name)
                user.active = bool(active)
                self._users.append(user)

            cursor.execute("SELECT username, password, full_name, active FROM empleados")
            empleados_data = cursor.fetchall()
            for username, password, full_name, active in empleados_data:
                user = User(username, password, "dependiente", full_name)
                user.active = bool(active)
                self._users.append(user)

            conn.close()
        except Exception as e:
            print(f"Error cargando usuarios: {e}")

    def _save_user_to_db(self, user):
        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            if user.role == "administrador":
                cursor.execute("""
                    INSERT OR REPLACE INTO administradores (username, password, full_name, active)
                    VALUES (?, ?, ?, ?)
                """, (user.username, user._password, user.full_name, user.active))
            else:
                cursor.execute("""
                    INSERT OR REPLACE INTO empleados (username, password, full_name, active)
                    VALUES (?, ?, ?, ?)
                """, (user.username, user._password, user.full_name, user.active))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error guardando usuario: {e}")
            return False

    def _load_products_from_db(self):
        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            cursor.execute("SELECT codigo, nombre, categoria, precio, cantidad, marca, descripcion FROM productos")
            products_data = cursor.fetchall()

            self._products = []
            for codigo, nombre, categoria, precio, cantidad, marca, descripcion in products_data:
                product = Product(codigo, nombre, categoria, precio, cantidad, marca, descripcion)
                self._products.append(product)

            conn.close()
        except Exception as e:
            print(f"Error cargando productos: {e}")
            self._products = []

    def _load_sales_from_db(self):
        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            cursor.execute("SELECT sale_id, username, total, date, nit FROM ventas")
            sales_data = cursor.fetchall()

            self._sales = []
            for sale_id, username, total, date, nit in sales_data:
                cursor.execute("""
                    SELECT product_code, product_name, quantity, price, subtotal 
                    FROM ventas_detalles WHERE sale_id = ?
                """, (sale_id,))
                details_data = cursor.fetchall()

                products = []
                for product_code, product_name, quantity, price, subtotal in details_data:
                    products.append({
                        'code': product_code,
                        'name': product_name,
                        'quantity': quantity,
                        'price': price,
                        'subtotal': subtotal
                    })

                sale = Sale(sale_id, username, products, total, nit)
                sale._date = date
                self._sales.append(sale)

                if sale_id >= self._sale_counter:
                    self._sale_counter = sale_id + 1

            conn.close()
        except Exception as e:
            print(f"Error cargando ventas: {e}")

    def _validate_nit(self, nit):
        """Valida el formato del NIT guatemalteco"""
        if not nit:
            return False
        # Formato básico: 1234567-8 o 12345678
        pattern = r'^\d{7,8}-?\d?$'
        return bool(re.match(pattern, nit))

    def _initialize_default_data(self):
        self._load_users_from_db()
        self._load_products_from_db()
        self._load_sales_from_db()

        if not self._users:
            admin = User("admin", "admin123", "administrador", "Administrador Principal")
            self._save_user_to_db(admin)

            empleado = User("vendedor", "vend123", "dependiente", "Juan Perez")
            self._save_user_to_db(empleado)

            self._load_users_from_db()

        if not self._products:
            productos_ejemplo = [
                Product("BOMB-LED-9W", "Bombillo LED 9W", "Iluminación", 25.50, 50, "Philips", "Luz día 6500K E27"),
                Product("TUBO-LED-4P", "Tubo LED 4 Pies", "Iluminación", 45.00, 30, "Sylvania", "Blanco frío 18W T8"),
                Product("LAMP-LED-PANEL", "Panel LED 600x600", "Iluminación", 180.00, 15, "Osram",
                        "36W para cielo falso"),
                Product("SPOT-LED-5W", "Spot LED Empotrable", "Iluminación", 32.00, 40, "Technolite", "5W 3000K GU10"),
                Product("TOMA-DOBLE-15A", "Tomacorriente Doble 15A", "Accesorios", 18.75, 100, "Steck",
                        "Blanco polar 250V"),
                Product("APAG-SIMPLE-15A", "Apagador Simple 15A", "Accesorios", 12.50, 80, "Legrand", "Blanco mate"),
                Product("BREAKER-20A", "Breaker 20A 1P", "Accesorios", 45.00, 60, "Square D", "Para tablero principal"),
                Product("CAJA-RECT-4x2", "Caja Rectangular 4x2", "Accesorios", 8.00, 120, "Conductores",
                        "Para apagadores"),
                Product("CABLE-TW-12", "Cable TW Calibre 12", "Cables", 3.50, 500, "Condumex", "75m rollo negro"),
                Product("CABLE-THWN-10", "Cable THWN Calibre 10", "Cables", 5.25, 300, "Camesa", "75m rollo rojo"),
                Product("CABLE-PAR-TRENZ", "Cable Par Trenzado CAT6", "Cables", 1.20, 200, "Belden", "305m caja datos"),
                Product("CABLE-COAX-RG6", "Cable Coaxial RG6", "Cables", 0.85, 150, "Commscope", "Para TV y video"),
                Product("TUBO-EMT-1/2", "Tubo EMT 1/2", "Canalización", 35.00, 80, "Camesa", "3 metros galvanizado"),
                Product("TUBO-PVC-3/4", "Tubo PVC 3/4", "Canalización", 28.50, 70, "Durman", "3 metros schedule 40"),
                Product("DUCTO-FLEX-1/2", "Ducto Flexible 1/2", "Canalización", 15.75, 90, "Electroduct",
                        "Metálico 2 metros"),
                Product("CANALETA-40x20", "Canaleta 40x20mm", "Canalización", 12.00, 110, "Panduit", "PVC blanco 2m"),
                Product("VENT-TECHO-48", "Ventilador de Techo 48", "Ventilación", 450.00, 12, "Hunter",
                        "Madera 5 aspas"),
                Product("VENT-BAÑO-100", "Ventilador de Baño 100CFM", "Ventilación", 185.00, 25, "Broan",
                        "Extractor silencioso"),
                Product("VENT-PEDESTAL-16", "Ventilador Pedestal 16", "Ventilación", 220.00, 18, "Lasko",
                        "3 velocidades"),
                Product("VENT-TUBO-4", "Ventilador de Tubo 4", "Ventilación", 95.00, 30, "S&P", "Para ductos 100CFM"),
                Product("CONEC-HEMBRA-15A", "Conector Hembra 15A", "Conectores", 4.50, 200, "Ideal",
                        "Para cable #12-14"),
                Product("TERMINAL-ANILLO-12", "Terminal Anillo #12", "Conectores", 0.25, 500, "3M",
                        "Estañado para 12-10"),
                Product("CINTA-AISL-NEG", "Cinta Aislante Negra", "Conectores", 12.00, 75, "Scotch", "3/4 x 20m"),
                Product("TAPA-TOMA-BCO", "Tapa para Tomacorriente", "Conectores", 2.00, 300, "Steck",
                        "Blanco seguridad niños"),
                Product("SENS-MOV-PIR", "Sensor de Movimiento PIR", "Automatización", 120.00, 25, "Leviton",
                        "180° interior/exterior"),
                Product("TIMER-DIGI-7D", "Timer Digital 7 Días", "Automatización", 85.00, 20, "Intermatic",
                        "Programable 40A"),
                Product("DIMMER-LED-600W", "Dimmer para LED 600W", "Automatización", 65.00, 35, "Lutron",
                        "Control intensidad"),
                Product("CONTROL-MOTOR", "Control para Motor 1HP", "Automatización", 150.00, 15, "Siemens",
                        "Reversa y protección")
            ]
            for producto in productos_ejemplo:
                self.add_product(producto)

    @property
    def current_user(self):
        return self._current_user

    def login(self, username, password):
        for user in self._users:
            if user.username == username and user.verify_password(password):
                if user.active:
                    self._current_user = user
                    self._action_history.push(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ingresar: {username}")
                    return True, f"Bienvenido {user.full_name}"
                else:
                    return False, "Usuario inactivo"
        return False, "Usuario o contraseña incorrectos"

    def logout(self):
        if self._current_user:
            self._action_history.push(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Cierre de sesion: {self._current_user.username}")
            self._current_user = None

    def add_user(self, user):
        if not self._validate_admin_permission():
            return False, "No tiene permisos"
        if any(u.username == user.username for u in self._users):
            return False, "Usuario ya existe"

        if self._save_user_to_db(user):
            self._users.append(user)
            self._action_history.push(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario creado: {user.username}")
            return True, "Usuario creado exitosamente"
        else:
            return False, "Error al guardar en base de datos"

    def list_users(self):
        return self._users.copy() if self._validate_admin_permission() else []

    def delete_user(self, username):
        if not self._validate_admin_permission():
            return False, "No tiene permisos"
        if username == self._current_user.username:
            return False, "No puede eliminarse a sí mismo"

        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            user_to_delete = None
            for user in self._users:
                if user.username == username:
                    user_to_delete = user
                    break

            if user_to_delete:
                if user_to_delete.role == "administrador":
                    cursor.execute("DELETE FROM administradores WHERE username = ?", (username,))
                else:
                    cursor.execute("DELETE FROM empleados WHERE username = ?", (username,))

                conn.commit()
                conn.close()

                self._users.remove(user_to_delete)
                self._action_history.push(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario eliminado: {username}")
                return True, "Usuario eliminado exitosamente"
            else:
                return False, "Usuario no encontrado"

        except Exception as e:
            return False, f"Error al eliminar usuario: {e}"

    def update_user(self, username, **kwargs):
        if not self._validate_admin_permission():
            return False, "No tiene permisos"

        user_to_update = None
        for user in self._users:
            if user.username == username:
                user_to_update = user
                break

        if not user_to_update:
            return False, "Usuario no encontrado"

        try:
            if 'full_name' in kwargs:
                user_to_update.full_name = kwargs['full_name']
            if 'role' in kwargs:
                user_to_update._role = kwargs['role']
            if 'active' in kwargs:
                user_to_update.active = kwargs['active']

            if self._save_user_to_db(user_to_update):
                self._action_history.push(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario actualizado: {username}")
                return True, "Usuario actualizado exitosamente"
            else:
                return False, "Error al actualizar en base de datos"

        except Exception as e:
            return False, f"Error al actualizar usuario: {e}"

    def change_user_password(self, username, old_password, new_password):
        """Cambia la contraseña de un usuario"""
        if not self._validate_admin_permission():
            return False, "No tiene permisos"

        user_to_update = None
        for user in self._users:
            if user.username == username:
                user_to_update = user
                break

        if not user_to_update:
            return False, "Usuario no encontrado"

        if user_to_update.change_password(old_password, new_password):
            if self._save_user_to_db(user_to_update):
                self._action_history.push(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Contraseña cambiada: {username}")
                return True, "Contraseña cambiada exitosamente"
            else:
                return False, "Error al guardar en base de datos"
        else:
            return False, "Contraseña actual incorrecta"

    def _validate_admin_permission(self):
        return self._current_user and self._current_user.role == "administrador"

    def add_product(self, product):
        if any(p.code == product.code for p in self._products):
            return False, "Código ya existe"

        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO productos (codigo, nombre, categoria, precio, cantidad, marca, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (product.code, product.name, product.category, product.price, product.quantity, product.brand,
                  product.description))
            conn.commit()
            conn.close()

            self._products.append(product)
            if self._current_user:
                self._action_history.push(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Producto agregado: {product.code}")
            return True, "Producto agregado exitosamente"

        except Exception as e:
            return False, f"Error al guardar en base de datos: {e}"

    def search_product_by_name(self, name):

        import sqlite3
        conn = sqlite3.connect("tiendaelect.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT codigo, nombre, categoria, precio, cantidad, marca, descripcion
            FROM productos
            WHERE LOWER(nombre) LIKE ?
        """, (f"%{name.lower()}%",))
        rows = cursor.fetchall()
        conn.close()
        return [Product(*row) for row in rows]

    def search_product_by_code(self, code):
        for product in self._products:
            if product.code == code:
                return product
        return None

    def search_products_sequential(self, key, value):
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
        return self._products.copy()

    def update_product(self, code, **kwargs):
        if not self._validate_admin_permission():
            return False, "No tiene permisos"

        product = self.search_product_by_code(code)
        if not product:
            return False, "Producto no encontrado"

        try:
            if 'name' in kwargs:
                product.name = kwargs['name']
            if 'price' in kwargs:
                product.price = kwargs['price']
            if 'quantity' in kwargs:
                product.quantity = kwargs['quantity']
            if 'brand' in kwargs:
                product._brand = kwargs['brand']
            if 'description' in kwargs:
                product.description = kwargs['description']

            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos 
                SET nombre = ?, categoria = ?, precio = ?, cantidad = ?, marca = ?, descripcion = ?
                WHERE codigo = ?
            """, (product.name, product.category, product.price, product.quantity, product.brand, product.description,
                  code))
            conn.commit()
            conn.close()

            self._action_history.push(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Producto actualizado: {code}")
            return True, "Producto actualizado exitosamente"

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al actualizar en base de datos: {e}"

    def delete_product(self, code):
        if not self._validate_admin_permission():
            return False, "No tiene permisos"

        product = self.search_product_by_code(code)
        if product:
            try:
                conn = sqlite3.connect("tiendaelect.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE codigo = ?", (code,))
                conn.commit()
                conn.close()

                self._products.remove(product)
                self._action_history.push(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Producto eliminado: {code}")
                return True, "Producto eliminado exitosamente"

            except Exception as e:
                return False, f"Error al eliminar de la base de datos: {e}"
        return False, "Producto no encontrado"

    def get_products_by_category(self, category):
        return [p for p in self._products if p.category.lower() == category.lower()]

    def quick_sort_products(self, products=None, key='name'):
        if products is None:
            products = self._products.copy()

        if len(products) <= 1:
            return products

        pivot = products[len(products) // 2]
        pivot_value = getattr(pivot, key)

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

        return self.quick_sort_products(left, key) + middle + self.quick_sort_products(right, key)

    def get_products_sorted_by_name(self):
        return self.quick_sort_products(key='name')

    def get_products_sorted_by_stock(self):
        return self.quick_sort_products(key='quantity')

    def get_products_sorted_by_price(self):
        return self.quick_sort_products(key='price')

    def get_products_sorted_by_category(self):
        sorted_products = self.quick_sort_products(key='category')
        if not sorted_products:
            return []

        current_category = None
        result = []
        for product in sorted_products:
            if product.category != current_category:
                current_category = product.category
                result.append(f"┌─── {current_category.upper()} ───")
            result.append(product)
        return result

    def binary_search_products(self, key, value):
        sorted_products = self.quick_sort_products(key=key)

        low, high = 0, len(sorted_products) - 1
        results = []

        while low <= high:
            mid = (low + high) // 2
            current_product = sorted_products[mid]
            current_value = getattr(current_product, key)

            if current_value == value:
                results.append(current_product)

                left = mid - 1
                while left >= 0 and getattr(sorted_products[left], key) == value:
                    results.append(sorted_products[left])
                    left -= 1

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
        return self.binary_search_products('name', name)

    def binary_search_by_category(self, category):
        return self.binary_search_products('category', category)

    def binary_search_by_price(self, price):
        return self.binary_search_products('price', float(price))

    def search_products_by_name(self, name):
        return self.search_products_sequential('name', name)

    def search_products_by_category(self, category):
        return self.search_products_sequential('category', category)

    def search_products_by_brand(self, brand):
        return self.search_products_sequential('brand', brand)

    def create_sale(self, product_codes_quantities, nit=""):
        if not self._current_user:
            return False, "Debe iniciar sesión"

        # Validar NIT si es requerido
        total_estimated = 0
        for code, quantity in product_codes_quantities:
            product = self.search_product_by_code(code)
            if product:
                total_estimated += product.price * quantity

        if total_estimated > 5000:
            if not nit:
                return False, "Para ventas mayores a Q5000 se requiere NIT"
            if not self._validate_nit(nit):
                return False, "NIT inválido. Formato: 1234567-8 o 12345678"

        # Validar productos y stock
        for code, quantity in product_codes_quantities:
            product = self.search_product_by_code(code)
            if not product:
                return False, f"Producto {code} no encontrado"
            if product.quantity < quantity:
                return False, f"Stock insuficiente para {product.name}"

        # Agregar tarea pendiente para validación
        self._pending_tasks.enqueue(f"Validar venta: {len(product_codes_quantities)} productos")

        # Procesar venta
        sale_products, total = [], 0
        for code, quantity in product_codes_quantities:
            product = self.search_product_by_code(code)
            product.reduce_stock(quantity)
            subtotal = product.price * quantity
            sale_products.append({
                'code': product.code,
                'name': product.name,
                'quantity': quantity,
                'price': product.price,
                'subtotal': subtotal
            })
            total += subtotal

        sale = Sale(self._sale_counter, self._current_user.username, sale_products, total, nit)

        try:
            conn = sqlite3.connect("tiendaelect.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO ventas (sale_id, username, total, date, nit)
                VALUES (?, ?, ?, ?, ?)
            """, (sale.sale_id, sale.username, sale.total, sale.date, sale.nit))

            for product in sale_products:
                cursor.execute("""
                    INSERT INTO ventas_detalles (sale_id, product_code, product_name, quantity, price, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (sale.sale_id, product['code'], product['name'], product['quantity'],
                      product['price'], product['subtotal']))

            for code, quantity in product_codes_quantities:
                cursor.execute("""
                    UPDATE productos SET cantidad = cantidad - ? 
                    WHERE codigo = ?
                """, (quantity, code))

            conn.commit()
            conn.close()

        except Exception as e:
            return False, f"Error al guardar venta en base de datos: {e}"

        self._sales.append(sale)
        self._sale_counter += 1

        # Agregar tareas pendientes
        self._pending_tasks.enqueue(f"Actualizar stock después de venta #{sale.sale_id}")
        self._pending_tasks.enqueue(f"Generar reporte de venta #{sale.sale_id}")

        self._action_history.push(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Venta registrada: #{sale.sale_id}")

        self._load_products_from_db()

        return True, f"Venta registrada exitosamente. Total: Q{total:.2f}"

    def list_sales(self):
        return self._sales.copy()

    def get_sales_by_user(self, username):
        return [s for s in self._sales if s.username == username]

    def get_pending_tasks(self):
        """Obtiene las tareas pendientes"""
        return self._pending_tasks.show_all()

    def process_pending_tasks(self):
        """Procesa todas las tareas pendientes"""
        processed = []
        while not self._pending_tasks.is_empty():
            task = self._pending_tasks.dequeue()
            processed.append(task)
            self._action_history.push(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Tarea procesada: {task}")
        return processed

    def get_total_sales(self):
        return sum(sale.total for sale in self._sales)

    def get_low_stock_products(self, threshold=5):
        return [p for p in self._products if p.quantity <= threshold]

    def get_sales_statistics(self):
        if not self._sales:
            return {'total_sales': 0, 'total_amount': 0, 'average_sale': 0}
        total_amount = self.get_total_sales()
        return {
            'total_sales': len(self._sales),
            'total_amount': total_amount,
            'average_sale': total_amount / len(self._sales)
        }

    def get_action_history(self, limit=10):
        history = self._action_history.show_all()
        return history[-limit:] if len(history) > limit else history


class ElectricalStoreGUI:
    def __init__(self, system):
        self.system = system
        self.root = tk.Tk()
        self.root.title("Materiales Electricos Anghie - Login Page")
        self.root.state("zoomed")
        self.root.configure(bg='gray49')

        self.cart_items = []
        self.current_cart_total = 0.0

        self.setup_styles()
        self.show_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background="#f0f0f0")
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Action.TButton', font=('Arial', 10), padding=10)
        style.configure('Menu.TButton', font=('Arial', 9), padding=8)
        style.configure('Success.TLabel', font=('Arial', 10), foreground='green', background='gray49')
        style.configure('Warning.TLabel', font=('Arial', 10), foreground='orange', background='gray49')
        style.configure('Danger.TLabel', font=('Arial', 10), foreground='red', background='gray49')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()

        # Logo (manejo de error si no existe)
        try:
            self.logo_imagen = tk.PhotoImage(file="LogoYimsaWeb-1.png")
            logo_label = tk.Label(self.root, image=self.logo_imagen)
            logo_label.pack()
        except:
            # Si no hay logo, mostrar título
            title_label = ttk.Label(self.root, text="Materiales Eléctricos Anghie", style='Title.TLabel')
            title_label.pack(pady=20)

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True)

        login_frame = ttk.LabelFrame(main_frame, text="Iniciar Sesión", padding=15)
        login_frame.pack(pady=20)

        ttk.Label(login_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = ttk.Entry(login_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = ttk.Entry(login_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_btn = ttk.Button(login_frame, text="Ingresar", command=self.login, style='Action.TButton')
        login_btn.grid(row=2, column=0, columnspan=2, pady=15)

        test_frame = ttk.Frame(main_frame)
        test_frame.pack(pady=10)
        ttk.Label(test_frame, text="Usuarios prueba: admin/admin123  o  vendedor/vend123", font=('Arial', 9)).pack()

        local_label = tk.Label(text="Oficina: Lotificación San Francisco, Las Pozas. Morales Izabal. Guatemala", bg='gray49')
        local_label.pack(pady=10, padx=10, anchor="w")

        number_label = tk.Label(text="Contacto: 5317-2913", bg='gray49')
        number_label.pack(pady=10, padx=10, anchor="w")

        correo_label = tk.Label(text="Correo: info@inversionesyimsa.com", bg='gray49')
        correo_label.pack(pady=10, padx=10, anchor="w")

        self.username_entry.focus()
        self.password_entry.bind('<Return>', lambda e: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = self.system.login(username, password)
        if success:
            if self.system.current_user.role == "administrador":
                self.show_admin_dashboard()
            else:
                self.show_employee_dashboard()
        else:
            messagebox.showerror("Error", message)

    def show_admin_dashboard(self):
        self.clear_window()

        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill='x')

        ttk.Label(header_frame, text=f"Panel de Administración", style='Title.TLabel').pack(side='left')
        ttk.Label(header_frame, text=f"Usuario: {self.system.current_user.full_name}", style='Subtitle.TLabel').pack(
            side='right')

        logout_btn = ttk.Button(header_frame, text="Cerrar Sesión", command=self.logout, style='Menu.TButton')
        logout_btn.pack(side='right', padx=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.setup_inventory_tab(notebook)
        self.setup_users_tab(notebook)
        self.setup_sales_tab(notebook)
        self.setup_reports_tab(notebook)
        self.setup_search_tab(notebook)

    def show_employee_dashboard(self):
        self.clear_window()

        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill='x')

        ttk.Label(header_frame, text=f"Panel de Vendedor", style='Title.TLabel').pack(side='left')
        ttk.Label(header_frame, text=f"Usuario: {self.system.current_user.full_name}", style='Subtitle.TLabel').pack(
            side='right')

        logout_btn = ttk.Button(header_frame, text="Cerrar Sesión", command=self.logout, style='Menu.TButton')
        logout_btn.pack(side='right', padx=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.setup_inventory_tab(notebook)
        self.setup_sales_tab(notebook)
        self.setup_search_tab(notebook)

    def setup_inventory_tab(self, notebook):
        inventory_frame = ttk.Frame(notebook)
        notebook.add(inventory_frame, text="Inventario")

        controls_frame = ttk.Frame(inventory_frame)
        controls_frame.pack(fill='x', pady=10)

        if self.system.current_user.role == "administrador":
            ttk.Button(controls_frame, text="Agregar Producto", command=self.show_add_product_dialog).pack(side='left',
                                                                                                           padx=5)
            ttk.Button(controls_frame, text="Editar Producto", command=self.show_edit_product_dialog).pack(side='left',
                                                                                                           padx=5)
            ttk.Button(controls_frame, text="Eliminar Producto", command=self.delete_product).pack(side='left', padx=5)

        ttk.Button(controls_frame, text="Ordenar por Nombre", command=self.sort_by_name).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Ordenar por Precio", command=self.sort_by_price).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Ordenar por Stock", command=self.sort_by_stock).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Ordenar por Categoría", command=self.sort_by_category).pack(side='left',
                                                                                                     padx=5)
        ttk.Button(controls_frame, text="Actualizar", command=self.refresh_inventory).pack(side='left', padx=5)

        filter_frame = ttk.Frame(inventory_frame)
        filter_frame.pack(fill='x', pady=5)

        ttk.Label(filter_frame, text="Filtrar por:").pack(side='left', padx=5)
        self.filter_var = tk.StringVar(value="Todos")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                    values=["Todos", "Stock Bajo (<10)", "Stock Crítico (<5)", "Por Categoría"])
        filter_combo.pack(side='left', padx=5)
        filter_combo.bind('<<ComboboxSelected>>', self.apply_inventory_filter)

        self.category_filter_var = tk.StringVar()
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_filter_var, width=15)
        self.category_combo.pack(side='left', padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.apply_inventory_filter)

        self.load_categories()

        tree_frame = ttk.Frame(inventory_frame)
        tree_frame.pack(fill='both', expand=True)

        columns = ('Código', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Marca')
        self.inventory_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)

        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)

        self.inventory_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.refresh_inventory()

    def setup_users_tab(self, notebook):
        if self.system.current_user.role != "administrador":
            return

        users_frame = ttk.Frame(notebook)
        notebook.add(users_frame, text="Usuarios")

        controls_frame = ttk.Frame(users_frame)
        controls_frame.pack(fill='x', pady=10)

        ttk.Button(controls_frame, text="Agregar Usuario", command=self.show_add_user_dialog).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Editar Usuario", command=self.show_edit_user_dialog).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Eliminar Usuario", command=self.delete_user).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Cambiar Contraseña", command=self.show_change_password_dialog).pack(
            side='left', padx=5)
        ttk.Button(controls_frame, text="Actualizar", command=self.refresh_users).pack(side='left', padx=5)

        tree_frame = ttk.Frame(users_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)

        columns = ('Usuario', 'Nombre', 'Rol', 'Estado')
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)

        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.refresh_users()

    def setup_sales_tab(self, notebook):
        sales_frame = ttk.Frame(notebook)
        notebook.add(sales_frame, text="Ventas")

        new_sale_frame = ttk.LabelFrame(sales_frame, text="Nueva Venta", padding=10)
        new_sale_frame.pack(fill='x', pady=10)

        product_frame = ttk.Frame(new_sale_frame)
        product_frame.pack(fill='x', pady=5)

        ttk.Label(product_frame, text="Nombre (Palabra clave):").pack(side='left', padx=5)
        self.sale_code_entry = ttk.Entry(product_frame, width=15)
        self.sale_code_entry.pack(side='left', padx=5)

        ttk.Label(product_frame, text="Cantidad:").pack(side='left', padx=5)
        self.sale_quantity_entry = ttk.Entry(product_frame, width=10)
        self.sale_quantity_entry.pack(side='left', padx=5)

        ttk.Button(product_frame, text="Buscar Producto", command=self.search_product_for_sale).pack(side='left',
                                                                                                     padx=5)
        ttk.Button(product_frame, text="Agregar al Carrito", command=self.add_to_cart).pack(side='left', padx=10)

        self.product_info_label = ttk.Label(product_frame, text="", style='Subtitle.TLabel')
        self.product_info_label.pack(side='left', padx=10)

        cart_frame = ttk.LabelFrame(new_sale_frame, text="Carrito de Compras", padding=10)
        cart_frame.pack(fill='x', pady=5)

        columns = ('Código', 'Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show='headings', height=6)

        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)

        cart_scrollbar = ttk.Scrollbar(cart_frame, orient='vertical', command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)

        self.cart_tree.pack(side='left', fill='both', expand=True)
        cart_scrollbar.pack(side='right', fill='y')

        total_frame = ttk.Frame(new_sale_frame)
        total_frame.pack(fill='x', pady=5)

        self.total_label = ttk.Label(total_frame, text="Total: Q0.00", style='Title.TLabel')
        self.total_label.pack(side='left')

        ttk.Button(total_frame, text="Procesar Venta", command=self.process_sale).pack(side='right', padx=5)
        ttk.Button(total_frame, text="Limpiar Carrito", command=self.clear_cart).pack(side='right', padx=5)
        ttk.Button(total_frame, text="Remover Item", command=self.remove_cart_item).pack(side='right', padx=5)

        history_frame = ttk.LabelFrame(sales_frame, text="Historial de Ventas", padding=10)
        history_frame.pack(fill='both', expand=True, pady=10)

        history_columns = ('ID', 'Fecha', 'Vendedor', 'Total', 'Productos')
        self.sales_history_tree = ttk.Treeview(history_frame, columns=history_columns, show='headings', height=10)

        for col in history_columns:
            self.sales_history_tree.heading(col, text=col)

        history_scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.sales_history_tree.yview)
        self.sales_history_tree.configure(yscrollcommand=history_scrollbar.set)

        self.sales_history_tree.pack(side='left', fill='both', expand=True)
        history_scrollbar.pack(side='right', fill='y')

        self.refresh_sales_history()

    def setup_reports_tab(self, notebook):
        reports_frame = ttk.Frame(notebook)
        notebook.add(reports_frame, text="Reportes")

        stats_frame = ttk.LabelFrame(reports_frame, text="Estadísticas Rápidas", padding=10)
        stats_frame.pack(fill='x', pady=10)

        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x')

        self.stats_labels = {}
        stats_data = [
            ("Total Ventas:", "total_sales"),
            ("Monto Total:", "total_amount"),
            ("Venta Promedio:", "average_sale"),
            ("Productos Stock Bajo:", "low_stock"),
            ("Total Productos:", "total_products"),
            ("Categorías:", "total_categories")
        ]

        for i, (text, key) in enumerate(stats_data):
            ttk.Label(stats_grid, text=text, style='Subtitle.TLabel').grid(
                row=i // 2, column=(i % 2) * 2, sticky='w', padx=10, pady=5)
            self.stats_labels[key] = ttk.Label(stats_grid, text="0", style='Title.TLabel')
            self.stats_labels[key].grid(row=i // 2, column=(i % 2) * 2 + 1, sticky='w', padx=5, pady=5)

        report_buttons_frame = ttk.Frame(stats_frame)
        report_buttons_frame.pack(fill='x', pady=10)

        ttk.Button(report_buttons_frame, text="Actualizar Estadísticas", command=self.update_stats).pack(side='left',
                                                                                                         padx=5)
        ttk.Button(report_buttons_frame, text="Ver Productos Stock Bajo", command=self.show_low_stock).pack(side='left',
                                                                                                            padx=5)
        ttk.Button(report_buttons_frame, text="Ver Historial de Acciones", command=self.show_action_history).pack(
            side='left', padx=5)
        ttk.Button(report_buttons_frame, text="Ver Tareas Pendientes", command=self.show_pending_tasks).pack(
            side='left', padx=5)
        ttk.Button(report_buttons_frame, text="Ver Ventas por Usuario", command=self.show_sales_by_user).pack(
            side='left', padx=5)

        category_frame = ttk.LabelFrame(reports_frame, text="Productos por Categoría", padding=10)
        category_frame.pack(fill='both', expand=True, pady=10)

        columns = ('Categoría', 'Cantidad de Productos', 'Stock Total', 'Valor Total')
        self.category_tree = ttk.Treeview(category_frame, columns=columns, show='headings', height=8)

        for col in columns:
            self.category_tree.heading(col, text=col)
            self.category_tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(category_frame, orient='vertical', command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)

        self.category_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.update_stats()
        self.update_category_report()

    def setup_search_tab(self, notebook):
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Búsqueda de Productos")

        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill='x', pady=10)

        ttk.Label(search_controls, text="Tipo de Búsqueda:").pack(side='left', padx=5)
        self.search_type = ttk.Combobox(search_controls, values=["Nombre", "Categoría", "Marca", "Código", "Precio"])
        self.search_type.pack(side='left', padx=5)
        self.search_type.set("Nombre")

        ttk.Label(search_controls, text="Término:").pack(side='left', padx=5)
        self.search_term = ttk.Entry(search_controls, width=30)
        self.search_term.pack(side='left', padx=5)

        ttk.Button(search_controls, text="Buscar Coincidencia", command=self.perform_search).pack(side='left', padx=10)
        ttk.Button(search_controls, text="Buscar Exacto", command=self.perform_binary_search).pack(side='left', padx=5)

        tree_frame = ttk.Frame(search_frame)
        tree_frame.pack(fill='both', expand=True)

        columns = ('Código', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Marca')
        self.search_results_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.search_results_tree.heading(col, text=col)
            self.search_results_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.search_results_tree.yview)
        self.search_results_tree.configure(yscrollcommand=scrollbar.set)

        self.search_results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    # MÉTODOS DE FUNCIONALIDAD COMPLETOS
    def refresh_inventory(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        products = self.system.list_products()
        for product in products:
            self.inventory_tree.insert('', 'end', values=(
                product.code, product.name, product.category,
                f"Q{product.price:.2f}", product.quantity, product.brand
            ))

    def sort_by_name(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        products = self.system.get_products_sorted_by_name()
        for product in products:
            self.inventory_tree.insert('', 'end', values=(
                product.code, product.name, product.category,
                f"Q{product.price:.2f}", product.quantity, product.brand
            ))

    def sort_by_price(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        products = self.system.get_products_sorted_by_price()
        for product in products:
            self.inventory_tree.insert('', 'end', values=(
                product.code, product.name, product.category,
                f"Q{product.price:.2f}", product.quantity, product.brand
            ))

    def sort_by_stock(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        products = self.system.get_products_sorted_by_stock()
        for product in products:
            self.inventory_tree.insert('', 'end', values=(
                product.code, product.name, product.category,
                f"Q{product.price:.2f}", product.quantity, product.brand
            ))

    def sort_by_category(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        products = self.system.get_products_sorted_by_category()
        for item in products:
            if isinstance(item, str):
                # Es un separador de categoría
                self.inventory_tree.insert('', 'end', values=(item, "", "", "", "", ""))
            else:
                # Es un producto
                self.inventory_tree.insert('', 'end', values=(
                    item.code, item.name, item.category,
                    f"Q{item.price:.2f}", item.quantity, item.brand
                ))

    def load_categories(self):
        products = self.system.list_products()
        categories = sorted(set(product.category for product in products))
        self.category_combo['values'] = ["Todas"] + categories

    def apply_inventory_filter(self, event=None):
        filter_type = self.filter_var.get()
        category = self.category_filter_var.get()

        products = self.system.list_products()
        filtered_products = []

        for product in products:
            if filter_type == "Stock Bajo (<10)" and product.quantity >= 10:
                continue
            elif filter_type == "Stock Crítico (<5)" and product.quantity >= 5:
                continue
            elif filter_type == "Por Categoría" and category != "Todas" and product.category != category:
                continue
            filtered_products.append(product)

        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        for product in filtered_products:
            self.inventory_tree.insert('', 'end', values=(
                product.code, product.name, product.category,
                f"Q{product.price:.2f}", product.quantity, product.brand
            ))

    def show_add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Producto")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()

        fields = [
            ("Código:", "code"),
            ("Nombre:", "name"),
            ("Categoría:", "category"),
            ("Precio:", "price"),
            ("Cantidad:", "quantity"),
            ("Marca:", "brand"),
            ("Descripción:", "description")
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            entries[key] = entry

        def save_product():
            try:
                code = entries['code'].get().strip().upper()
                name = entries['name'].get().strip()
                category = entries['category'].get().strip()
                price_str = entries['price'].get().strip()
                quantity_str = entries['quantity'].get().strip()
                brand = entries['brand'].get().strip()
                description = entries['description'].get().strip()

                # Validaciones
                if not all([code, name, category, price_str, quantity_str]):
                    messagebox.showwarning("Advertencia", "Debe llenar todos los campos obligatorios")
                    return

                try:
                    price = float(price_str)
                    quantity = int(quantity_str)
                    if price < 0 or quantity < 0:
                        raise ValueError("Los valores no pueden ser negativos")
                except ValueError:
                    messagebox.showerror("Error", "Precio y cantidad deben ser números válidos y positivos")
                    return

                product = Product(code, name, category, price, quantity, brand, description)
                success, message = self.system.add_product(product)

                if success:
                    messagebox.showinfo("Éxito", message)
                    self.refresh_inventory()
                    self.load_categories()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)

            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar producto: {str(e)}")

        ttk.Button(dialog, text="Guardar", command=save_product).grid(row=len(fields), column=1, pady=10)

    def show_edit_product_dialog(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return

        item = self.inventory_tree.item(selected[0])
        code = item['values'][0]

        product = self.system.search_product_by_code(code)
        if not product:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Producto")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()

        fields = [
            ("Código:", "code", product.code, True),
            ("Nombre:", "name", product.name, False),
            ("Categoría:", "category", product.category, False),
            ("Precio:", "price", str(product.price), False),
            ("Cantidad:", "quantity", str(product.quantity), False),
            ("Marca:", "brand", product.brand, False),
            ("Descripción:", "description", product.description, False)
        ]

        entries = {}
        for i, (label, key, value, disabled) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog, width=30)
            entry.insert(0, value)
            if disabled:
                entry.config(state='disabled')
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            entries[key] = entry

        def update_product():
            try:
                updates = {}
                if entries['name'].get():
                    updates['name'] = entries['name'].get()
                if entries['category'].get():
                    updates['category'] = entries['category'].get()
                if entries['price'].get():
                    updates['price'] = float(entries['price'].get())
                if entries['quantity'].get():
                    updates['quantity'] = int(entries['quantity'].get())
                if entries['brand'].get():
                    updates['brand'] = entries['brand'].get()
                updates['description'] = entries['description'].get()

                success, message = self.system.update_product(code, **updates)
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.refresh_inventory()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)
            except ValueError as e:
                messagebox.showerror("Error", "Datos inválidos: " + str(e))

        ttk.Button(dialog, text="Actualizar", command=update_product).grid(row=len(fields), column=1, pady=10)

    def delete_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return

        item = self.inventory_tree.item(selected[0])
        code = item['values'][0]
        name = item['values'][1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto {name}?"):
            success, message = self.system.delete_product(code)
            if success:
                messagebox.showinfo("Éxito", message)
                self.refresh_inventory()
                self.load_categories()
            else:
                messagebox.showerror("Error", message)

    def refresh_users(self):
        if hasattr(self, 'users_tree'):
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            users = self.system.list_users()
            for user in users:
                status = "Activo" if user.active else "Inactivo"
                self.users_tree.insert('', 'end', values=(
                    user.username, user.full_name, user.role, status
                ))

    def show_add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Usuario")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        fields = [
            ("Usuario:", "username"),
            ("Contraseña:", "password"),
            ("Nombre Completo:", "full_name"),
            ("Rol:", "role")
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            if key == "role":
                role_combo = ttk.Combobox(dialog, values=["administrador", "dependiente"], width=27)
                role_combo.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                role_combo.set("dependiente")
                entries[key] = role_combo
            elif key == "password":
                entry = ttk.Entry(dialog, width=30, show="*")
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                entries[key] = entry
            else:
                entry = ttk.Entry(dialog, width=30)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                entries[key] = entry

        def save_user():
            try:
                username = entries['username'].get().strip()
                password = entries['password'].get()
                full_name = entries['full_name'].get().strip()
                role = entries['role'].get()

                if not all([username, password, full_name, role]):
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return

                user = User(username, password, role, full_name)
                success, message = self.system.add_user(user)

                if success:
                    messagebox.showinfo("Éxito", message)
                    self.refresh_users()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)

            except Exception as e:
                messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")

        ttk.Button(dialog, text="Guardar", command=save_user).grid(row=len(fields), column=1, pady=10)

    def show_edit_user_dialog(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para editar")
            return

        item = self.users_tree.item(selected[0])
        username = item['values'][0]

        user_to_edit = None
        for user in self.system.list_users():
            if user.username == username:
                user_to_edit = user
                break

        if not user_to_edit:
            messagebox.showerror("Error", "Usuario no encontrado")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Usuario")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        fields = [
            ("Usuario:", "username", user_to_edit.username, True),
            ("Nombre Completo:", "full_name", user_to_edit.full_name, False),
            ("Rol:", "role", user_to_edit.role, False),
            ("Activo:", "active", user_to_edit.active, False)
        ]

        entries = {}
        for i, (label, key, value, disabled) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')

            if key == "role":
                role_combo = ttk.Combobox(dialog, values=["administrador", "dependiente"], width=27)
                role_combo.set(value)
                if disabled:
                    role_combo.config(state='disabled')
                role_combo.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                entries[key] = role_combo
            elif key == "active":
                active_var = tk.BooleanVar(value=value)
                active_check = ttk.Checkbutton(dialog, variable=active_var)
                active_check.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                entries[key] = active_var
            else:
                entry = ttk.Entry(dialog, width=30)
                entry.insert(0, value)
                if disabled:
                    entry.config(state='disabled')
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                entries[key] = entry

        def update_user():
            try:
                updates = {}
                if entries['full_name'].get():
                    updates['full_name'] = entries['full_name'].get()
                if entries['role'].get():
                    updates['role'] = entries['role'].get()
                updates['active'] = entries['active'].get()

                success, message = self.system.update_user(username, **updates)
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.refresh_users()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar usuario: {str(e)}")

        ttk.Button(dialog, text="Actualizar", command=update_user).grid(row=len(fields), column=1, pady=10)

    def show_change_password_dialog(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para cambiar contraseña")
            return

        item = self.users_tree.item(selected[0])
        username = item['values'][0]

        dialog = tk.Toplevel(self.root)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text=f"Cambiar contraseña de {username}").pack(pady=10)

        ttk.Label(dialog, text="Contraseña actual:").pack(pady=5)
        old_password_entry = ttk.Entry(dialog, width=25, show="*")
        old_password_entry.pack(pady=5)

        ttk.Label(dialog, text="Nueva contraseña:").pack(pady=5)
        new_password_entry = ttk.Entry(dialog, width=25, show="*")
        new_password_entry.pack(pady=5)

        def change_password():
            old_password = old_password_entry.get()
            new_password = new_password_entry.get()

            if not old_password or not new_password:
                messagebox.showerror("Error", "Ambas contraseñas son requeridas")
                return

            success, message = self.system.change_user_password(username, old_password, new_password)
            if success:
                messagebox.showinfo("Éxito", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)

        ttk.Button(dialog, text="Cambiar Contraseña", command=change_password).pack(pady=15)

    def delete_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return

        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        full_name = item['values'][1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al usuario {full_name}?"):
            success, message = self.system.delete_user(username)
            if success:
                messagebox.showinfo("Éxito", message)
                self.refresh_users()
            else:
                messagebox.showerror("Error", message)

    def show_search_products_for_sale(self, products):
        dialog = tk.Toplevel(self.root)
        dialog.title("Búsqueda de producto")
        dialog.geometry("900x500")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill="both", expand=True)

        columns = ("Código", "Nombre", "Precio", "Stock", "Marca")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Insertar productos
        for product in products:
            tree.insert("", "end", values=(
                product.code, product.name, f"Q{product.price:.2f}", product.quantity, product.brand
            ))

        def select_product():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            item = tree.item(selected[0])
            values = item["values"]

            # 🔹 Guardar producto seleccionado
            self.selected_product = {
                "code": values[0],
                "name": values[1],
                "price": float(str(values[2]).replace("Q", "")),
                "stock": int(values[3]),
                "brand": values[4]
            }

            # 🔹 Mostrar el código en la entrada de venta (opcional)
            self.sale_code_entry.delete(0, tk.END)
            self.sale_code_entry.insert(0, self.selected_product["code"])

            dialog.destroy()

        ttk.Button(dialog, text="Seleccionar", command=select_product).pack(pady=10)

    def search_product_for_sale(self):
        search_text = self.sale_code_entry.get().strip()
        if not search_text:
            return

        products = self.system.search_products_by_name(search_text)

        if products:
            self.show_search_products_for_sale(products)
        else:
            self.product_info_label.config(text="No se encontraron productos con esa palabra")

    def add_to_cart(self):
        # 🔹 Si hay producto seleccionado, usarlo
        if hasattr(self, "selected_product") and self.selected_product:
            code = self.selected_product["code"].strip().upper()
        else:
            # 🔹 Si no hay selección, usar el campo de código
            code = self.sale_code_entry.get().strip().upper()

        quantity_str = self.sale_quantity_entry.get().strip()

        if not code or not quantity_str:
            messagebox.showwarning("Advertencia", "Ingrese código y cantidad")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        # 🔹 Buscar el producto en la base de datos
        product = self.system.search_product_by_code(code)
        if not product:
            messagebox.showerror("Error", f"Producto '{code}' no encontrado en la base de datos.")
            return

        # 🔹 Validar stock
        if product.quantity < quantity:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {product.quantity}")
            return

        # 🔹 Si ya está en el carrito, actualiza cantidad
        for i, item in enumerate(self.cart_items):
            if item['code'] == code:
                self.cart_items[i]['quantity'] += quantity
                self.cart_items[i]['subtotal'] = self.cart_items[i]['quantity'] * product.price
                break
        else:
            # 🔹 Si no está, agregarlo como nuevo
            self.cart_items.append({
                'code': code,
                'name': product.name,
                'quantity': quantity,
                'price': product.price,
                'subtotal': quantity * product.price
            })

        self.update_cart_display()

        # 🔹 Limpiar campos y selección
        self.sale_code_entry.delete(0, tk.END)
        self.sale_quantity_entry.delete(0, tk.END)
        self.selected_product = None

    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        self.current_cart_total = 0
        for item in self.cart_items:
            self.cart_tree.insert('', 'end', values=(
                item['code'], item['name'], item['quantity'],
                f"Q{item['price']:.2f}", f"Q{item['subtotal']:.2f}"
            ))
            self.current_cart_total += item['subtotal']

        self.total_label.config(text=f"Total: Q{self.current_cart_total:.2f}")

    def remove_cart_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item para remover")
            return

        item_index = self.cart_tree.index(selected[0])
        if 0 <= item_index < len(self.cart_items):
            self.cart_items.pop(item_index)
            self.update_cart_display()

    def clear_cart(self):
        self.cart_items = []
        self.update_cart_display()
        self.sale_code_entry.delete(0, tk.END)
        self.sale_quantity_entry.delete(0, tk.END)
        self.product_info_label.config(text="")

    def process_sale(self):
        if not self.cart_items:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return

        sale_items = [(item['code'], item['quantity']) for item in self.cart_items]

        nit = ""
        if self.current_cart_total > 5000:
            nit = simpledialog.askstring("NIT", "Para ventas mayores a Q5000 ingrese NIT (formato: 1234567-8):")
            if not nit:
                messagebox.showwarning("Advertencia", "Se requiere NIT para ventas mayores a Q5000")
                return

        success, message = self.system.create_sale(sale_items, nit)
        if success:
            messagebox.showinfo("Éxito", message)
            self.clear_cart()
            self.refresh_inventory()
            self.refresh_sales_history()
            self.update_stats()
        else:
            messagebox.showerror("Error", message)

    def refresh_sales_history(self):
        for item in self.sales_history_tree.get_children():
            self.sales_history_tree.delete(item)

        sales = self.system.list_sales()
        for sale in sales:
            products_text = ", ".join([f"{p['name']} x{p['quantity']}" for p in sale.products[:2]])
            if len(sale.products) > 2:
                products_text += f" ... (+{len(sale.products) - 2} más)"

            nit_info = f" - NIT: {sale.nit}" if sale.nit else ""
            self.sales_history_tree.insert('', 'end', values=(
                sale.sale_id, sale.date, sale.username,
                f"Q{sale.total:.2f}{nit_info}", products_text
            ))

    def update_stats(self):
        stats = self.system.get_sales_statistics()
        low_stock = len(self.system.get_low_stock_products(10))
        products = self.system.list_products()
        categories = len(set(product.category for product in products))

        self.stats_labels['total_sales'].config(text=str(stats['total_sales']))
        self.stats_labels['total_amount'].config(text=f"Q{stats['total_amount']:.2f}")
        self.stats_labels['average_sale'].config(text=f"Q{stats['average_sale']:.2f}")
        self.stats_labels['low_stock'].config(text=str(low_stock))
        self.stats_labels['total_products'].config(text=str(len(products)))
        self.stats_labels['total_categories'].config(text=str(categories))

        self.update_category_report()

    def update_category_report(self):
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        products = self.system.list_products()
        categories = {}

        for product in products:
            if product.category not in categories:
                categories[product.category] = {
                    'count': 0,
                    'total_stock': 0,
                    'total_value': 0.0
                }

            categories[product.category]['count'] += 1
            categories[product.category]['total_stock'] += product.quantity
            categories[product.category]['total_value'] += product.price * product.quantity

        for category, data in categories.items():
            self.category_tree.insert('', 'end', values=(
                category,
                data['count'],
                data['total_stock'],
                f"Q{data['total_value']:.2f}"
            ))

    def show_low_stock(self):
        low_stock = self.system.get_low_stock_products(10)

        dialog = tk.Toplevel(self.root)
        dialog.title("Productos con Stock Bajo (<10 unidades)")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()

        if not low_stock:
            ttk.Label(dialog, text="No hay productos con stock bajo", style='Subtitle.TLabel').pack(pady=20)
            return

        columns = ('Código', 'Nombre', 'Categoría', 'Stock Actual', 'Precio')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for product in low_stock:
            stock_style = "!STOCK CRÍTICO!" if product.quantity < 5 else "Stock Bajo"
            tree.insert('', 'end', values=(
                product.code,
                product.name,
                product.category,
                f"{product.quantity} ({stock_style})",
                f"Q{product.price:.2f}"
            ))

        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

    def show_action_history(self):
        history = self.system.get_action_history(20)

        dialog = tk.Toplevel(self.root)
        dialog.title("Historial de Acciones (Últimas 20)")
        dialog.geometry("700x400")
        dialog.transient(self.root)
        dialog.grab_set()

        if not history:
            ttk.Label(dialog, text="No hay acciones en el historial", style='Subtitle.TLabel').pack(pady=20)
            return

        columns = ('#', 'Acción', 'Timestamp')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for i, action in enumerate(reversed(history), 1):
            if " - " in action:
                parts = action.split(" - ", 1)
                action_text = parts[1] if len(parts) > 1 else action
                timestamp = parts[0] if len(parts) > 1 else "N/A"
            else:
                action_text = action
                timestamp = "N/A"

            tree.insert('', 'end', values=(
                i,
                action_text,
                timestamp
            ))

        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

    def show_pending_tasks(self):
        tasks = self.system.get_pending_tasks()

        dialog = tk.Toplevel(self.root)
        dialog.title("Tareas Pendientes")
        dialog.geometry("600x300")
        dialog.transient(self.root)
        dialog.grab_set()

        if not tasks:
            ttk.Label(dialog, text="No hay tareas pendientes", style='Subtitle.TLabel').pack(pady=20)
            return

        columns = ('#', 'Tarea')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=250)

        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for i, task in enumerate(tasks, 1):
            tree.insert('', 'end', values=(i, task))

        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

        def process_tasks():
            processed = self.system.process_pending_tasks()
            messagebox.showinfo("Éxito", f"Tareas procesadas: {len(processed)}")
            dialog.destroy()

        ttk.Button(dialog, text="Procesar Tareas", command=process_tasks).pack(pady=10)

    def show_sales_by_user(self):
        """Muestra ventas agrupadas por usuario"""
        users = self.system.list_users()

        dialog = tk.Toplevel(self.root)
        dialog.title("Ventas por Usuario")
        dialog.geometry("700x500")
        dialog.transient(self.root)
        dialog.grab_set()

        if not users:
            ttk.Label(dialog, text="No hay usuarios registrados", style='Subtitle.TLabel').pack(pady=20)
            return

        columns = ('Usuario', 'Nombre', 'Total Ventas', 'Monto Total')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for user in users:
            user_sales = self.system.get_sales_by_user(user.username)
            total_sales = len(user_sales)
            total_amount = sum(sale.total for sale in user_sales)

            tree.insert('', 'end', values=(
                user.username,
                user.full_name,
                total_sales,
                f"Q{total_amount:.2f}"
            ))

        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

    def perform_search(self):
        search_type = self.search_type.get()
        term = self.search_term.get()

        if not term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return

        results = []
        if search_type == "Nombre":
            results = self.system.search_products_by_name(term)
        elif search_type == "Categoría":
            results = self.system.search_products_by_category(term)
        elif search_type == "Marca":
            results = self.system.search_products_by_brand(term)
        elif search_type == "Código":
            product = self.system.search_product_by_code(term.upper())
            if product:
                results = [product]

        self.display_search_results(results, f"Búsqueda Secuencial por {search_type}")

    def perform_binary_search(self):
        search_type = self.search_type.get()
        term = self.search_term.get()

        if not term:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return

        results = []
        if search_type == "Nombre":
            results = self.system.binary_search_by_name(term)
        elif search_type == "Categoría":
            results = self.system.binary_search_by_category(term)
        elif search_type == "Precio":
            try:
                price = float(term)
                results = self.system.binary_search_by_price(price)
            except ValueError:
                messagebox.showerror("Error", "Precio inválido")
                return

        self.display_search_results(results, f"Búsqueda Binaria por {search_type}")

    def display_search_results(self, results, search_method):
        for item in self.search_results_tree.get_children():
            self.search_results_tree.delete(item)

        if results:
            messagebox.showinfo("Resultados", f"Se encontraron {len(results)} productos")
        else:
            messagebox.showinfo("Resultados", "No se encontraron productos")

    def logout(self):
        self.system.logout()
        self.show_login_screen()

    def run(self):
        self.root.mainloop()


def run_system():
    system = InventorySystem()
    app = ElectricalStoreGUI(system)
    app.run()


if __name__ == "__main__":
    run_system()