# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล (ฉบับสมบูรณ์)
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


# ---------- ลูกค้า (customer) ----------
def search_customers(filters):
    sql = "SELECT * FROM customer WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("phone"):
        sql += " AND phone LIKE %s"
        params.append(f"%{filters['phone']}%")
    if filters.get("member_tier"):
        sql += " AND member_tier = %s"
        params.append(filters["member_tier"])
    return run_query(sql, tuple(params))


def get_customer(cust_id):
    sql = "SELECT * FROM customer WHERE cust_id = %s"
    rows = run_query(sql, (cust_id,))
    return rows[0] if rows else None


def create_customer(data):
    sql = "INSERT INTO customer (name, phone, member_tier) VALUES (%s, %s, %s)"
    return run_command(sql, (data.get("name"), data.get("phone"), data.get("member_tier", "normal")))


def update_customer(cust_id, data):
    sql = "UPDATE customer SET name = %s, phone = %s, member_tier = %s WHERE cust_id = %s"
    return run_command(sql, (data.get("name"), data.get("phone"), data.get("member_tier"), cust_id))


def delete_customer(cust_id):
    sql = "DELETE FROM customer WHERE cust_id = %s"
    return run_command(sql, (cust_id,))


# ---------- เมนูอาหาร (menu_item) ----------
def search_items(filters):
    sql = "SELECT * FROM menu_item WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("category"):
        sql += " AND category = %s"
        params.append(filters["category"])
    return run_query(sql, tuple(params))


def get_item(item_id):
    sql = "SELECT * FROM menu_item WHERE item_id = %s"
    rows = run_query(sql, (item_id,))
    return rows[0] if rows else None


def create_item(data):
    sql = "INSERT INTO menu_item (name, category, price, is_available) VALUES (%s, %s, %s, %s)"
    return run_command(sql, (data.get("name"), data.get("category"), data.get("price"), data.get("is_available", 1)))


def update_item(item_id, data):
    sql = "UPDATE menu_item SET name = %s, category = %s, price = %s, is_available = %s WHERE item_id = %s"
    return run_command(sql, (data.get("name"), data.get("category"), data.get("price"), data.get("is_available"), item_id))


def delete_item(item_id):
    sql = "DELETE FROM menu_item WHERE item_id = %s"
    return run_command(sql, (item_id,))


# ---------- ออเดอร์ (food_order) ----------
def search_orders(filters):
    sql = "SELECT * FROM food_order WHERE 1=1"
    params = []
    if filters.get("cust_id"):
        sql += " AND cust_id = %s"
        params.append(filters["cust_id"])
    if filters.get("table_id"):
        sql += " AND table_id = %s"
        params.append(filters["table_id"])
    if filters.get("status"):
        sql += " AND status = %s"
        params.append(filters["status"])
    return run_query(sql, tuple(params))


def get_order(order_id):
    sql = "SELECT * FROM food_order WHERE order_id = %s"
    rows = run_query(sql, (order_id,))
    return rows[0] if rows else None


def create_order(data):
    sql = "INSERT INTO food_order (cust_id, table_id, order_time, status) VALUES (%s, %s, NOW(), %s)"
    return run_command(sql, (data.get("cust_id"), data.get("table_id"), data.get("status", "pending")))


def update_order(order_id, data):
    sql = "UPDATE food_order SET cust_id = %s, table_id = %s, status = %s WHERE order_id = %s"
    return run_command(sql, (data.get("cust_id"), data.get("table_id"), data.get("status"), order_id))


def delete_order(order_id):
    sql = "DELETE FROM food_order WHERE order_id = %s"
    return run_command(sql, (order_id,))


# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    customers_count = run_query("SELECT COUNT(*) AS cnt FROM customer")[0]["cnt"]
    items_count = run_query("SELECT COUNT(*) AS cnt FROM menu_item")[0]["cnt"]
    orders_count = run_query("SELECT COUNT(*) AS cnt FROM food_order")[0]["cnt"]
    return {
        "customers": customers_count,
        "menu_items": items_count,
        "orders": orders_count
    }


def report_popular_items():
    """📈 เมนูขายดี (Best Sellers)"""
    sql = """
        SELECT m.item_id, m.name, m.category, SUM(oi.qty) AS total_qty
        FROM order_item oi
        INNER JOIN menu_item m ON oi.item_id = m.item_id
        GROUP BY m.item_id, m.name, m.category
        ORDER BY total_qty DESC
        LIMIT 5
    """
    return run_query(sql)


def report_daily_sales():
    """💰 ยอดขายรวมต่อวัน (Daily Sales)"""
    sql = """
        SELECT DATE(f.order_time) AS sale_date, SUM(oi.qty * m.price) AS total_sales
        FROM food_order f
        INNER JOIN order_item oi ON f.order_id = oi.order_id
        INNER JOIN menu_item m ON oi.item_id = m.item_id
        GROUP BY DATE(f.order_time)
        ORDER BY sale_date DESC
    """
    return run_query(sql)


def report_big_orders():
    """🧾 ออเดอร์ยอดเกิน 500 บาท (HAVING)"""
    sql = """
        SELECT f.order_id, f.order_time, f.status, SUM(oi.qty * m.price) AS total_amount
        FROM food_order f
        INNER JOIN order_item oi ON f.order_id = oi.order_id
        INNER JOIN menu_item m ON oi.item_id = m.item_id
        GROUP BY f.order_id, f.order_time, f.status
        HAVING total_amount > 500
        ORDER BY total_amount DESC
    """
    return run_query(sql)