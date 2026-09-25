import os
import subprocess
from google.cloud import firestore
from google.oauth2.credentials import Credentials

PROJECT_ID = "qwiklabs-gcp-02-eb01df7117c0"

def get_db():
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
        creds = Credentials(token)
        return firestore.Client(project=PROJECT_ID, credentials=creds)
    except Exception:
        return firestore.Client(project=PROJECT_ID)

def seed_database():
    db = get_db()
    print(f"Connected to Firestore project: {PROJECT_ID}")

    products = [
        {
            "id": "KKW-101",
            "name": "Festive Silk Ethnic Lehenga Choli Set",
            "category": "Girls",
            "price": 49.99,
            "sizes": ["2Y", "3Y", "4Y", "5Y", "6Y", "7Y-8Y"],
            "age_group": "2-8 Years",
            "in_stock": True,
            "stock_quantity": 15,
            "description": "Handcrafted premium silk lehenga choli set with intricate embroidery, perfect for celebrations and festive occasions.",
            "image_url": "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/lehenga.jpg"
        },
        {
            "id": "KKW-102",
            "name": "Dapper Royal Silk Kurta Pyjama with Waistcoat",
            "category": "Boys",
            "price": 44.99,
            "sizes": ["2Y", "3Y", "4Y", "5Y", "6Y", "7Y-8Y"],
            "age_group": "2-8 Years",
            "in_stock": True,
            "stock_quantity": 20,
            "description": "Traditional royal silk kurta pyjama styled with a brocade waistcoat for little gents.",
            "image_url": "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/kurta.jpg"
        },
        {
            "id": "KKW-103",
            "name": "Organic Soft Cotton Pastel Onesie Set (3-Pack)",
            "category": "Toddlers",
            "price": 24.99,
            "sizes": ["0-3M", "3-6M", "6-12M", "12-18M"],
            "age_group": "0-18 Months",
            "in_stock": True,
            "stock_quantity": 30,
            "description": "100% GOTS certified organic cotton onesies in gentle pastel shades for sensitive baby skin.",
            "image_url": "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/onesie.jpg"
        },
        {
            "id": "KKW-104",
            "name": "Breezy Summer Floral Cotton Party Dress",
            "category": "Girls",
            "price": 34.99,
            "sizes": ["2Y", "3Y", "4Y", "5Y", "6Y"],
            "age_group": "2-6 Years",
            "in_stock": True,
            "stock_quantity": 18,
            "description": "Lightweight breathable cotton dress featuring hand-printed floral motifs and waist bow.",
            "image_url": "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/dress.jpg"
        },
        {
            "id": "KKW-105",
            "name": "Little Gentleman Tuxedo Suit with Bowtie",
            "category": "Boys",
            "price": 54.99,
            "sizes": ["3Y", "4Y", "5Y", "6Y", "7Y"],
            "age_group": "3-7 Years",
            "in_stock": True,
            "stock_quantity": 10,
            "description": "Premium 4-piece formal tuxedo suit including blazer, shirt, trousers, and silk bowtie.",
            "image_url": "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/tuxedo.jpg"
        },
        {
            "id": "KKW-106",
            "name": "Handmade Floral Turban & Bow Headband Set",
            "category": "Accessories",
            "price": 14.99,
            "sizes": ["Free Size"],
            "age_group": "0-6 Years",
            "in_stock": True,
            "stock_quantity": 40,
            "description": "Soft stretch fabric baby turbans and headbands adorned with delicate pearls.",
            "image_url": "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/accessories.jpg"
        }
    ]

    for p in products:
        db.collection("products").document(p["id"]).set(p)
        print(f"Seeded product: {p['id']} - {p['name']}")

    # Seed initial order
    sample_order = {
        "order_id": "ORD-1001",
        "customer_name": "Priya Sharma",
        "phone_number": "+919876543210",
        "items": [
            {
                "product_id": "KKW-101",
                "name": "Festive Silk Ethnic Lehenga Choli Set",
                "size": "4Y",
                "quantity": 1,
                "unit_price": 49.99
            }
        ],
        "total_amount": 49.99,
        "status": "Confirmed",
        "payment_status": "Paid",
        "whatsapp_link": "https://wa.me/919876543210?text=Order%20ORD-1001%20Confirmed",
        "created_at": "2026-09-25 10:00:00"
    }
    db.collection("orders").document(sample_order["order_id"]).set(sample_order)
    print("Seeded sample order: ORD-1001")

if __name__ == "__main__":
    seed_database()
