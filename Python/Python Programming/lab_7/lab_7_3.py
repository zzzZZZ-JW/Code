class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        item = {
            "name" : name,
            "price" : price,
            "quantity": quantity
        }
        self.items.append(item)

    def __str__(self):
        if not self.items:
            return "购物车是空的"
        
        result = "购物车内容:\n"
        total = 0

        for item in self.items:
            item_total = item["price"] * item["quantity"]
            result += f"- {item['name']} × {item['quantity']}: ￥{item_total:.2f}\n"
            total = total + item_total

        result += f"总计: ￥{total:.2f}"
        return result

cart = ShoppingCart()

cart.add_item("Python书籍", 49.9, 2)
cart.add_item("鼠标", 52)

print(cart)