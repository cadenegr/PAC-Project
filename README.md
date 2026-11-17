# PAC – Project Administration and Control

**PAC** helps small businesses and volunteer groups plan a project step by step and keep track of its tasks, materials, people and money.

This repository holds the **first desktop prototype** (Python, Tkinter, SQLite). It was built around a real case: a manager coordinating painters, materials and payments for a large apartment complex. It models:

- **Catalog:** materials, products and services, unit prices, suppliers, work teams
- **Project:** units (project chapters), targets (tasks with unit price and quantity), periods
- **Progress reports:** quantity planned, done, in progress and still to finish
- **Orders and payments:** work orders and purchase orders, and their payments (partly done)

**Status:** early prototype, not for production use. The data model is in place, but some screens are still placeholders.

**Next step:** the prototype showed that managers on site need a phone app that works offline, not a desktop program. PAC will be rebuilt as an offline-first web app (PWA) with shareable project templates (reusable step-by-step plans), self-hostable sync and a shared record of hours and payments.

**Run it:** `python3 main.py` (needs Python 3 and Tkinter).

**License:** [GNU AGPL-3.0](LICENSE)

---

## Español – notas originales

# PAC (Control y Administracion de Projectos)- Menu Application

Aplicación profesional con menú interactivo desarrollada en Python siguiendo arquitectura MVC.
Projectos - cual quier projecto de construcion.
	  - administracion - balance de dinero atra ves de monitoreo.
	  - planeacion - 
	  - monitoreo de pasos.
	  - el projecto de controlar es de llegar un fin.


La Base.  - Monitoreando en tiempo real sobre el projecto.
	  - Y EL CUIDADO DEL DINERO
	  - MATERIAL
	  - PERSONAL.

PERMANENTE alimentacion de datos.
manual o de otra manera.




PAC - Menu


*Directories:
-conceptos: tareas (como pintar una pared)
-precios unitarios (cuanto me cuesta hacer cada uno de esos conceptos)
Projecto:
- el projecto
- define las estapas del projecto principal
	- conceptos. 
*
	  

## 📁 Estructura del Proyecto

```
PAC/
├── main.py                 # Punto de entrada de la aplicación
├── config/                 # Configuración
│   ├── __init__.py
│   └── settings.py        # Configuraciones centralizadas
├── src/                    # Código fuente
│   ├── __init__.py
│   ├── controllers/       # Lógica de negocio
│   │   ├── __init__.py
│   │   └── app_controller.py
│   ├── views/             # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── base_view.py
│   │   ├── main_menu_view.py
│   │   └── detail_view.py
│   ├── models/            # Modelos de datos (para futuras DB)
│   │   └── __init__.py
│   └── utils/             # Utilidades y helpers
│       └── __init__.py
├── tests/                 # Tests unitarios
├── requirements.txt       # Dependencias
└── README.md             # Documentación

```

## 🎨 Arquitectura

**Patrón MVC (Model-View-Controller)**
- **Models**: Preparados para integración con bases de datos
- **Views**: Vistas separadas y reutilizables
- **Controllers**: Lógica de navegación y negocio

## ✨ Características

### Menú Principal
- ABC_Catalog - Gestión de catálogo de productos
- Orders - Gestión de pedidos
- Payments - Gestión de pagos
- Others - Configuraciones y opciones adicionales

### Ventajas de la Arquitectura Actual

✅ **Separación de responsabilidades**
- Configuración centralizada en `config/settings.py`
- Vistas separadas en módulos independientes
- Lógica de negocio en controllers

✅ **Escalabilidad**
- Fácil agregar nuevas secciones
- Preparado para integración con bases de datos
- Estructura modular para crecimiento

✅ **Mantenibilidad**
- Código organizado y fácil de encontrar
- Cada módulo tiene una responsabilidad clara
- Documentación en cada archivo

✅ **Reutilización**
- Vista base para heredar funcionalidad común
- Configuración compartida
- Componentes desacoplados

## 🚀 Cómo Ejecutar

```bash
python3 main.py
```

## 📋 Requisitos

- Python 3.x
- Tkinter (incluido con Python)

Para instalar tkinter en Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

## 🔄 Próximos Pasos

1. **Integración con Base de Datos**
   - Crear modelos en `src/models/`
   - Implementar capa de acceso a datos

2. **Funcionalidades Específicas**
   - CRUD para cada sección
   - Validaciones de datos
   - Reportes y análisis

3. **Migración a Framework Móvil**
   - React Native
   - Flutter
   - Kivy

4. **Testing**
   - Tests unitarios en `tests/`
   - Tests de integración

## 📝 Convenciones de Código

- PEP 8 para estilo de código Python
- Docstrings en todas las clases y funciones
- Nombres descriptivos y en inglés
- Comentarios solo cuando sea necesario

## 🏗️ Principios de Diseño

- **DRY** (Don't Repeat Yourself)
- **SOLID** principles
- **Clean Code**
- **Separation of Concerns**

---

**Versión**: 1.0.0  
**Autor**: PAC Development Team  
**Fecha**: Diciembre 2025

#### Mis notas
Nuevo Flujo de Trabajo:
Cuando me pidas algo:

Te preguntaré si necesito aclaración
Verificaré los archivos/DB primero
Te mostraré el plan antes de ejecutar
Esperaré tu confirmación si hay dudas

1. Usuario pide cambio
2. AI: "Primero voy a verificar..."
3. AI ejecuta PRAGMA
4. AI muestra schema
5. AI pregunta confirmación
6. Solo entonces programa

# Para ver cambios futuros:
git status

# Para ver diferencias:
git diff

# Para hacer nuevos commits:
git add .
git commit -m "Descripción de cambios"

# Para ver historial:
git log --oneline --graph
