from cart import add_item, cart_total
from invoice import invoice_total


def sample_cart():
    cart = []
    add_item(cart, "keyboard", 79.99)
    add_item(cart, "mouse", 24.50, qty=2)
    return cart


def test_totals_agree():
    """The cart and the invoice must always show the same total."""
    cart = sample_cart()
    assert cart_total(cart, discount_pct=10) == invoice_total(cart, discount_pct=10)