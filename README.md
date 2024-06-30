# Byte Ecommerce
**A Django based ecommerce project**

## Landing Page
![Homepage](https://github.com/OverkillViper/Byte/assets/117332017/d2a5909b-cfb2-4f2b-a735-8e691f0600f0)

## Framework
<p align="center">
<img src="https://static.djangoproject.com/img/logos/django-logo-positive.png" alt="drawing" width="120"/>
</p>
<p align="center">
<font size="5">
<b>Django</b>
</font>
</p>

## Features
✅ Multi-role authentication <br>
✅ Roles:

| Customer | Seller | Moderator |
|----------|--------|-----------|

<details>
  <summary><b>Authentication</b></summary>
  ✅ Register (Email based)
  <br>✅ Login
  <br>✅ Account verification via email
  <br>✅ Reset lost password via email
</details>

<details>
  <summary><b>Common Role Features</b></summary>
  ✅ Nofitications
  <br>✅ Basic Chat System
</details>

<details>
  <summary><b>Customer Features</b></summary>
  ✅ Add product to cart
  <br>✅ Add product to wishlist
  <br>✅ Get notification when wishlisted product re-stocks
  <br>✅ Get notification on product delivery stage change
  <br>✅ Rate product after delivery
  <br>✅ Track orders. View order details
  <br>✅ Chat with seller
  <br>✅ Maintain multiple delivery addresses
  <br>✅ Both Cash on Delivery and Cashless Payment accepted
  <br>✅ Buy product from different seller in same order
  <br>✅ <b>Dashboard:</b>
  <br>&nbsp&nbsp&nbsp&nbsp✅ Standing orders
  <br>&nbsp&nbsp&nbsp&nbsp✅ Completed orders
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total product purchased
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total money spent
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Addresses
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Wishlists
  <br>&nbsp&nbsp&nbsp&nbsp✅ Percentage of payment method selected
  <br>&nbsp&nbsp&nbsp&nbsp✅ Monthly purchases
</details>

<details>
  <summary><b>Seller Features</b></summary>
  ✅ Maintain multiple stores
  <br>✅ Add product to wishlist
  <br>✅ Product CRUD
  <br>✅ Add product attributes
  <br>✅ Add multiple images for product
  <br>✅ Set discount on product
  <br>✅ Change order status
  <br>✅ Notified on order placed
  <br>✅ <b>Dashboard:</b>
  <br>&nbsp&nbsp&nbsp&nbsp✅ Track order status
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total sales
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total products
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total stores
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Orders
  <br>&nbsp&nbsp&nbsp&nbsp✅ Avarage Rating
  <br>&nbsp&nbsp&nbsp&nbsp✅ Monthly delivered orders
</details>

<details>
  <summary><b>Moderator Features</b></summary>
  ✅ Can delete product
  <br>✅ Can delete stores
  <br>✅ Maintain registered accounts
  <br>✅ Add or delete category
  <br>✅ <b>Dashboard:</b>
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Products
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total customers
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Stored
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Seller
  <br>&nbsp&nbsp&nbsp&nbsp✅ Total Sales
  <br>&nbsp&nbsp&nbsp&nbsp✅ Payments methods
  <br>&nbsp&nbsp&nbsp&nbsp✅ Monthly sales
  <br>&nbsp&nbsp&nbsp&nbsp✅ Top Stores
</details>

## Database Schema
![db sCHEMA](https://github.com/OverkillViper/Byte/assets/117332017/51d738dc-4451-4a0d-8c73-2f7e9d144961)

## Installation
```shell
cd project
```
Install virtual enviroment
```shell
pip install -r requirements.txt
```
Start virtual environment
```shell
..\venv\Scripts\activate
```
Start Server
```shell
python manage.py runserver 0.0.0.0:8000
```
