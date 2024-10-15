from typing import Any
from rest_framework.validators import ValidationError
from .models import *

class MenuItemExistsValidator:
    def __call__(self, data):
        menuitem_id = data['menuitem_id']
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            raise ValidationError('This menuitem does not exist.')
        
class CartNotEmptyValidator:
    def __call__(self, data):
        user = data['user']
        cart = Cart.objects.filter(user=user)
        if len(cart)==0:
            raise ValidationError('no items in Cart')
        
class DeliveryCrewExistsValidator:
    def __call__(self,data):
        delivery_crew_id = data['delivery_crew_id']
        user = User.objects.get(id=delivery_crew_id)
        if not user.groups.filter(name="Delivery Crew").exists():
            raise ValidationError('Delivery Crew with given ID does not exists')
