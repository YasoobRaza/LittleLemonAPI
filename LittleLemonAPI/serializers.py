from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.validators import UniqueTogetherValidator
from .models import *
from .validators import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','groups']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True) 
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2,read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2,read_only=True)
    class Meta:
        model = Cart
        fields = ['user','menuitem','menuitem_id','quantity','unit_price','price']
        extra_kwargs = {
            "quantity":{"min_value":1},
        }
    validators = [
        UniqueTogetherValidator(
            queryset=Cart.objects.all(),
            fields = ["user","menuitem_id"]
        ),
        MenuItemExistsValidator(),
    ]
    def set_unit_price(self,cart:Cart):
        return cart.menuitem.price
    def calculate_price(self,cart:Cart):
        return cart.menuitem.price*cart.quantity
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total = serializers.DecimalField(max_digits=6, decimal_places=2,read_only=True)
    date = serializers.DateField(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(default=None,write_only=True)
    status = serializers.BooleanField()
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','delivery_crew_id','status','total','date']

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if request and not request.user.groups.filter(name="Manager").exists() :
            if request.user.groups.filter(name="Delivery Crew").exists():
                fields.pop('delivery_crew_id')
            else:
                fields.pop('delivery_crew_id')
                fields.pop('status')
        return fields
    
    validators = [
        CartNotEmptyValidator(),
        DeliveryCrewExistsValidator(),
    ]

class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(read_only=True)
    menuitem_id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2,read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2,read_only=True)
    class Meta:
        model = OrderItem
        fields = ['order_id','menuitem_id','quantity','unit_price','price']

