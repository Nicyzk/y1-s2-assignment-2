def get_max_price(prompt):
    while True:
        try:
            price = float(input(prompt))
            if price <= 0:
                print("Error: Meal price cannot be 0 or a negative number. Please try again.")
            else:
                return price
        except Exception as e:
            print(e)


def get_k(prompt):
    while True:
        try:
            k = int(input(prompt))
            if k <= 0:
                print("Warning: k cannot be 0 or a negative value. Default k = 1 is set.")
                return 1
            else:
                return k
        except Exception as e:
            print(e)
