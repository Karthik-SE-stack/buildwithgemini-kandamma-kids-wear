-- Flyway V2: KAndamma Catalog, Kid Size Chart, Product Variants & Orders
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    age_group VARCHAR(50) NOT NULL, -- BABY (0-24M), TODDLER (2-5Y), KIDS (6-14Y), FESTIVE, ORGANIC
    parent_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kid_size_charts (
    id BIGSERIAL PRIMARY KEY,
    size_code VARCHAR(20) UNIQUE NOT NULL, -- 0-3M, 3-6M, 6-12M, 12-18M, 18-24M, 2-3Y, 3-4Y, 4-5Y, 6-7Y, 8-9Y, 10-12Y
    min_age_months INT NOT NULL,
    max_age_months INT NOT NULL,
    min_height_cm NUMERIC(5, 2) NOT NULL,
    max_height_cm NUMERIC(5, 2) NOT NULL,
    min_weight_kg NUMERIC(5, 2) NOT NULL,
    max_weight_kg NUMERIC(5, 2) NOT NULL
);

-- Seed Kid Size Chart
INSERT INTO kid_size_charts (size_code, min_age_months, max_age_months, min_height_cm, max_height_cm, min_weight_kg, max_weight_kg) VALUES
('0-3M', 0, 3, 50.0, 60.0, 3.0, 6.0),
('3-6M', 3, 6, 60.0, 68.0, 6.0, 8.0),
('6-12M', 6, 12, 68.0, 76.0, 8.0, 10.0),
('12-18M', 12, 18, 76.0, 83.0, 10.0, 12.0),
('18-24M', 18, 24, 83.0, 90.0, 12.0, 14.0),
('2-3Y', 24, 36, 90.0, 98.0, 14.0, 16.0),
('3-4Y', 36, 48, 98.0, 105.0, 16.0, 18.0),
('4-5Y', 48, 60, 105.0, 112.0, 18.0, 20.0),
('6-7Y', 72, 84, 115.0, 125.0, 21.0, 25.0),
('8-9Y', 96, 108, 128.0, 138.0, 26.0, 32.0)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    fabric_composition VARCHAR(255), -- e.g., '100% Organic Mulberry Silk & Cotton'
    price NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_variants (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku VARCHAR(100) UNIQUE NOT NULL,
    color VARCHAR(50) NOT NULL,
    size_code VARCHAR(20) NOT NULL,
    image_url TEXT,
    stock_quantity INT NOT NULL DEFAULT 0,
    version BIGINT DEFAULT 0 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(100) UNIQUE NOT NULL,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL, -- PENDING, PAID, SHIPPED, DELIVERED, CANCELLED
    total_amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    payment_gateway VARCHAR(50), -- STRIPE, RAZORPAY
    payment_intent_or_order_id VARCHAR(255),
    idempotency_key VARCHAR(255) UNIQUE,
    gift_wrapping_enabled BOOLEAN DEFAULT FALSE,
    gift_message TEXT,
    shipping_address_encrypted TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    variant_id BIGINT REFERENCES product_variants(id) ON DELETE SET NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_variants_sku ON product_variants(sku);
CREATE INDEX idx_orders_user ON orders(user_id);
