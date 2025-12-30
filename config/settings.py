"""
Configuration settings for the PAC application
"""

# Application settings
APP_NAME = "PAC - Menu Application"
APP_VERSION = "1.0.0"

# Window settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
WINDOW_BG_COLOR = "#ECF0F1"  # Gris claro moderno

# Color Scheme - Colores individuales para fácil acceso
PRIMARY_COLOR = "#2C3E50"      # Azul oscuro (botones principales)
SECONDARY_COLOR = "#34495E"    # Gris azulado (botones secundarios)
ACCENT_COLOR = "#3498DB"       # Azul brillante (acentos)
SUCCESS_COLOR = "#27AE60"      # Verde (éxito/confirmación)
DANGER_COLOR = "#E74C3C"       # Rojo (eliminar/cancelar)
WARNING_COLOR = "#F39C12"      # Naranja (advertencias)
INFO_COLOR = "#16A085"         # Turquesa (información)

# Background Colors
FRAME_BG_COLOR = "#FFFFFF"     # Blanco (fondo frames)
HEADER_BG_COLOR = "#2C3E50"    # Azul oscuro (encabezados)

# Text Colors
TEXT_COLOR = "#2C3E50"         # Texto principal
HEADER_TEXT_COLOR = "#FFFFFF"  # Texto encabezados
SUBTITLE_COLOR = "#7F8C8D"     # Subtítulos

# Color scheme - Esquema moderno y profesional (diccionario legacy)
COLORS = {
    "primary": "#2C3E50",           # Azul oscuro elegante
    "primary_hover": "#34495E",      # Azul oscuro más claro
    "secondary": "#3498DB",          # Azul brillante
    "secondary_hover": "#2980B9",    # Azul brillante oscuro
    "success": "#27AE60",            # Verde éxito
    "success_hover": "#229954",      # Verde oscuro
    "danger": "#E74C3C",             # Rojo peligro
    "danger_hover": "#C0392B",       # Rojo oscuro
    "warning": "#F39C12",            # Naranja advertencia
    "info": "#16A085",               # Turquesa información
    "text_dark": "#2C3E50",          # Texto oscuro
    "text_light": "#7F8C8D",         # Texto claro
    "white": "#FFFFFF",              # Blanco puro
    "background": "#ECF0F1",         # Gris muy claro
    "card_bg": "#FFFFFF",            # Fondo de tarjetas
    "input_bg": "#FFFFFF",           # Fondo de inputs
    "input_border": "#BDC3C7",       # Borde de inputs
    "header_bg": "#2C3E50",          # Fondo de encabezados
    "header_text": "#FFFFFF"         # Texto de encabezados
}

# Font settings - Tipografías modernas
FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "subtitle": ("Segoe UI", 18, "bold"),
    "button": ("Segoe UI", 11, "bold"),
    "button_small": ("Segoe UI", 10),
    "text": ("Segoe UI", 10),
    "label": ("Segoe UI", 9),
    "header": ("Segoe UI", 14, "bold")
}

