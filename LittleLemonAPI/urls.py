from django.urls import path,include
from . import views

urlpatterns = [
    path('menu-items',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),
    path('category',views.CategoriesView.as_view()),
    path('cart',views.CartView.as_view()),
    path('groups/manager/users',views.ManagerGroupView.as_view()),
    path('groups/manager/users/<int:pk>',views.SingleManagerView.as_view()),
    path('groups/delivery-crew/users',views.DeliveryCrewGroupView.as_view()),
    path('groups/delivery-crew/users/<int:pk>',views.SingleDeliveryCrewView.as_view()),
    path('order',views.OrderView.as_view()),
    path('order/<int:pk>',views.SingleOrderView.as_view()),
]
