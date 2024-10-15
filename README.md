
# Little Lemon API

This project is a backend solution for managing a restaurant's menu, orders, and delivery operations. Built with **Django** and **Django REST Framework**, it provides role-based access for customers, managers, and delivery staff.

## Key Features
- **Menu Management**: Add, update, and delete menu items.
- **Order Processing**: Customers can place orders; managers assign them to delivery crew.
- **Delivery Management**: Delivery staff can update order statuses.
- **Role-Based Access**: Different permissions for customers, managers, and delivery crew.

## Installation
1. Clone the repo:  
   `git clone https://github.com/your-username/LittleLemonAPI.git`
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Setup MySQL database and environment variables.
4. Run migrations:  
   `python manage.py migrate`
5. Start the server:  
   `python manage.py runserver`

## API Endpoints (Highlights)

- **Menu**:  
  `GET /menu-items` - View all menu items  
  `GET /menu-items/<int:pk>` - View a specific menu item by ID  
  `POST /menu-items` - Add a new menu item

- **Category**:  
  `GET /category` - View all categories

- **Cart**:  
  `GET /cart` - View the cart  
  `POST /cart` - Add an item to the cart

- **Groups**:  
  `GET /groups/manager/users` - View all manager users  
  `GET /groups/manager/users/<int:pk>` - View a specific manager  
  `GET /groups/delivery-crew/users` - View all delivery crew members  
  `GET /groups/delivery-crew/users/<int:pk>` - View a specific delivery crew member

- **Orders**:  
  `GET /order` - View all orders  
  `GET /order/<int:pk>` - View a specific order by ID  
  `POST /order` - Place a new order

