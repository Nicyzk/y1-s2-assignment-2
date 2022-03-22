def check_option(prompt):
    while True:
        try:
            option = int(input(prompt))
            if 0 < option <= 5:
                return option
            else:
                raise Exception()
        except Exception as e:
            print("Error: Option must be between 1 and 5. Please try again.")

def check_mixed_rice_2d(and_groups):
    updated_and_groups = []
    for keywords in and_groups:
        updated = []
        iter = 0
        while iter != len(keywords):
            if keywords[iter] == 'mixed' and keywords[iter+1] == 'rice':
                updated.append('mixed rice')
                iter += 2
            else:
                updated.append(keywords[iter])
                iter += 1
        updated_and_groups.append(updated)
    return updated_and_groups

def check_mixed_rice_1d(keywords):
    updated = []
    iter = 0
    while iter != len(keywords):
        if keywords[iter] == 'mixed' and keywords[iter+1] == 'rice':
            updated.append('mixed rice')
            iter += 2
        else:
            updated.append(keywords[iter])
            iter += 1
    return updated

def get_max_price(prompt):
    while True:
        try:
            price = float(input(prompt))
            if price <= 0:
                print("Error: Meal price cannot be 0 or a negative number. Please try again.")
            else:
                return price
        except Exception as e:
            print("Please enter a numerical value. Please try again.")


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
