# ============================================================
#  app.py — เว็บแอป Flask (ทำให้เสร็จแล้ว ★ ไม่ต้องแก้)
#  รัน:  python app.py  แล้วเปิด http://127.0.0.1:5000
# ============================================================
from flask import Flask, request, jsonify, render_template
import db

app = Flask(__name__)


def safe(fn, *args, **kwargs):
    try:
        return jsonify({"ok": True, "data": fn(*args, **kwargs)})
    except NotImplementedError as e:
        return jsonify({"ok": False, "todo": True, "error": str(e)}), 501
    except Exception as e:
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500


@app.route("/")
def page_home():
    return render_template("index.html")

@app.route("/report")
def page_report():
    return render_template("report.html")


# ---- ลูกค้า ----
@app.route("/api/customers", methods=["GET"])
def customers_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_customers, filters)

@app.route("/api/customers/<int:_id>", methods=["GET"])
def customer_get(_id):
    return safe(db.get_customer, _id)

@app.route("/api/customers", methods=["POST"])
def customer_create():
    return safe(db.create_customer, request.json)

@app.route("/api/customers/<int:_id>", methods=["PUT"])
def customer_update(_id):
    return safe(db.update_customer, _id, request.json)

@app.route("/api/customers/<int:_id>", methods=["DELETE"])
def customer_delete(_id):
    return safe(db.delete_customer, _id)

# ---- เมนูอาหาร ----
@app.route("/api/menu-items", methods=["GET"])
def items_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_items, filters)

@app.route("/api/menu-items/<int:_id>", methods=["GET"])
def item_get(_id):
    return safe(db.get_item, _id)

@app.route("/api/menu-items", methods=["POST"])
def item_create():
    return safe(db.create_item, request.json)

@app.route("/api/menu-items/<int:_id>", methods=["PUT"])
def item_update(_id):
    return safe(db.update_item, _id, request.json)

@app.route("/api/menu-items/<int:_id>", methods=["DELETE"])
def item_delete(_id):
    return safe(db.delete_item, _id)

# ---- ออเดอร์ ----
@app.route("/api/orders", methods=["GET"])
def orders_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_orders, filters)

@app.route("/api/orders/<int:_id>", methods=["GET"])
def order_get(_id):
    return safe(db.get_order, _id)

@app.route("/api/orders", methods=["POST"])
def order_create():
    return safe(db.create_order, request.json)

@app.route("/api/orders/<int:_id>", methods=["PUT"])
def order_update(_id):
    return safe(db.update_order, _id, request.json)

@app.route("/api/orders/<int:_id>", methods=["DELETE"])
def order_delete(_id):
    return safe(db.delete_order, _id)


@app.route("/api/reports/summary")
def report_summary():
    return safe(db.report_summary)

@app.route("/api/reports/popular-items")
def route_report_popular_items():
    return safe(db.report_popular_items)

@app.route("/api/reports/daily-sales")
def route_report_daily_sales():
    return safe(db.report_daily_sales)

@app.route("/api/reports/big-orders")
def route_report_big_orders():
    return safe(db.report_big_orders)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
