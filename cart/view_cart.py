def view_cart(cart_list):
    if not cart_list:
        print("\nYour cart is empty.")
        return

    print("\n===== Your Cart =====")
    total = 0
    for item in cart_list:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        print(f"{item['brand']} {item['name']} - ₹{item['price']} x {item['quantity']} = ₹{subtotal}")
    print("-" * 40)
    print(f"Total: ₹{total}")
    print("=" * 40)
