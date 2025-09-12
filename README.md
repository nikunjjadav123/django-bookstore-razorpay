# 📚 Django Bookstore with Razorpay Integration  

A simple online **Book Shop** built with **Django** where users can browse and purchase books.  
The project integrates **Razorpay Payment Gateway** to support **UPI, Card, and Netbanking payments**.  

---

## 🚀 Features  
- This is just simpl project to clear concept of payment  
- Direct Checkout functionality  
- Secure checkout with Razorpay  
- Payment support ( only UPI)  
- Django Admin panel to manage books & orders & payments 

---

## 🛠️ Tech Stack  
- **Backend:** Django, Python  
- **Database:** PostgreSQL  
- **Payment Gateway:** Razorpay API  
- **Frontend:** HTML, CSS, Bootstrap  
- **Other:** Django ORM, Razorpay Python SDK  

---

## 📂 Installation  

### 1️⃣ Clone the repo  
```bash
git clone https://github.com/your-username/django-bookstore-razorpay.git
cd django-bookstore-razorpay
python -m venv venv  (Create virtual environment)
venv\Scripts\activate  (Activate virtual environment)
pip install -r requirements.txt (I’ve added a requirements.txt file, so you can install all dependencies for this project)
python manage.py migrate (Migrate all Book,Order,Order Items , Payment Tables)
python manage.py createsuperuser ( Create Super User )
RAZORPAY_KEY_ID=your_key_id ( Put your Razorpay Key )
RAZORPAY_KEY_SECRET=your_key_secret ( Put your Razorpay Secret )
python manage.py runserver ( Run Server )

