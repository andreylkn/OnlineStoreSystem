def calculate_effective_price(price, discount):
    return price * (1 - discount / 100)

def calculate_total_item_price(effective_price, quantity):
    return effective_price * quantity
