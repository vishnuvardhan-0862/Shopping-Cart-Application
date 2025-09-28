def update_cart(cart_list, product_id, quantity):
    for item in cart_list:
        if item["id"] == product_id:
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                return
            item["quantity"] = quantity
            print(f"Quantity of {item['brand']} {item['name']} updated to {quantity}")
            return
    print("Product not found in cart.")
