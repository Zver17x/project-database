-- ============================================================
--  schema.sql — ระบบร้านอาหาร
-- ============================================================

CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    member_tier VARCHAR(20) DEFAULT 'normal'
);

CREATE TABLE menu_item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    is_available TINYINT(1) DEFAULT 1
);

CREATE TABLE dining_table (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    seats INT NOT NULL,
    zone VARCHAR(50)
);

CREATE TABLE food_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT,
    table_id INT,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'pending',
    FOREIGN KEY (cust_id) REFERENCES customer(cust_id),
    FOREIGN KEY (table_id) REFERENCES dining_table(table_id)
);

CREATE TABLE order_item (         -- M:N: food_order × menu_item
    order_id INT, 
    item_id INT,
    qty INT NOT NULL DEFAULT 1,
    note VARCHAR(255),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES food_order(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_item(item_id)
);

CREATE TABLE combo (              -- M:N: menu_item × menu_item
    combo_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT, 
    sub_item_id INT, 
    amount INT NOT NULL DEFAULT 1,
    FOREIGN KEY (item_id) REFERENCES menu_item(item_id),
    FOREIGN KEY (sub_item_id) REFERENCES menu_item(item_id)
);

-- ข้อมูลตัวอย่าง (Sample Data) ทุกตาราง
INSERT INTO customer (name, phone, member_tier) VALUES 
('สมชาย ใจดี', '0812345678', 'normal'),
('สมหญิง รักเรียน', '0898765432', 'gold'),
('มานะ อดทน', '0823456789', 'vip');

INSERT INTO menu_item (name, category, price, is_available) VALUES 
('ข้าวผัดหมู', 'อาหารจานเดียว', 60.00, 1),
('ต้มยำกุ้ง', 'ต้ม/แกง', 150.00, 1),
('น้ำอัดลม', 'เครื่องดื่ม', 25.00, 1),
('ส้มตำไทย', 'ยำ/ส้มตำ', 50.00, 1);

INSERT INTO dining_table (seats, zone) VALUES 
(4, 'Indoor'),
(2, 'Outdoor'),
(8, 'VIP Room');

INSERT INTO food_order (cust_id, table_id, order_time, status) VALUES 
(1, 1, '2026-09-28 12:00:00', 'completed'),
(2, 2, '2026-09-28 12:30:00', 'cooking'),
(3, 3, '2026-09-28 13:00:00', 'pending');

INSERT INTO order_item (order_id, item_id, qty, note) VALUES 
(1, 1, 2, 'ไม่ใส่ผักชี'),
(1, 3, 2, 'หวานน้อย'),
(2, 2, 1, 'เผ็ดน้อย'),
(2, 4, 1, 'ไม่ใส่กุ้งแห้ง'),
(3, 1, 3, 'พิเศษ');

INSERT INTO combo (item_id, sub_item_id, amount) VALUES 
(1, 3, 1);
