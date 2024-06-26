# Byte Ecommerce
**A Django based ecommerce project**

## Features
- Multi-role authentication
- Roles:
  - Customer
  - Seller
  - Moderator

### Authentication
- Register (Email based)
- Login
- Account verification via email
- Reset lost password via email

### Common Role Features
- Nofitications
- Basic Chat System

### Customer Features
- Add product to cart
- Add product to wishlist
- Get notification when wishlisted product re-stocks
- Get notification on product delivery stage change
- Rate product after delivery
- Track orders. View order details
- Chat with seller
- Maintain multiple delivery addresses
- Both Cash on Delivery and Cashless Payment accepted
- Buy product from different seller in same order
- Dashboard:
  - Standing orders
  - Completed orders
  - Total product purchased
  - Total money spent
  - Total Addresses
  - Total Wishlists
  - Percentage of payment method selected
  - Monthly purchases

### Seller Features
- Maintain multiple stores
- Product CRUD
- Add product attributes
- Add multiple images for product
- Set discount on product
- Change order status
- Notified on order placed
- Dashboard:
  - Track order status
  - Total sales
  - Total products
  - Total stores
  - Total Orders
  - Avarage Rating
  - Monthly delivered orders

### Moderator Features
- Can delete product
- Can delete stores
- Maintain registered accounts
- Add or delete category
- Dashboard
  - Total Products
  - Total customers
  - Total Stored
  - Total Seller
  - Total Sales
  - Payments methods
  - Monthly sales
  - Top Stores