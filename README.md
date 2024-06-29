# Byte Ecommerce
**A Django based ecommerce project**

## Landing Page
![Landing Page](https://raw.githubusercontent.com/OverkillViper/Byte/main/Homepage.png?token=GHSAT0AAAAAACUDZL4DMP3F6HCNYQDRWFZOZUAD7SA)

## Framework
<p align="center">
<img src="https://static.djangoproject.com/img/logos/django-logo-positive.png" alt="drawing" width="120"/>
</p>
<p align="center">
<font size="5">
<b>Djnago</b>
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
![DB Schema](https://raw.githubusercontent.com/OverkillViper/Byte/e9ba2f47995f0bdddfebe9e8d77e32edf61563c0/App%20Design-Page-3.drawio.svg?token=A37FQMMDZCD2GQRRAQ2HGILGQAQDC)

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
