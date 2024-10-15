from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated,OR
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.response import Response
from rest_framework.request import Request
from .models import *
from .serializers import *
from .permissions import *
# Create your views here.

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price"]
    filterset_fields = ["price"]
    search_fields = ["title","category__title"]

    def get_permissions(self):
        if self.request.method =='GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsAuthenticated(),IsManager()]
        else:
            return []
        
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method =='GET':
            return [IsAuthenticated()]
        elif self.request.method in ['PUT','DELETE','PATCH']:
            return [IsAuthenticated(),IsManager()]
        else:
            return []

class CategoriesView(generics.ListCreateAPIView):
    queryset= Category.objects.all()
    serializer_class = CategorySerializer

class ManagerGroupView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups=Group.objects.get(name='Manager'))
    serializer_class =UserSerializer
    
    def create(self,request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username = username)
            manager_group = Group.objects.get(name='Manager')
            user.groups.add(manager_group)
            user.save()
            return Response({"message":f"user {username} added to Managers group "},status.HTTP_200_OK)
        
        return  Response({"message":"Error"},status.HTTP_400_BAD_REQUEST)

class SingleManagerView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups=Group.objects.get(name='Manager'))
    serializer_class =UserSerializer

    def destroy(self, request, *args, **kwargs):
        id = kwargs['pk']
        if id:
            user = get_object_or_404(User,id = id)
            Manager_group = Group.objects.get(name='Manager')
            user.groups.remove(Manager_group)
            user.save()
            return Response({"message":f"user {user.username} removed from Manager group "},status.HTTP_200_OK)
        return  Response({"message":"Error"},status.HTTP_400_BAD_REQUEST)

class DeliveryCrewGroupView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups=Group.objects.get(name='Delivery Crew'))
    serializer_class =UserSerializer
    
    def create(self,request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username = username)
            deliverycrew_group = Group.objects.get(name='Delivery Crew')
            user.groups.add(deliverycrew_group)
            user.save()
            return Response({"message":f"user {username} added to Delivery Crew group "},status.HTTP_200_OK)
        return  Response({"message":"Error"},status.HTTP_400_BAD_REQUEST)

class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups=Group.objects.get(name='Delivery Crew'))
    serializer_class =UserSerializer

    def destroy(self, request, *args, **kwargs):
        id = kwargs['pk']
        if id:
            user = get_object_or_404(User,id = id)
            deliverycrew_group = Group.objects.get(name='Delivery Crew')
            user.groups.remove(deliverycrew_group)
            user.save()
            return Response({"message":f"user {user.username} removed from Delivery Crew group "},status.HTTP_200_OK)
        return  Response({"message":"Error"},status.HTTP_400_BAD_REQUEST)

        


class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    # lookup_field = 
    def get_queryset(self):
        queryset = Cart.objects.filter(user = self.request.user) 
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = int(self.request.data['quantity'])
        menuitem_id =self.request.data['menuitem_id']
        item = MenuItem.objects.get(id=menuitem_id)
        unit_price = float(item.price)
        price = item.price*quantity
        serializer.save(unit_price=unit_price,price=price)
        return Response({"message":"Item added to cart"},status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # Get all cart objects for the current user and delete them
        Cart.objects.filter(user=request.user).delete()
        return Response({"message":"cart cleared"},status.HTTP_204_NO_CONTENT)
    
class OrderView(generics.ListCreateAPIView):
    ordering_fields = ["date"]
    filterset_fields = ["user"]
    search_fields = ["user__username","delivery_crew__username"]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        user=self.request.user
        cart_items = Cart.objects.filter(user=self.request.user)
        order = Order.objects.create(user=user, status=False, total=0,date=datetime.now())
        total=0
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
            total+=item.price
        order.total = total
        order.save()
        cart_items.delete()
        return Response({"message":"order has been placed"},status.HTTP_201_CREATED)
    
class SingleOrderView(generics.ListAPIView,generics.RetrieveUpdateDestroyAPIView):
    order_fields = ["prices"]
    def get_permissions(self):
        if self.request.method =='GET':
            return [IsAuthenticated()]
        elif self.request.method in ['PUT','PATCH']:
            return [IsAuthenticated(),OR(IsManager(),IsDeliveryCrew())]
        elif self.request.method =='DELETE':
            return [IsAuthenticated(),IsManager()]
        else:
            return []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderItemSerializer
        elif self.request.method in ['PUT','PATCH','DELETE']:
            return OrderSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        queryset = OrderItem.objects.filter(order_id=id)
        return queryset
        
    def update(self, request, *args, **kwargs):
        
        order_id = self.kwargs['pk']
        crew_id = int(self.request.data['delivery_crew_id'])
        order_status = bool(self.request.data.get('status'))
        order = Order.objects.get(id=order_id)
        if crew_id:
            order.delivery_crew =User.objects.get(id=crew_id)
        if order_status:
            order.status=order_status
        else:
            order.status=False 
        order.save()
        return Response({"message":"order has been placed"},status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response({"message":"order has been deleted"},status.HTTP_204_NO_CONTENT)


        
        
        


    

    