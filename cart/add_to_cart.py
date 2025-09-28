def add_to_cart(products_list, cart_list, product_id, quantity):
    if len(cart_list) >= 8 and all(item["id"] != product_id for item in cart_list):
        print("Cart limit reached (max 8 items).")
        return

    product = next((p for p in products_list if p["id"] == product_id), None)
    if not product:
        print("Invalid product ID.")
        return

    for item in cart_list:
        if item["id"] == product_id:
            item["quantity"] += quantity
            print(f"Updated quantity of {item['brand']} {item['name']} to {item['quantity']}")
            return

    cart_list.append({
        "id": product["id"],
        "name": product["name"],
        "brand": product["brand"],
        "price": product["price"],
        "quantity": quantity
    })
    print(f"{product['brand']} {product['name']} added to cart.")
