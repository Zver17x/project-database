# ระบบร้านอาหาร (Restaurant Ordering) — Term Project Template

เทมเพลตนี้ทำส่วนหน้าเว็บ (frontend) และ API ให้แล้ว
งานของนิสิตคือ **ออกแบบฐานข้อมูล และเขียน SQL** ใน `db.py` กับ `schema.sql`

## เริ่มต้น
1. `pip install -r requirements.txt`
2. แก้ `config.py` ใส่ user/password/host ของ MySQL ที่อาจารย์แจกให้
3. ออกแบบและสร้างตารางใน `schema.sql` แล้วรันบน MySQL ของตัวเอง
4. `python app.py` → เปิด http://127.0.0.1:5000

> เปิดมาจะเห็นหน้าเว็บ แต่กดค้นหาจะขึ้น 🚧 TODO จนกว่าจะเขียน SQL ครบ

## งานที่ต้องทำใน db.py (มองหา # TODO)
**CRUD:**
  - search_customers, get/create/update/delete_customer
  - search_items, get/create/update/delete_item
  - search_orders, get/create/update/delete_order

**รายงาน (JOIN + GROUP BY + subquery):**
  - report_summary — ตัวเลขสรุป dashboard
  - report_popular_items — 📈 เมนูขายดี (Best Sellers)
  - report_daily_sales — 💰 ยอดขายรวมต่อวัน (Daily Sales)
  - report_big_orders — 🧾 ออเดอร์ยอดเกิน 500 บาท (HAVING)

## กติกา
- ใช้ `%s` เป็น placeholder เสมอ (กัน SQL injection)
- query ที่ join หลายตารางเขียนแบบ explicit INNER JOIN ... ON ...
- ชื่อตาราง/คอลัมน์ใน db.py ต้องตรงกับ schema.sql
