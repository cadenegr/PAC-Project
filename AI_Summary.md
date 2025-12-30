# AI Summary - PAC Project Documentation

**Última Actualización:** 30 de Diciembre, 2025 - **REFACTORIZACIÓN COMPLETA + SCHEMAS DB VERIFICADOS**  
**Lenguaje de Comunicación:** Español (independientemente del idioma del usuario)

---

## ⚠️ REGLAS CRÍTICAS PARA EL ASISTENTE AI

### ANTES DE MODIFICAR CUALQUIER CÓDIGO:
1. **✅ SIEMPRE VERIFICAR** el schema de la base de datos primero
2. **✅ CONSULTAR** este AI_Summary.md para nombres de campos exactos
3. **✅ PREGUNTAR** al usuario si hay duda sobre nombres de campos
4. **❌ NUNCA ASUMIR** nombres de campos sin verificar

### Comandos de Verificación Obligatorios:
```bash
# Ver schema de tabla (USAR ANTES DE PROGRAMAR)
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(materials)'); print([row for row in cursor.fetchall()]); conn.close()"

# Ver datos reales de tabla
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM materials LIMIT 3'); print(cursor.fetchall()); conn.close()"

# Listar todas las tablas
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\"); print([t[0] for t in cursor.fetchall()]); conn.close()"
```

### Proceso de Trabajo:
1. Usuario solicita cambio/nuevo módulo
2. AI responde: "Primero voy a verificar el schema de la DB..."
3. AI ejecuta comando de verificación
4. AI muestra schema al usuario
5. AI pregunta confirmación si hay dudas
6. Solo entonces procede a programar

---

## 🚀 REFACTORIZACIÓN COMPLETADA

### Reducción de Código Duplicado
- **ANTES:** ~2,262 líneas duplicadas en vistas (Materials: 908, Products: 721, Suppliers: 635, Create_Targets: ~800)
- **DESPUÉS:** ~500 líneas de componentes + ~600 líneas totales en vistas
- **ELIMINACIÓN:** 73% del código duplicado
- **VISTAS REFACTORIZADAS:**
  - ✅ Materials: 908 → 95 líneas (89% reducción)
  - ✅ Products: 721 → 80 líneas (89% reducción)
  - ✅ Suppliers: 635 → 80 líneas (87% reducción)
  - ✅ Chapters: ~110 líneas (usando BaseCRUDView desde inicio)
  - ✅ Create_Targets: ~800 → 330 líneas (59% reducción con validaciones custom)
- **BENEFICIO:** Mantenibilidad, escalabilidad, código DRY

### Nueva Arquitectura de Componentes
```
src/
├── components/                      # ✨ NUEVO - Componentes reutilizables
│   ├── __init__.py
│   ├── ui_components.py             # Botones, labels, entries estándar
│   ├── form_builder.py              # Constructor dinámico de formularios
│   └── base_crud_view.py            # Lógica CRUD completa (herencia)
```

---

## 📋 Información del Proyecto

### Objetivo General
Aplicación de gestión empresarial desarrollada en Python con Tkinter, diseñada para uso móvil con arquitectura MVC profesional y componentes reutilizables.

### Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **GUI Framework:** Tkinter (temporal, migración futura a Kivy para móvil)
- **Base de Datos:** SQLite3 (`data/pac.db`)
- **Arquitectura:** MVC + Componentes Reutilizables
- **Patrón:** DRY (Don't Repeat Yourself)
- **SO Desarrollo:** Linux (zsh)

### Estructura del Proyecto
```
/home/dci-student/Desktop/PAC/
├── main.py                          # Punto de entrada
├── config/
│   └── settings.py                  # Configuración centralizada (colores)
├── src/
│   ├── components/                  # ✨ COMPONENTES REUTILIZABLES
│   │   ├── ui_components.py         # Headers, botones, entries, navegación (304 líneas)
│   │   ├── form_builder.py          # Constructor dinámico de formularios (138 líneas)
│   │   └── base_crud_view.py        # Clase base CRUD (toda la lógica) (513 líneas)
│   ├── controllers/
│   │   └── app_controller.py        # Controlador principal
│   ├── models/
│   │   ├── material.py              # ✅ Modelo Material
│   │   ├── product.py               # ✅ Modelo Product
│   │   ├── supplier.py              # ✅ Modelo Supplier
│   │   ├── target.py                # ✅ Modelo Target
│   │   ├── chapter.py               # ✅ Modelo Chapter
│   │   └── ...
│   ├── database/
│   │   ├── material_db.py           # ✅ Servicio DB Materials
│   │   ├── product_db.py            # ✅ Servicio DB Products
│   │   ├── supplier_db.py           # ✅ Servicio DB Suppliers
│   │   ├── target_db.py             # ✅ Servicio DB Targets
│   │   ├── chapter_db.py            # ✅ Servicio DB Chapters
│   │   └── ...
│   └── views/
│       ├── base_view.py             # Clase base abstracta (limpieza)
│       ├── main_menu_view.py        # Menú principal
│       ├── materials_view.py        # ✅ REFACTORIZADO (908→95 líneas)
│       ├── products_view.py         # ✅ REFACTORIZADO (721→80 líneas)
│       ├── suppliers_view.py        # ✅ REFACTORIZADO (635→80 líneas)
│       ├── chapters_view.py         # ✅ REFACTORIZADO (~110 líneas)
│       ├── create_targets_view.py   # ✅ REFACTORIZADO (~800→330 líneas)
│       └── ...
└── data/
    └── pac.db                       # Base de datos SQLite
```

---

## 🎨 Principios de Diseño

### 1. **Mobile-First UI**
- Formularios ocupan todo el ancho de pantalla
- Listas de registros en ventanas emergentes (popups)
- NO usar paneles lado a lado
- Botones grandes con íconos emoji

### 2. **Arquitectura MVC + Componentes Reutilizables**
- **Modelo:** Dataclasses con validaciones y truncado automático
- **Vista:** Clases que heredan de `BaseCRUDView` (solo configuración)
- **Controlador:** `AppController` maneja navegación
- **Componentes:** UIComponents, FormBuilder (reutilizables en TODO el proyecto)
- **Patrón DRY:** Don't Repeat Yourself - código modular y profesional

### 3. **Colores Estandarizados** (en `config/settings.py`)
```python
PRIMARY_COLOR = "#2C3E50"      # Azul oscuro
SECONDARY_COLOR = "#34495E"    # Gris azulado
ACCENT_COLOR = "#3498DB"       # Azul claro
SUCCESS_COLOR = "#27AE60"      # Verde
DANGER_COLOR = "#E74C3C"       # Rojo
WARNING_COLOR = "#F39C12"      # Naranja
INFO_COLOR = "#16A085"         # Turquesa
```

---

## 🧩 COMPONENTES REUTILIZABLES (✨ NUEVO)

### ui_components.py
Componentes UI estandarizados para TODAS las vistas:
- `create_header()` - Encabezado con título
- `create_footer_back_button()` - Botón de regreso
- `create_navigation_buttons()` - ▲🔍▼ navegación
- `create_crud_buttons()` - 💾✏️🗑️🔄 (Guardar, Actualizar, Eliminar, Limpiar)
- `create_status_label()` - Mensajes de estado
- `create_form_label()` - Etiquetas de formulario
- `create_entry()` - Entry estándar con validación
- `create_numeric_entry()` - Entry numérico con formato (1,234.56)
- `create_search_button()` - Botón 🔍 pequeño

### form_builder.py
Constructor dinámico de formularios desde definiciones:
- `build_form()` - Construye formulario completo desde configuración
- `get_values()` - Obtiene todos los valores del formulario
- `set_values()` - Llena formulario desde dict
- `clear_all()` - Limpia todos los campos
- `focus_first()` - Focus en primer campo

**Tipos de campos soportados:**
- `'primary'` - Clave primaria con búsqueda automática
- `'secondary'` - Búsqueda secundaria (nombre)
- `'numeric'` - Numérico con formato (decimals configurable)
- `'text'` - Texto estándar

### base_crud_view.py
Clase base abstracta con TODA la lógica CRUD (herencia):
- Navegación ▲▼ circular con índices
- Auto-búsqueda por clave primaria y secundaria
- Ventana popup con lista completa + búsqueda
- CRUD completo (Create, Read, Update, Delete)
- Validación de campos obligatorios (*)
- Mensajes de estado (éxito, error, advertencia)

**Las subclases SOLO implementan:**
```python
get_title()                    # "Materials Management"
get_field_definitions()        # Lista de campos
get_database()                 # self.db
get_model_class()              # Material
get_primary_key_name()         # 'mat_number'
get_record_by_primary_key()    # db.get_material_by_number()
search_by_secondary_key()      # db.search_by_name()
get_all_records()              # db.get_all_materials()
create_record()                # db.create_material()
update_record()                # db.update_material()
delete_record()                # db.delete_material()
get_list_columns()             # Configuración de columnas popup
```

---

## 📊 Estructura del Menú Principal

### 1. **ABC_Catalog** (Catálogo)
- ✅ **Materials** - Materiales (REFACTORIZADO - 908→95 líneas)
- ✅ **Products** - Productos (REFACTORIZADO - 721→80 líneas)
- ✅ **Suppliers** - Proveedores (REFACTORIZADO - 635→80 líneas)
- ⏳ **Unit_Price** - Precios unitarios (siguiente)
- ⏳ **Teams_Work** - Equipos de trabajo (siguiente)

### 2. **Project** (Proyectos)
- ✅ **Chapters** - Capítulos del proyecto (REFACTORIZADO ~110 líneas)
- ✅ **Create_Targets** - Crear targets con validación (REFACTORIZADO ~330 líneas)
- ⏳ Original_Project (visualizador PDF)
- ⏳ Budget
- ⏳ Change_Orders
- ⏳ Progress_Report

### 3. **Orders** (Pedidos)
- ⏳ Purchase_Orders
- ⏳ Receive_Materials
- ⏳ Order_Status
- ⏳ Vendor_Invoices

### 4. **Payments** (Pagos)
- ⏳ Payment_Schedule
- ⏳ Payment_History

---

## 🗄️ SCHEMAS DE BASES DE DATOS (VERIFICADOS)

### ⚠️ IMPORTANTE: Nombres Exactos de Campos
Los siguientes schemas fueron verificados directamente de la base de datos SQLite.
**NUNCA ASUMIR** nombres de campos - usar estos nombres EXACTOS.

---

### ✅ 1. Materials
**Tabla:** `materials`  
**Verificado:** 30-Dic-2025

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| material_id | INTEGER | PK AUTOINCREMENT | ID único (interno) |
| **raw_part** | TEXT | NOT NULL UNIQUE | ⚠️ Número de parte (PRIMARY KEY lógica) |
| **raw_description** | TEXT | NOT NULL | ⚠️ Descripción del material |
| **raw_unit** | TEXT | NOT NULL | ⚠️ Unidad de medida |
| **raw_price1** | REAL | DEFAULT 0.0 | ⚠️ Precio actual |
| **raw_price2** | REAL | DEFAULT 0.0 | ⚠️ Precio previo |
| **raw_balance** | REAL | DEFAULT 0.0 | ⚠️ Balance calculado |
| raw_in | INTEGER | DEFAULT 0 | Total entradas |
| raw_out | INTEGER | DEFAULT 0 | Total salidas |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha actualización |

**⚠️ ATENCIÓN:** Los campos usan prefijo `raw_` NO `mat_`

**Archivos:**
- Modelo: `src/models/material.py`
- Database: `src/database/material_db.py`
- Vista: `src/views/materials_view.py` (95 líneas)

**Métodos DB Principales:**
- `get_material_by_part(raw_part)` - ⚠️ NO `get_material_by_number`
- `search_by_description(term)` - ⚠️ NO `search_by_name`
- `get_all_materials()`
- `create_material(material)`
- `update_material(material)`
- `delete_material(raw_part)`

---

### ✅ 2. Products
**Tabla:** `products`  
**Verificado:** 30-Dic-2025

| Campo | Tipo | Restricción | Longitud Máx | Descripción |
|-------|------|-------------|--------------|-------------|
| product_id | INTEGER | PK AUTOINCREMENT | - | ID único (interno) |
| **pro_part** | TEXT | NOT NULL UNIQUE | 12 chars | ⚠️ Número de parte (PRIMARY KEY lógica) |
| **pro_description** | TEXT | NOT NULL | 30 chars | ⚠️ Descripción del producto |
| **pro_unit** | TEXT | NOT NULL | 4 chars | ⚠️ Unidad de medida |
| **pro_price1** | REAL | DEFAULT 0.0 | 12 dígitos | ⚠️ Precio 1 |
| **pro_price2** | REAL | DEFAULT 0.0 | 12 dígitos | ⚠️ Precio 2 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha actualización |

**⚠️ ATENCIÓN:** Los campos usan prefijo `pro_` NO `prod_`

**Archivos:**
- Modelo: `src/models/product.py`
- Database: `src/database/product_db.py`
- Vista: `src/views/products_view.py` (80 líneas)

**Métodos DB Principales:**
- `get_product_by_part(pro_part)` - ⚠️ NO `get_product_by_code` o `get_product_by_number`
- `search_by_description(term)` - ⚠️ NO `search_by_name`
- `get_all_products()`
- `create_product(product)`
- `update_product(product)`
- `delete_product(pro_part)`

**Validaciones en Modelo:**
```python
- pro_part: max 12 caracteres (truncado automáticamente)
- pro_description: max 30 caracteres (truncado automáticamente)
- pro_unit: max 4 caracteres (truncado automáticamente)
- pro_price1/price2: >= 0 (no negativos)
```

---

### ✅ 3. Suppliers
**Tabla:** `suppliers`  
**Verificado:** 30-Dic-2025

| Campo | Tipo | Restricción | Longitud Máx | Descripción |
|-------|------|-------------|--------------|-------------|
| supplier_id | INTEGER | PK AUTOINCREMENT | - | ID único (interno) |
| **sup_number** | TEXT | NOT NULL UNIQUE | 12 chars | ⚠️ Número de proveedor (PRIMARY KEY lógica) |
| **sup_name** | TEXT | NOT NULL | 30 chars | ⚠️ Nombre del proveedor |
| sup_address | TEXT | DEFAULT '' | 30 chars | Dirección |
| sup_phone1 | TEXT | DEFAULT '' | 12 chars | Teléfono principal |
| sup_phone2 | TEXT | DEFAULT '' | 12 chars | Teléfono secundario |
| sup_email | TEXT | DEFAULT '' | 30 chars | Correo electrónico |
| sup_paymethod | TEXT | DEFAULT '' | 20 chars | Método de pago |
| sup_username | TEXT | DEFAULT '' | 20 chars | Nombre de usuario |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha actualización |

**⚠️ ATENCIÓN:** Los campos usan prefijo `sup_`

**Archivos:**
- Modelo: `src/models/supplier.py`
- Database: `src/database/supplier_db.py`
- Vista: `src/views/suppliers_view.py` (80 líneas)

**Métodos DB Principales:**
- `get_supplier_by_number(sup_number)`
- `search_by_name(term)`
- `get_all_suppliers()`
- `create_supplier(supplier)`
- `update_supplier(supplier)`
- `delete_supplier(sup_number)`

---

### ✅ 4. Targets
**Tabla:** `targets`  
**Verificado:** 30-Dic-2025

| Campo | Tipo | Restricción | Longitud Máx | Descripción |
|-------|------|-------------|--------------|-------------|
| target_id | INTEGER | PK AUTOINCREMENT | - | ID único (interno) |
| **targ_pronumber** | TEXT | NOT NULL UNIQUE | 12 chars | ⚠️ Número de producto (PRIMARY KEY lógica) |
| **targ_prochapter** | TEXT | NOT NULL | 3 chars | ⚠️ Número de capítulo (FK a chapters) |
| **targ_prodescription** | TEXT | DEFAULT '' | 30 chars | Descripción (copiada de products) |
| **targ_prounit** | TEXT | DEFAULT '' | 4 chars | Unidad (copiada de products) |
| **targ_proprice1** | REAL | DEFAULT 0.0 | 12 dígitos | Precio |
| **targ_qtyproject** | REAL | DEFAULT 0.0 | 12 dígitos | Cantidad proyecto |
| **targ_qtydone** | REAL | DEFAULT 0.0 | 12 dígitos | Cantidad completada |
| **targ_qtyprogress** | REAL | DEFAULT 0.0 | 12 dígitos | Cantidad en progreso |
| **targ_qtyfinish** | REAL | DEFAULT 0.0 | 12 dígitos | Cantidad finalizada |
| **targ_payment** | REAL | DEFAULT 0.0 | 12 dígitos | Pago |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha actualización |

**⚠️ ATENCIÓN:** Los campos usan prefijo `targ_`

**Archivos:**
- Modelo: `src/models/target.py`
- Database: `src/database/target_db.py`
- Vista: `src/views/create_targets_view.py` (330 líneas - con validaciones custom)

**Validaciones Especiales:**
- Antes de crear: validar `targ_prochapter` existe en tabla `chapters`
- Antes de crear: validar `targ_pronumber` existe en tabla `products`
- Auto-llenar `targ_prodescription` y `targ_prounit` desde `products`

**Métodos DB Principales:**
- `get_target_by_number(targ_pronumber)`
- `search_by_description(term)`
- `get_all_targets()`
- `create_target(target)`
- `update_target(target)`
- `delete_target(targ_pronumber)`

---

### ✅ 5. Chapters
**Tabla:** `chapters`  
**Verificado:** 30-Dic-2025

| Campo | Tipo | Restricción | Longitud Máx | Descripción |
|-------|------|-------------|--------------|-------------|
| chapter_id | INTEGER | PK AUTOINCREMENT | - | ID único (interno) |
| **chap_number** | INTEGER | NOT NULL UNIQUE | 0-999 | ⚠️ Número de capítulo (PRIMARY KEY lógica) |
| **chap_description** | TEXT | NOT NULL | 30 chars | ⚠️ Descripción del capítulo |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha actualización |

**⚠️ ATENCIÓN:** 
- `chap_number` es INTEGER (0-999), NO TEXT
- Los campos usan prefijo `chap_`

**Archivos:**
- Modelo: `src/models/chapter.py`
- Database: `src/database/chapter_db.py`
- Vista: `src/views/chapters_view.py` (~110 líneas)

**Métodos DB Principales:**
- `get_chapter_by_number(chap_number)` - Recibe INTEGER
- `search_by_description(term)`
- `get_all_chapters()`
- `create_chapter(chapter)`
- `update_chapter(chapter)`
- `delete_chapter(chap_number)`

---

## 🗄️ Bases de Datos Implementadas (LEGACY - Ver schemas arriba)

### ✅ 1. Materials (Completado)
**Tabla:** `materials`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| material_id | INTEGER | PK AUTOINCREMENT | ID único |
| raw_part | TEXT | NOT NULL UNIQUE | Número de parte (llave primaria) |
| raw_description | TEXT | NOT NULL | Descripción |
| raw_unit | TEXT | NOT NULL | Unidad de medida (texto libre) |
| raw_price1 | REAL | DEFAULT 0.0 | Precio actual |
| raw_price2 | REAL | DEFAULT 0.0 | Precio previo |
| raw_balance | REAL | DEFAULT 0.0 | Balance (calculado) |
| raw_in | INTEGER | DEFAULT 0 | Total entradas |
| raw_out | INTEGER | DEFAULT 0 | Total salidas |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha actualización |

**Archivos:**
- Modelo: `src/models/material.py`
- Database: `src/database/material_db.py`
- Vista: `src/views/materials_view.py`

---

### ✅ 2. Products (Completado)
**Tabla:** `products`

| Campo | Tipo | Restricción | Longitud Máx | Descripción |
|-------|------|-------------|--------------|-------------|
| product_id | INTEGER | PK AUTOINCREMENT | - | ID único |
| pro_part | TEXT | NOT NULL UNIQUE | 12 chars | Número de parte (llave primaria) |
| pro_description | TEXT | NOT NULL | 30 chars | Descripción |
| pro_unit | TEXT | NOT NULL | 4 chars | Unidad de medida |
| pro_price1 | REAL | DEFAULT 0.0 | 12 dígitos | Precio 1 |
| pro_price2 | REAL | DEFAULT 0.0 | 12 dígitos | Precio 2 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha actualización |

**Archivos:**
- Modelo: `src/models/product.py`
- Database: `src/database/product_db.py`
- Vista: `src/views/products_view.py`

**Validaciones en Modelo:**
```python
- pro_part: max 12 caracteres (truncado automáticamente)
- pro_description: max 30 caracteres (truncado automáticamente)
- pro_unit: max 4 caracteres (truncado automáticamente)
- pro_price1/price2: >= 0 (no negativos)
```

---

### ✅ 3. Suppliers (Completado)
**Tabla:** `suppliers`

| Campo | Tipo | Restricción | Longitud Máx | Descripción |
|-------|------|-------------|--------------|-------------|
| supplier_id | INTEGER | PK AUTOINCREMENT | - | ID único |
| sup_number | TEXT | NOT NULL UNIQUE | 12 chars | Número de proveedor (llave primaria) |
| sup_name | TEXT | NOT NULL | 30 chars | Nombre del proveedor |
| sup_address | TEXT | DEFAULT '' | 30 chars | Dirección |
| sup_phone1 | TEXT | DEFAULT '' | 12 chars | Teléfono principal |
| sup_phone2 | TEXT | DEFAULT '' | 12 chars | Teléfono secundario |
| sup_email | TEXT | DEFAULT '' | 30 chars | Correo electrónico |
| sup_paymethod | TEXT | DEFAULT '' | 20 chars | Método de pago |
| sup_username | TEXT | DEFAULT '' | 20 chars | Nombre de usuario |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha creación |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | - | Fecha actualización |

**Archivos:**
- Modelo: `src/models/supplier.py`
- Database: `src/database/supplier_db.py`
- Vista: `src/views/suppliers_view.py`

**Campos con restricción de longitud:**
```python
- Sup.Number: width=12, maxlength=12
- Sup.Name: width=30, maxlength=30
- Sup.Address: width=30, maxlength=30
- Sup.Phone1: width=12, maxlength=12
- Sup.Phone2: width=12, maxlength=12
- Sup.Email: width=30, maxlength=30
- Sup.PayMethod: width=20, maxlength=20
- Sup.UserName: width=20, maxlength=20
```

---

## 🔧 Patrón de Implementación CRUD (✨ REFACTORIZADO)

**NUEVO PATRÓN:** Usar herencia de `BaseCRUDView` - reduce código de 600-900 líneas a 80-110 líneas por vista.

### ⚠️ CHECKLIST OBLIGATORIO ANTES DE PROGRAMAR:

```bash
# PASO 1: Verificar schema EXACTO de la tabla
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(NOMBRE_TABLA)'); print([row for row in cursor.fetchall()]); conn.close()"

# PASO 2: Ver datos de ejemplo
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM NOMBRE_TABLA LIMIT 3'); print(cursor.fetchall()); conn.close()"

# PASO 3: Consultar AI_Summary.md para nombres exactos de métodos DB
```

**❌ NUNCA programar sin ejecutar PASO 1 y PASO 2 primero**

---

### Paso 1: Crear Modelo (`src/models/[nombre].py`)
```python
from dataclasses import dataclass, field

@dataclass
class [Nombre]:
    campo1: str = ""
    campo2: str = ""
    # ...
    
    def __post_init__(self):
        """Truncar campos automáticamente"""
        self.campo1 = self.campo1[:max_length] if self.campo1 else ""
        # ...
    
    def validate(self):
        """Retorna (is_valid, error_message)"""
        if not self.campo1:
            return False, "Campo1 es obligatorio"
        return True, ""
    
    def to_dict(self):
        """Convertir a diccionario para FormBuilder"""
        return {
            'campo1': self.campo1,
            'campo2': self.campo2,
            # ...
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crear instancia desde diccionario"""
        return cls(**data)
```

### Paso 2: Crear Servicio DB (`src/database/[nombre]_db.py`)
```python
import sqlite3
from src.models.[nombre] import [Nombre]

class [Nombre]Database:
    def __init__(self, db_path='data/pac.db'):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """CREATE TABLE IF NOT EXISTS..."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS [tabla] (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campo1 TEXT NOT NULL UNIQUE,
                campo2 TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def create_[nombre](self, obj: [Nombre]):
        """INSERT INTO... RETURN id or None if duplicate"""
        # Implementación con manejo de duplicados
    
    def get_[nombre]_by_[primary_key](self, key):
        """SELECT ... WHERE primary_key = ? RETURN obj or None"""
    
    def search_by_[secondary_key](self, term):
        """SELECT ... WHERE secondary_key LIKE ? RETURN list[obj]"""
    
    def get_all_[nombres](self):
        """SELECT * FROM [tabla] RETURN list[obj]"""
    
    def update_[nombre](self, obj: [Nombre]):
        """UPDATE ... WHERE primary_key = ? RETURN bool"""
    
    def delete_[nombre](self, primary_key):
        """DELETE FROM ... WHERE primary_key = ? RETURN bool"""
```

### Paso 3: Crear Vista Heredando de BaseCRUDView (`src/views/[nombre]_view.py`)
```python
from src.views.base_crud_view import BaseCRUDView
from src.database.[nombre]_db import [Nombre]Database
from src.models.[nombre] import [Nombre]

class [Nombre]View(BaseCRUDView):
    """[Nombre] management view - inherits all CRUD logic from base"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = [Nombre]Database()
    
    def get_title(self):
        return "[Nombre] Management"
    
    def get_field_definitions(self):
        return [
            {'name': 'campo1', 'label': 'Campo 1 *:', 'type': 'primary', 'width': 12, 'maxlength': 12},
            {'name': 'campo2', 'label': 'Campo 2 *:', 'type': 'secondary', 'width': 30, 'maxlength': 30},
            {'name': 'campo3', 'label': 'Campo 3:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'campo4', 'label': 'Campo 4:', 'type': 'text', 'width': 20, 'maxlength': 20}
        ]
    
    def get_database(self):
        return self.db
    
    def get_model_class(self):
        return [Nombre]
    
    def get_primary_key_name(self):
        return 'campo1'  # Primary key field
    
    def get_record_by_primary_key(self, key):
        return self.db.get_[nombre]_by_campo1(key)
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_campo2(value)
    
    def get_all_records(self):
        return self.db.get_all_[nombres]()
    
    def create_record(self, model):
        return self.db.create_[nombre](model)
    
    def update_record(self, model):
        return self.db.update_[nombre](model)
    
    def delete_record(self, primary_key):
        return self.db.delete_[nombre](primary_key)
    
    def get_list_columns(self):
        return [
            ('campo1', 'Label 1', 120),
            ('campo2', 'Label 2', 250),
            ('campo3', 'Label 3', 100)
        ]
```

### Paso 4: Registrar en Controller (`src/controllers/app_controller.py`)
```python
from src.views.[nombre]_view import [Nombre]View

class AppController:
    def show_[nombre]_view(self):
        view = [Nombre]View(self.container, self)
        view.render()
```

**BENEFICIOS DE LA REFACTORIZACIÓN:**
- ✅ Solo 80-110 líneas por vista (vs 600-900 antes)
- ✅ Toda la lógica CRUD en base_crud_view.py (una sola vez)
- ✅ FormBuilder genera formularios dinámicamente
- ✅ UIComponents reutiliza botones, navegación, popups
- ✅ Mantenimiento centralizado (cambio en un lugar afecta todas las vistas)
- ✅ Escalable para 20+ módulos sin duplicación

**⚠️ ERRORES COMUNES A EVITAR:**
1. ❌ Asumir nombres de campos sin verificar DB
   - Ejemplo: Asumir `mat_number` cuando es `raw_part`
   - Ejemplo: Asumir `prod_code` cuando es `pro_part`
2. ❌ No convertir primary_key a string en Treeview
   - Fix aplicado en base_crud_view.py línea 478: `primary_key = str(values[0])`
3. ❌ Olvidar que algunos campos son TEXT aunque parezcan números
   - `raw_part`, `pro_part`, `sup_number` son TEXT en DB
4. ❌ No consultar AI_Summary.md antes de programar
   - Siempre verificar schemas de DB arriba antes de crear vistas

---

## 🎯 Características Comunes en Todas las Vistas CRUD

### 1. **Auto-búsqueda en Campo Clave**
- Al presionar Enter o perder foco en campo principal
- Si existe: cargar datos completos
- Si no existe: mostrar advertencia, preparar para nuevo registro

### 2. **Navegación con Flechas**
- ▲ Registro anterior (circular al final)
- ▼ Siguiente registro (circular al inicio)
- Muestra: "Registro X de Y"

### 3. **Botón Search (🔍)**
- Abre ventana popup con lista completa
- Barra de búsqueda en popup
- Doble clic o selección carga registro en formulario principal
- Cierra popup automáticamente al seleccionar

### 4. **Botones de Acción**
- **💾 Guardar** - Verde (#27AE60) - Crear nuevo
- **✏️ Actualizar** - Naranja (#F39C12) - Modificar existente
- **🗑️ Eliminar** - Rojo (#E74C3C) - Borrar con confirmación
- **🔄 Limpiar** - Gris (#34495E) - Limpiar formulario

### 5. **Status Label**
- Mensajes informativos con colores:
  - ✓ Verde: Éxito
  - ⚠ Naranja: Advertencia
  - 🔍 Turquesa: Info

---

## 📝 Historial de Errores y Correcciones

### Error #1: Nombres de Campos Incorrectos en Materials (30-Dic-2025)
**Problema:** Durante refactorización, se asumieron nombres `mat_number`, `mat_name`, etc.  
**Realidad:** DB usa `raw_part`, `raw_description`, `raw_unit`, `raw_price1`, `raw_price2`, `raw_balance`  
**Error:** `AttributeError: 'Material' object has no attribute 'mat_number'`  
**Corrección:** Verificar schema con PRAGMA, actualizar materials_view.py  
**Lección:** SIEMPRE verificar DB schema antes de asumir nombres

### Error #2: Nombres de Campos Incorrectos en Products (30-Dic-2025)
**Problema:** Refactorización usó `prod_code`, `prod_name`, etc.  
**Realidad:** DB usa `pro_part`, `pro_description`, `pro_unit`, `pro_price1`, `pro_price2`  
**Error:** Search no funcionaba, no se podía ver contenido  
**Corrección:** Actualizar products_view.py con nombres correctos  
**Lección:** NUNCA asumir, SIEMPRE verificar

### Error #3: Treeview Convierte TEXT a INT (30-Dic-2025)
**Problema:** `OverflowError: Python int too large to convert to SQLite INTEGER`  
**Causa:** Treeview convierte valores numéricos '1011' a int, pero `raw_part` es TEXT  
**Corrección:** En base_crud_view.py línea 478: `primary_key = str(values[0])`  
**Lección:** Siempre convertir primary_key a string al obtener de Treeview

### Error #4: Create_Targets No Seguía DRY (30-Dic-2025)
**Problema:** create_targets_view.py tenía ~800 líneas con código duplicado  
**Expectativa:** Debería usar BaseCRUDView como materials/products/suppliers  
**Corrección:** Refactorizado a 330 líneas heredando de BaseCRUDView, override _create_form para validaciones custom  
**Lección:** Incluso vistas con lógica especial deben seguir DRY usando herencia

---

## 📝 Cambios Históricos Importantes (LEGACY)

### Materiales - Historial de Modificaciones
1. ❌ **Eliminado** botón "Nuevo" (redundante con Limpiar)
2. ✅ **Separada** lista en ventana popup (optimización móvil)
3. ✅ **Cambiado** Raw.Unit de Combobox a Entry (texto libre)
4. ✅ **Raw.Balance** en modo readonly (campo calculado)
5. ✅ **Campos con ancho y longitud máxima restringida:**
   - Raw.Part: width=20, maxlength=20
   - Raw.Description: width=50, maxlength=100
   - Raw.Unit: width=10, maxlength=10
   - Raw.Price1: width=12, maxlength=12
   - Raw.Price2: width=12, maxlength=12
   - Raw.Balance: width=12, maxlength=12
   - Raw.IN: width=10, maxlength=10
   - Raw.OUT: width=10, maxlength=10
6. ✅ **Formateo de números con comas y puntos:**
   - Método `_format_number()`: Formatea con comas para miles (1,234.56)
   - Método `_parse_number()`: Parsea removiendo comas para guardar en DB
   - Aplicado en precios y balance

### Products - Implementación Inicial
1. ✅ Validaciones de longitud en modelo
2. ✅ Misma estructura UI que Materials
3. ✅ 5 campos principales (sin Balance, IN, OUT)
4. ✅ **Campos con ancho y longitud máxima restringida:**
   - Pro.Part: width=12, maxlength=12
   - Pro.Description: width=30, maxlength=30
   - Pro.Unit: width=4, maxlength=4
   - Pro.Price1: width=12, maxlength=12
   - Pro.Price2: width=12, maxlength=12
5. ✅ **Formateo de números con comas y puntos:**
   - Método `_format_number()`: Formatea con comas para miles (1,234.56)
   - Método `_parse_number()`: Parsea removiendo comas para guardar en DB
   - Aplicado en: guardar, actualizar, limpiar, poblar formulario

---

## 🚀 Próximos Módulos a Implementar

### Prioridad Alta
1. **Unit_Price** - Precios unitarios
2. **Suppliers** - Proveedores
3. **Teams_Work** - Completar implementación
   - Campos requeridos: Team_Number, Team_Name, Team_Phone_1, Team_Phone_2, Team_email, Team_Wassup, Team_Address, Team_Pay_Method, Team_UserName

### Prioridad Media
4. **Original_Project** - Visualizador PDF para proyectos originales
5. Módulos de Orders y Payments

---

## 💡 Notas para el Asistente AI

### Reglas de Comunicación
- **SIEMPRE** responder en español, incluso si el usuario escribe en inglés
- Ser conciso y directo
- Confirmar acciones con ✅ o ❌

### PROCESO OBLIGATORIO Antes de Programar
1. **VERIFICAR** schema de DB con comando PRAGMA (ver arriba)
2. **CONSULTAR** este AI_Summary.md sección "SCHEMAS DE BASES DE DATOS"
3. **MOSTRAR** schema al usuario
4. **PREGUNTAR** si hay duda sobre implementación
5. **SOLO ENTONCES** proceder a programar

### Al Crear Nueva Base de Datos
1. Seguir el **Patrón de Implementación CRUD** (template arriba)
2. **PRIMERO** verificar si la tabla ya existe en DB
3. Aplicar validaciones de longitud si se especifican
4. Usar nombres consistentes: `[prefijo]_campo`
5. Incluir `created_at` y `updated_at` automáticos
6. Optimizar para móvil: formulario completo, lista en popup
7. Probar con script Python antes de confirmar
8. **ACTUALIZAR** este AI_Summary.md con schema VERIFICADO

### Al Modificar Código Existente
1. **VERIFICAR** nombres de campos en DB primero
2. Usar `multi_replace_string_in_file` para múltiples cambios
3. Incluir 3-5 líneas de contexto en replace
4. No crear archivos MD de resumen (salvo que se solicite)
5. Probar con `python3 main.py` después de cambios
6. Si hay error, verificar stack trace y corregir

### Comandos Útiles (USAR FRECUENTEMENTE)
```bash
# Ejecutar app
cd /home/dci-student/Desktop/PAC && python3 main.py

# Ver todas las tablas
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\"); print([t[0] for t in cursor.fetchall()]); conn.close()"

# Ver schema COMPLETO de tabla (⚠️ USAR ANTES DE PROGRAMAR)
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(TABLA)'); print([row for row in cursor.fetchall()]); conn.close()"

# Ver datos de ejemplo (para confirmar tipos)
python3 -c "import sqlite3; conn = sqlite3.connect('data/pac.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM TABLA LIMIT 3'); print(cursor.fetchall()); conn.close()"
```

### Workflow Ideal
```
Usuario: "Crea formulario de X"
AI: "Primero voy a verificar el schema de la tabla X..."
AI: [ejecuta comando PRAGMA]
AI: [muestra schema al usuario]
AI: "Veo que usa campos: campo1, campo2, campo3. ¿Procedo?"
Usuario: "Sí"
AI: [programa usando nombres EXACTOS verificados]
AI: [prueba con python3 main.py]
AI: "✅ Completado y probado"
```

---

## 📊 Estado Actual del Proyecto

**Módulos Completados:** 5/20+ (Materials, Products, Suppliers, Chapters, Create_Targets)  
**Progreso:** ~25%  
**Última Funcionalidad:** 
- ✅ Refactorización completa de 5 vistas siguiendo DRY
- ✅ Corrección de nombres de campos en Materials y Products
- ✅ Create_Targets con validaciones cross-database
- ✅ Fix de Treeview integer conversion
**Formato Estándar Establecido:** 
- ✅ BaseCRUDView para vistas estándar (~80-110 líneas)
- ✅ Override _create_form para validaciones custom (~330 líneas)
- ✅ Verificación de schemas antes de programar (OBLIGATORIO)
- ✅ Conversion str() en Treeview selections
**Próximo Paso:** Unit_Price o Teams_Work usando BaseCRUDView

---

**FIN DEL RESUMEN**
