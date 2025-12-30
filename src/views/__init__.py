"""
Views package initialization
"""

from src.views.base_view import BaseView
from src.views.main_menu_view import MainMenuView
from src.views.detail_view import DetailView
from src.views.catalog_submenu_view import CatalogSubmenuView
from src.views.catalog_item_view import CatalogItemView
from src.views.project_submenu_view import ProjectSubmenuView
from src.views.project_item_view import ProjectItemView
from src.views.orders_submenu_view import OrdersSubmenuView
from src.views.orders_item_view import OrdersItemView
from src.views.payments_submenu_view import PaymentsSubmenuView
from src.views.payments_item_view import PaymentsItemView
from src.views.teams_work_submenu_view import TeamsWorkSubmenuView
from src.views.new_team_view import NewTeamView
from src.views.update_team_view import UpdateTeamView

__all__ = [
    'BaseView', 'MainMenuView', 'DetailView',
    'CatalogSubmenuView', 'CatalogItemView',
    'ProjectSubmenuView', 'ProjectItemView',
    'OrdersSubmenuView', 'OrdersItemView',
    'PaymentsSubmenuView', 'PaymentsItemView',
    'TeamsWorkSubmenuView', 'NewTeamView', 'UpdateTeamView'
]
