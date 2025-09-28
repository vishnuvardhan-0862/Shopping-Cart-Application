def remove_from_cart(cart_list, product_id):
    for item in cart_list:
        if item["id"] == product_id:
            cart_list.remove(item)
            print(f"{item['brand']} {item['name']} removed from cart.")
            return
    print("Product not found in cart.")
