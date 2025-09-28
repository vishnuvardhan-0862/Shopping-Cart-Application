def checkout(cart_list):
    if not cart_list:
        print("\nCart is empty. Nothing to checkout.")
        return

    print("\n===== Final Bill =====")
    total = 0
    for item in cart_list:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        print(f"{item['brand']} {item['name']} - ₹{item['price']} x {item['quantity']} = ₹{subtotal}")
    print("-" * 40)
    print(f"Grand Total: ₹{total}")
    print("=" * 40)

    cart_list.clear()
    print("Thank you for shopping with us!")
