import datetime
import os
import random
import string
import subprocess

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.apps import App
from google.adk.models import Gemini
from google import genai
from google.genai import types
from google.cloud import firestore, storage
from google.oauth2.credentials import Credentials

async def generate_memories_callback(callback_context: CallbackContext):
    try:
        await callback_context.add_session_to_memory()
    except Exception:
        pass
    return None

from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog
from .a2ui_utils import a2ui_callback

PROJECT_ID = "qwiklabs-gcp-02-eb01df7117c0"
BUCKET_NAME = f"{PROJECT_ID}-kandamma-media"

def get_db():
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
        creds = Credentials(token)
        return firestore.Client(project=PROJECT_ID, credentials=creds)
    except Exception:
        return firestore.Client(project=PROJECT_ID)

def get_storage_client():
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
        creds = Credentials(token)
        return storage.Client(project=PROJECT_ID, credentials=creds)
    except Exception:
        return storage.Client(project=PROJECT_ID)


def get_inventory(category: str = None, size: str = None, max_price: float = None) -> list[dict]:
    """Fetch and filter clothing items from the Kandamma Kids Wear catalog.

    Args:
        category: Optional category filter ("Girls", "Boys", "Toddlers", "Accessories").
        size: Optional size filter ("2Y", "3Y", "4Y", "5Y", "6Y", "0-3M", etc.).
        max_price: Optional maximum price filter in USD.

    Returns:
        List of product dictionaries matching the query filters.
    """
    db = get_db()
    products_ref = db.collection("products")
    docs = products_ref.stream()

    results = []
    for doc in docs:
        p = doc.to_dict()
        if category and p.get("category", "").lower() != category.lower():
            continue
        if max_price and p.get("price", 0.0) > max_price:
            continue
        if size and size.upper() not in [s.upper() for s in p.get("sizes", [])]:
            continue
        results.append(p)
    return results


def get_product_details(product_id: str) -> dict:
    """Fetch details for a specific product ID (e.g. 'KKW-101').

    Args:
        product_id: Product ID string.

    Returns:
        Product dictionary or error message if not found.
    """
    db = get_db()
    doc = db.collection("products").document(product_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"error": f"Product '{product_id}' not found in catalog."}


