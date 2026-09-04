from cart import TAX_RATE


def invoice_total(cart, discount_pct=0):
    subtotal = sum(item["price"] * item["qty"] for item in cart)
    total = subtotal * (1 - discount_pct / 100)
    return round(total * (1 + TAX_RATE), 2)


def render_invoice(cart, discount_pct=0):
    lines = [f"{i['qty']}x {i['name']:<12} ${i['price'] * i['qty']:>7.2f}" for i in cart]
    lines.append("-" * 26)
    lines.append(f"TOTAL             ${invoice_total(cart, discount_pct):>7.2f}")
    return "\n".join(lines)