# Button styles - Botones modernos y atractivos
BUTTON_STYLES = {
    "main_menu": {
        "font": FONTS["button"],
        "width": 22,
        "height": 2,
        "bg": COLORS["primary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["primary_hover"],
        "relief": "flat",
        "border": 0,
        "cursor": "hand2"
    },
    "back": {
        "font": FONTS["button_small"],
        "width": 20,
        "height": 2,
        "bg": COLORS["secondary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["secondary_hover"],
        "relief": "flat",
        "border": 0,
        "cursor": "hand2"
    },
    "exit": {
        "font": FONTS["button_small"],
        "width": 20,
        "height": 2,
        "bg": COLORS["danger"],
        "fg": COLORS["white"],
        "activebackground": COLORS["danger_hover"],
        "relief": "flat",
        "border": 0,
        "cursor": "hand2"
    },
    "save": {
        "font": FONTS["button"],
        "width": 15,
        "height": 2,
        "bg": COLORS["success"],
        "fg": COLORS["white"],
        "activebackground": COLORS["success_hover"],
        "relief": "flat",
        "border": 0,
        "cursor": "hand2"
    },
    "cancel": {
        "font": FONTS["button_small"],
        "width": 15,
        "height": 2,
        "bg": COLORS["text_light"],
        "fg": COLORS["white"],
        "activebackground": "#95A5A6",
        "relief": "flat",
        "border": 0,
        "cursor": "hand2"
    },
    "action": {
        "font": FONTS["button_small"],
        "width": 18,
        "height": 2,
        "bg": COLORS["info"],
        "fg": COLORS["white"],
        "activebackground": "#138D75",
        "relief": "flat",
        "border": 0,
        "cursor": "hand2"
    }
}

# Menu items configuration
MENU_ITEMS = [
    {
        "id": "catalog",
        "title": "ABC_Catalog",
        "has_submenu": True
    },
    {
        "id": "project",
        "title": "Project",
        "has_submenu": True
    },
    {
        "id": "orders",
        "title": "Orders",
        "has_submenu": True
    },
    {
        "id": "payments",
        "title": "Payments",
        "has_submenu": True
    },
]

# Submenu items configuration
CATALOG_SUBMENU = [
    {
        "id": "materials",
        "title": "Materials",
        "description": "Manage your materials inventory.\n\n"
                      "Features coming soon:\n"
                      "• View all materials\n"
                      "• Add new materials\n"
                      "• Edit material details\n"
                      "• Track material stock"
    },
    {
        "id": "products",
        "title": "Products",
        "description": "Manage your product catalog.\n\n"
                      "Features:\n"
                      "• View all products\n"
                      "• Add new products\n"
                      "• Edit product information\n"
                      "• Product management"
    },
    {
        "id": "unit_price",
        "title": "Unit_Price",
        "description": "Manage pricing information.\n\n"
                      "Features coming soon:\n"
                      "• View price list\n"
                      "• Update prices\n"
                      "• Price history\n"
                      "• Bulk price updates"
    },
    {
        "id": "teams_work",
        "title": "Teams_Work",
        "has_submenu": True
    },
    {
        "id": "suppliers",
        "title": "Suppliers",
        "description": "Manage supplier information.\n\n"
                      "Features coming soon:\n"
                      "• View suppliers\n"
                      "• Add new suppliers\n"
                      "• Supplier contacts\n"
                      "• Purchase history"
    }
]

# Project submenu items
PROJECT_SUBMENU = [
    {
        "id": "original_project",
        "title": "Original_Project",
        "description": "Manage original project information.\n\n"
                      "Features coming soon:\n"
                      "• View project details\n"
                      "• Edit project information\n"
                      "• Project timeline\n"
                      "• Project resources"
    },
    {
        "id": "chapters",
        "title": "Chapters",
        "description": "Manage project chapters.\n\n"
                      "Features:\n"
                      "• Create chapters\n"
                      "• Edit chapter information\n"
                      "• Delete chapters\n"
                      "• Search and navigate"
    },
    {
        "id": "create_targets",
        "title": "Create_Targets",
        "description": "Create and manage project targets.\n\n"
                      "Features coming soon:\n"
                      "• Define targets\n"
                      "• Set milestones\n"
                      "• Track progress\n"
                      "• Target reports"
    },
    {
        "id": "new_period",
        "title": "New_Period",
        "description": "Manage project periods.\n\n"
                      "Features coming soon:\n"
                      "• Create new period\n"
                      "• Period configuration\n"
                      "• Period reports\n"
                      "• Historical periods"
    },
    {
        "id": "view",
        "title": "View",
        "has_submenu": True
    }
]

# View submenu items (under Project)
VIEW_SUBMENU = [
    {
        "id": "qty_project",
        "title": "Qty Project",
        "description": "View project quantities report"
    },
    {
        "id": "qty_done",
        "title": "Qty Done",
        "description": "View completed quantities report"
    },
    {
        "id": "qty_progress",
        "title": "Qty Progress",
        "description": "View in-progress quantities report"
    },
    {
        "id": "qty_to_finish",
        "title": "Qty to Finish",
        "description": "View remaining quantities report"
    }
]

# Orders submenu items
ORDERS_SUBMENU = [
    {
        "id": "work_orders",
        "title": "Work_Orders",
        "description": "Manage work orders.\n\n"
                      "Features coming soon:\n"
                      "• View work orders\n"
                      "• Create new work order\n"
                      "• Edit work order\n"
                      "• Work order status"
    },
    {
        "id": "purchase_order",
        "title": "Purchase_Order",
        "description": "Manage purchase orders.\n\n"
                      "Features coming soon:\n"
                      "• View purchase orders\n"
                      "• Create purchase order\n"
                      "• Edit purchase order\n"
                      "• Purchase history"
    },
    {
        "id": "pay_work_order",
        "title": "Pay_Work_Order",
        "description": "Process payments for work orders.\n\n"
                      "Features coming soon:\n"
                      "• View pending payments\n"
                      "• Process payment\n"
                      "• Payment history\n"
                      "• Payment receipts"
    },
    {
        "id": "pay_purchase_order",
        "title": "Pay_Purchase_Order",
        "description": "Process payments for purchase orders.\n\n"
                      "Features coming soon:\n"
                      "• View pending payments\n"
                      "• Process payment\n"
                      "• Payment history\n"
                      "• Payment receipts"
    }
]

# Payments submenu items
PAYMENTS_SUBMENU = [
    {
        "id": "pay_work_order",
        "title": "Pay_Work_Order",
        "description": "Process payments for work orders.\n\n"
                      "Features coming soon:\n"
                      "• View pending payments\n"
                      "• Process payment\n"
                      "• Payment history\n"
                      "• Payment receipts\n"
                      "• Payment reports"
    },
    {
        "id": "pay_purchase_order",
        "title": "Pay_Purchase_Order",
        "description": "Process payments for purchase orders.\n\n"
                      "Features coming soon:\n"
                      "• View pending payments\n"
                      "• Process payment\n"
                      "• Payment history\n"
                      "• Payment receipts\n"
                      "• Payment reports"
    }
]

# Teams_Work submenu items
TEAMS_WORK_SUBMENU = [
    {
        "id": "new_team",
        "title": "New",
        "description": "Add a new team to the database"
    },
    {
        "id": "update_team",
        "title": "Update",
        "description": "Update existing team information"
    }
]