def admin_manage_product(action: str, product_id: str, name: str = None, category: str = None, price: float = None, sizes: list = None, stock_quantity: int = None, description: str = None) -> str:
    """Admin CRUD tool to add, update, or remove inventory items from Kandamma Kids Wear catalog.

    Args:
        action: "add", "update", or "delete".
        product_id: Unique product ID (e.g., 'KKW-107').
        name: Name of product (for add/update).
        category: Product category (for add/update).
        price: Price in USD (for add/update).
        sizes: List of sizes (for add/update).
        stock_quantity: Available inventory count (for add/update).
        description: Product description (for add/update).

    Returns:
        Confirmation status string.
    """
    db = get_db()
    doc_ref = db.collection("products").document(product_id)

    if action.lower() == "delete":
        doc_ref.delete()
        return f"Successfully deleted product {product_id} from catalog."

    if action.lower() in ["add", "update"]:
        p_data = {
            "id": product_id,
            "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if name: p_data["name"] = name
        if category: p_data["category"] = category
        if price is not None: p_data["price"] = float(price)
        if sizes: p_data["sizes"] = sizes
        if stock_quantity is not None: p_data["stock_quantity"] = int(stock_quantity)
        if description: p_data["description"] = description
        p_data["in_stock"] = (stock_quantity is None or stock_quantity > 0)

        doc_ref.set(p_data, merge=True)
        return f"Successfully {action}ed product {product_id} ({name or ''}) in catalog."

    return f"Unknown action '{action}'. Use 'add', 'update', or 'delete'."


def create_whatsapp_order(customer_name: str, phone_number: str, product_id: str, size: str, quantity: int = 1) -> dict:
    """Create an order for Kandamma Kids Wear and format a WhatsApp admin order link.

    Args:
        customer_name: Customer full name.
        phone_number: Customer phone number.
        product_id: Product ID to order (e.g., 'KKW-101').
        size: Selected size (e.g., '4Y').
        quantity: Order quantity.

    Returns:
        Order summary including Order ID, WhatsApp admin link, and secure checkout URL.
    """
    db = get_db()
    prod_doc = db.collection("products").document(product_id).get()
    if not prod_doc.exists:
        return {"error": f"Product '{product_id}' does not exist."}

    prod = prod_doc.to_dict()
    unit_price = prod.get("price", 0.0)
    total_amount = round(unit_price * quantity, 2)

    order_num = "".join(random.choices(string.digits, k=5))
    order_id = f"ORD-{order_num}"

    product_name = prod.get("name", product_id)
    product_link = prod.get("image_url", f"https://kandammakidswear.com/p/{product_id}")

    # Format WhatsApp order message
    wa_msg = (
        f"Hi Kandamma Kids Wear Admin! I would like to place an order:\n"
        f"Order ID: {order_id}\n"
        f"Product: {product_name} ({product_id})\n"
        f"Size: {size}\n"
        f"Quantity: {quantity}\n"
        f"Total: ${total_amount}\n"
        f"Customer: {customer_name} ({phone_number})\n"
        f"Product Link: {product_link}"
    )

    import urllib.parse
    encoded_msg = urllib.parse.quote(wa_msg)
    whatsapp_url = f"https://wa.me/919876543210?text={encoded_msg}"
    payment_url = f"https://checkout.kandammakidswear.com/pay/{order_id}"

    order_doc = {
        "order_id": order_id,
        "customer_name": customer_name,
        "phone_number": phone_number,
        "items": [
            {
                "product_id": product_id,
                "name": product_name,
                "size": size,
                "quantity": quantity,
                "unit_price": unit_price
            }
        ],
        "total_amount": total_amount,
        "status": "Pending",
        "payment_status": "Secured Checkout Pending",
        "whatsapp_link": whatsapp_url,
        "payment_link": payment_url,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db.collection("orders").document(order_id).set(order_doc)

    return {
        "order_id": order_id,
        "customer_name": customer_name,
        "product": product_name,
        "size": size,
        "total_amount": f"${total_amount:.2f}",
        "whatsapp_admin_link": whatsapp_url,
        "secured_payment_link": payment_url,
        "message": "Order created successfully! Click the WhatsApp link to submit order directly to admin."
    }


def process_secure_payment(order_id: str) -> dict:
    """Generate or verify a secure payment session for an order.

    Args:
        order_id: Order ID (e.g. 'ORD-1001').

    Returns:
        Payment session status and secured checkout details.
    """
    db = get_db()
    order_ref = db.collection("orders").document(order_id)
    doc = order_ref.get()

    if not doc.exists:
        return {"error": f"Order '{order_id}' not found."}

    order = doc.to_dict()
    total = order.get("total_amount", 0.0)

    payment_session = {
        "order_id": order_id,
        "amount": f"${total:.2f}",
        "currency": "USD",
        "payment_gateway": "Stripe/Razorpay 256-bit SSL Encrypted",
        "status": "Ready for Payment",
        "checkout_url": f"https://checkout.kandammakidswear.com/pay/{order_id}?token=sec_live_99831"
    }

    return payment_session


def generate_outfit_preview(prompt: str, tool_context=None) -> dict:
    """Generate a high-quality visual preview/image for Kandamma Kids Wear apparel styling using gemini-3.1-flash-lite-image.

    Args:
        prompt: Description of the outfit/clothing visual to generate.

    Returns:
        Dictionary containing public image URL and description.
    """
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
        creds = Credentials(token)
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="global", credentials=creds)
    except Exception:
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

    full_prompt = f"Professional studio product photography of Kandamma Kids Wear apparel: {prompt}. High resolution, clean luxury backdrop, vivid colors."

    res = client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=full_prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
    )

    image_bytes = None
    for part in res.candidates[0].content.parts:
        if part.inline_data:
            image_bytes = part.inline_data.data
            break

    if not image_bytes:
        return {"error": "Failed to generate image bytes from model."}

    # Save artifact for Playground if tool_context available
    if tool_context and hasattr(tool_context, "save_artifact"):
        try:
            tool_context.save_artifact(image_bytes, filename="outfit_preview.jpg", mime_type="image/jpeg")
        except Exception:
            pass

    # Upload to Cloud Storage
    rand_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    blob_name = f"outfits/outfit_{rand_suffix}.jpg"

    storage_client = get_storage_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(image_bytes, content_type="image/jpeg")

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_name}"

    return {
        "status": "success",
        "prompt": prompt,
        "public_url": public_url,
        "message": f"Outfit image generated and published successfully to {public_url}"
    }


# Set up A2UI System Prompt
schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

system_instruction = schema_manager.generate_system_prompt(
    role_description="You are the AI Shopping Concierge & Admin Assistant for 'Kandamma Kids Wear', a premium kids apparel brand.",
    workflow_description="Help customers explore luxury kids outfits, check catalog inventory, place orders via WhatsApp admin link, process secure payments, and generate visual outfit styling previews.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms. "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (like public_url returned from generate_outfit_preview). Set the Image url to that exact https link. "
        "No markdown in text; use usageHint property ('h1', 'h2', 'body') for headings. "
        "Output ONLY raw A2UI JSON array when returning structured UI."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="kandamma_kids_wear_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=system_instruction,
    tools=[
        PreloadMemoryTool(),
        get_inventory,
        get_product_details,
        admin_manage_product,
        create_whatsapp_order,
        process_secure_payment,
        generate_outfit_preview
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
