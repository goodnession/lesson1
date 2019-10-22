def format_price(price):
    price = abs(int(price))
    return f'Цена: {price} руб.'

price = format_price(56.24)
print(price)