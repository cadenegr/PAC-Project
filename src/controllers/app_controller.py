"""
Application Controller
Manages navigation and business logic
"""

from src.views.main_menu_view import MainMenuView
from src.views.detail_view import DetailView
from src.views.catalog_submenu_view import CatalogSubmenuView
from src.views.catalog_item_view import CatalogItemView
from src.views.project_submenu_view import ProjectSubmenuView
from src.views.project_item_view import ProjectItemView
from src.views.view_submenu_view import ViewSubmenuView
from src.views.view_item_view import ViewItemView
from src.views.orders_submenu_view import OrdersSubmenuView
from src.views.orders_item_view import OrdersItemView
from src.views.payments_submenu_view import PaymentsSubmenuView
from src.views.payments_item_view import PaymentsItemView
from src.views.teams_work_submenu_view import TeamsWorkSubmenuView
from src.views.teams_work_form_view import TeamsWorkFormView
from src.views.materials_view import MaterialsView
from src.views.products_view import ProductsView
from src.views.suppliers_view import SuppliersView
from config.settings import MENU_ITEMS


class AppController:
    """Main application controller"""
    
    def __init__(self, container, root):
        """
        Initialize the application controller
        
        Args:
            container: The main container widget
            root: The root Tkinter window
        """
        self.container = container
        self.root = root
        self.current_view = None
    
    def show_main_menu(self):
        """Display the main menu"""
        self.current_view = MainMenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to(self, section_id):
        """
        Navigate to a specific section
        
        Args:
            section_id: ID of the section to navigate to
        """
        # Check if this section has a submenu
        section_data = self._get_section_data(section_id)
        
        if section_data and section_data.get("has_submenu"):
            # Navigate to submenu based on section
            if section_id == "catalog":
                self.show_catalog_submenu()
            elif section_id == "project":
                self.show_project_submenu()
            elif section_id == "orders":
                self.show_orders_submenu()
            elif section_id == "payments":
                self.show_payments_submenu()
        else:
            # Navigate to regular detail view
            self.current_view = DetailView(self.container, self, section_id)
            self.current_view.render()
    
    def _get_section_data(self, section_id):
        """Get section data from configuration"""
        for item in MENU_ITEMS:
            if item["id"] == section_id:
                return item
        return None
    
    # Catalog methods
    def show_catalog_submenu(self):
        """Display the ABC_Catalog submenu"""
        self.current_view = CatalogSubmenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to_catalog_item(self, item_id):
        """Navigate to a specific catalog item"""
        # Check if it's Materials, Products, or Suppliers which have their own special views
        if item_id == "materials":
            self.current_view = MaterialsView(self.container, self)
            self.current_view.render()
        elif item_id == "products":
            self.current_view = ProductsView(self.container, self)
            self.current_view.render()
        elif item_id == "suppliers":
            self.current_view = SuppliersView(self.container, self)
            self.current_view.render()
        else:
            self.current_view = CatalogItemView(self.container, self, item_id)
            self.current_view.render()
    
    # Project methods
    def show_project_submenu(self):
        """Display the Project submenu"""
        self.current_view = ProjectSubmenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to_project_item(self, item_id):
        """Navigate to a specific project item"""
        if item_id == "chapters":
            from src.views.chapters_view import ChaptersView
            self.current_view = ChaptersView(self.container, self)
            self.current_view.render()
        elif item_id == "create_targets":
            from src.views.create_targets_view import CreateTargetsView
            self.current_view = CreateTargetsView(self.container, self)
            self.current_view.render()
        elif item_id == "new_period":
            from src.views.new_period_view import NewPeriodView
            self.current_view = NewPeriodView(self.container, self)
            self.current_view.render()
        elif item_id == "view":
            # View has a submenu
            self.show_view_submenu()
        else:
            self.current_view = ProjectItemView(self.container, self, item_id)
            self.current_view.render()
    
    # View methods (under Project)
    def show_view_submenu(self):
        """Display the View submenu"""
        self.current_view = ViewSubmenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to_view_item(self, item_id):
        """Navigate to a specific view report"""
        self.current_view = ViewItemView(self.container, self, item_id)
        self.current_view.render()
    
    # Orders methods
    def show_orders_submenu(self):
        """Display the Orders submenu"""
        self.current_view = OrdersSubmenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to_orders_item(self, item_id):
        """Navigate to a specific orders item"""
        self.current_view = OrdersItemView(self.container, self, item_id)
        self.current_view.render()
    
    def show_work_order_form(self, mode):
        """Display the Work Order form"""
        from src.views.work_order_form_view import WorkOrderFormView
        self.current_view = WorkOrderFormView(self.container, self, mode)
        self.current_view.render()
    
    def show_work_order_view(self):
        """Display the Work Order view"""
        # TODO: Implement work order view
        pass
    
    # Payments methods
    def show_payments_submenu(self):
        """Display the Payments submenu"""
        self.current_view = PaymentsSubmenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to_payments_item(self, item_id):
        """Navigate to a specific payments item"""
        self.current_view = PaymentsItemView(self.container, self, item_id)
        self.current_view.render()
    
    # Teams_Work methods
    def show_teams_work_submenu(self):
        """Display the Teams_Work submenu"""
        self.current_view = TeamsWorkSubmenuView(self.container, self)
        self.current_view.render()
    
    def navigate_to_teams_work_item(self, item_id):
        """Navigate to a specific teams work item"""
        if item_id == "new_team":
            self.current_view = TeamsWorkFormView(self.container, self, mode="new")
            self.current_view.render()
        elif item_id == "update_team":
            self.current_view = TeamsWorkFormView(self.container, self, mode="update")
            self.current_view.render()
    
    def exit_app(self):
        """Exit the application"""
        self.root.quit()
