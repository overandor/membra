-- MEMBRA Production Database Schema
-- SQLite compatible

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    is_host INTEGER DEFAULT 0,
    is_verified INTEGER DEFAULT 0,
    trust_score REAL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hosts table
CREATE TABLE IF NOT EXISTS hosts (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    business_name TEXT,
    tax_id TEXT,
    stripe_account_id TEXT,
    is_active INTEGER DEFAULT 0,
    rating REAL DEFAULT 0.00,
    total_bookings INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY,
    host_id TEXT REFERENCES hosts(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    area_sq_ft REAL,
    climate_control TEXT,
    access_type TEXT,
    is_verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Uploaded images table
CREATE TABLE IF NOT EXISTS uploaded_images (
    id TEXT PRIMARY KEY,
    room_id TEXT REFERENCES rooms(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER,
    mime_type TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed INTEGER DEFAULT 0
);

-- Detected objects table
CREATE TABLE IF NOT EXISTS detected_objects (
    id TEXT PRIMARY KEY,
    image_id TEXT REFERENCES uploaded_images(id) ON DELETE CASCADE,
    object_name TEXT NOT NULL,
    category TEXT,
    confidence REAL,
    bounding_box TEXT,
    detection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SKU matches table
CREATE TABLE IF NOT EXISTS sku_matches (
    id TEXT PRIMARY KEY,
    object_id TEXT REFERENCES detected_objects(id) ON DELETE CASCADE,
    sku_id TEXT,
    match_score REAL,
    suggested_rent_price REAL,
    suggested_sale_price REAL,
    rent_mode TEXT,
    space_mode TEXT,
    is_approved INTEGER DEFAULT 0,
    approved_by TEXT REFERENCES users(id),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory items table
CREATE TABLE IF NOT EXISTS inventory_items (
    id TEXT PRIMARY KEY,
    host_id TEXT REFERENCES hosts(id) ON DELETE CASCADE,
    room_id TEXT REFERENCES rooms(id) ON DELETE CASCADE,
    sku_match_id TEXT REFERENCES sku_matches(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    condition TEXT,
    rent_price REAL,
    sale_price REAL,
    deposit_amount REAL,
    rent_mode TEXT,
    space_mode TEXT,
    is_public INTEGER DEFAULT 0,
    is_available INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approvals table
CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    inventory_item_id TEXT REFERENCES inventory_items(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    approval_type TEXT,
    status TEXT,
    notes TEXT,
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Smart actions table
CREATE TABLE IF NOT EXISTS smart_actions (
    id TEXT PRIMARY KEY,
    inventory_item_id TEXT REFERENCES inventory_items(id) ON DELETE CASCADE,
    action_type TEXT NOT NULL,
    action_config TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Requests table
CREATE TABLE IF NOT EXISTS requests (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    inventory_item_id TEXT REFERENCES inventory_items(id) ON DELETE CASCADE,
    action_type TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    quantity INTEGER DEFAULT 1,
    total_amount REAL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    request_id TEXT REFERENCES requests(id) ON DELETE CASCADE,
    payment_method_id TEXT,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    status TEXT,
    stripe_payment_intent_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    old_values TEXT,
    new_values TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics events table
CREATE TABLE IF NOT EXISTS analytics_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    host_id TEXT REFERENCES hosts(id) ON DELETE SET NULL,
    event_data TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_hosts_user_id ON hosts(user_id);
CREATE INDEX IF NOT EXISTS idx_rooms_host_id ON rooms(host_id);
CREATE INDEX IF NOT EXISTS idx_uploaded_images_room_id ON uploaded_images(room_id);
CREATE INDEX IF NOT EXISTS idx_detected_objects_image_id ON detected_objects(image_id);
CREATE INDEX IF NOT EXISTS idx_sku_matches_object_id ON sku_matches(object_id);
CREATE INDEX IF NOT EXISTS idx_inventory_items_host_id ON inventory_items(host_id);
CREATE INDEX IF NOT EXISTS idx_inventory_items_room_id ON inventory_items(room_id);
CREATE INDEX IF NOT EXISTS idx_requests_user_id ON requests(user_id);
CREATE INDEX IF NOT EXISTS idx_requests_inventory_item_id ON requests(inventory_item_id);
CREATE INDEX IF NOT EXISTS idx_transactions_request_id ON transactions(request_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_events_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_timestamp ON analytics_events(timestamp);
