# My agent: Kandamma Kids Wear - AI Concierge & E-Commerce Platform

One-liner: A high-end e-commerce conversational agent and storefront for kids' apparel (Kandamma Kids Wear) featuring product catalog search, size recommendations, Firestore inventory management, WhatsApp order routing, secure checkout links, and custom outfit visual generation.

Tool coverage:
- Memory: Remembers customer preferences such as kid's age, gender, size, style/color preferences, delivery address, and past orders.
- Tools:
  - `get_inventory`: Fetch and filter clothing items from Firestore catalog by category (Boys, Girls, Toddlers, Accessories), size, age group, or price range.
  - `create_whatsapp_order`: Formats order details (Order ID, product link, size, total price) and generates direct WhatsApp admin order message link for seamless customer support & ordering.
  - `process_secure_payment`: Generates a secure payment session/link for online checkout.
  - `admin_manage_product`: Admin CRUD tool to add, update, or remove inventory items from Firestore.
- Catalog/UI: Products collection rendered as A2UI rich cards, product showcases, price summary tables, and admin management tables.
- Image gen: Generates custom kids outfit visual previews and styling suggestions using `gemini-3.1-flash-lite-image`.
- Sandbox: Cart total, discount calculations, size recommendation logic, and tax computation using Python sandbox code executor.

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): WhatsApp admin integration, secure payment gateway link, Admin CRUD tools, Cloud Storage image hosting, Cloud Run frontend deployment.
