TAX_RATE = 0.08


def add_item(cart, name, price, qty=1):
    cart.append({"name": name, "price": price, "qty": qty})


def cart_total(cart, discount_pct=0):
    subtotal = sum(item["price"] * item["qty"] for item in cart)
    total = subtotal * (1 - discount_pct / 100)
    return round(total * (1 + TAX_RATE), 2)