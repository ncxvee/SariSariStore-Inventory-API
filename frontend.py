import requests

API_URL = "http://127.0.0.1:5000/products"

def display_header():
    print("\n")
    print("          +------------------------------------+")
    print("        +        TINDAHAN NI ALING NENA          +")
    print("      +        Sari-Sari Store Inventory           +")
    print("    +------------------------------------------------+")

def display_menu():
    display_header()

    print("    |                                                |")
    print("    |   [1]  View All Products                       |")
    print("    |   [2]  Search Product                          |")
    print("    |   [3]  Add New Product                         |")
    print("    |   [4]  Update Product                          |")
    print("    |   [5]  Delete Product                          |")
    print("    |   [6]  Exit                                    |")
    print("    |                                                |")
    print("    +------------------------------------------------+")

    print()
    print("Welcome, Ka-Tindera!")
    print("What would you like to do?")
    print()

def display_products(products):

    if not products:
        print("\nNo products available in the sari-sari store.")
        return

    print()
    print(f"{'ID':<8}{'PRODUCT NAME':<30}{'PRICE':<15}{'STOCK':<10}")
    print()

    for product in products:
        print(
            f"{product['id']:<8}"
            f"{product['name']:<30}"
            f"PHP {product['price']:<11.2f}"
            f"{product['stock']:<10}"
        )

def view_products():

    print("\n----- STORE INVENTORY -----")

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        display_products(response.json())
        return True

    except requests.exceptions.RequestException as error:
        print(f"\nUnable to retrieve products: {error}")
        return False

def search_product():

    print("\n----- SEARCH PRODUCT -----")

    while True:
        try:
            product_id = int(input("Enter Product ID: "))

            if product_id <= 0:
                print("\nPlease enter a valid product ID.")
                continue

            response = requests.get(
                f"{API_URL}/{product_id}", timeout=10
            )

            if response.status_code == 404:
                print("\nSorry! Product not found.")
                continue

            response.raise_for_status()

            print("\nProduct found!")
            display_products([response.json()])
            return True

        except ValueError:
            print("\nPlease enter a valid product ID.")

        except requests.exceptions.RequestException as error:
            print(f"\nUnable to search product: {error}")
            input("\nPress Enter to try again...")

def add_product():

    print("\n----- ADD NEW PRODUCT -----")

    while True:
        name = input("Product Name: ").strip()

        if not name:
            print("\nProduct name cannot be empty.")
            continue

        try:
            price = float(input("Price (PHP): "))
            stock = int(input("Stock Quantity: "))

            if price < 0 or stock < 0:
                print("\nPrice and stock cannot be negative.")
                continue

            product_data = {
                "name": name,
                "price": price,
                "stock": stock
            }

            response = requests.post(
                API_URL, json=product_data, timeout=10
            )
            response.raise_for_status()

            print("\nProduct added successfully!")
            display_products([response.json()])
            return True

        except ValueError:
            print("\nPlease enter valid numbers for price and stock.")

        except requests.exceptions.RequestException as error:
            print(f"\nUnable to add product: {error}")
            input("\nPress Enter to try again...")

def update_product():

    print("\n----- UPDATE PRODUCT -----")

    while True:
        try:
            product_id = int(input("Enter Product ID to update: "))

            if product_id <= 0:
                print("\nPlease enter a valid product ID.")
                continue

            response = requests.get(
                f"{API_URL}/{product_id}", timeout=10
            )

            if response.status_code == 404:
                print("\nSorry! Product not found.")
                continue

            response.raise_for_status()
            current_product = response.json()

            print("\nCurrent Product Details:")
            display_products([current_product])

            print("\nEnter the new details.")
            print("Leave a field blank to keep its current value.\n")

            name = input("New Product Name: ").strip()
            price_input = input("New Price (PHP): ").strip()
            stock_input = input("New Stock Quantity: ").strip()

            updated_data = {}

            if name:
                updated_data["name"] = name

            if price_input:
                price = float(price_input)

                if price < 0:
                    print("\nPrice cannot be negative.")
                    continue

                updated_data["price"] = price

            if stock_input:
                stock = int(stock_input)

                if stock < 0:
                    print("\nStock quantity cannot be negative.")
                    continue

                updated_data["stock"] = stock

            if not updated_data:
                print("\nNo changes entered.")
                continue

            response = requests.patch(
                f"{API_URL}/{product_id}",
                json=updated_data,
                timeout=10
            )
            response.raise_for_status()

            print("\nProduct updated successfully!")
            display_products([response.json()])
            return True

        except ValueError:
            print("\nPlease enter a valid product ID.")

        except requests.exceptions.RequestException as error:
            print(f"\nUnable to update product: {error}")
            input("\nPress Enter to try again...")

def delete_product():

    print("\n----- DELETE PRODUCT -----")

    while True:
        try:
            product_id = int(input("Enter Product ID to delete: "))

            if product_id <= 0:
                print("\nPlease enter a valid product ID.")
                continue

            response = requests.get(
                f"{API_URL}/{product_id}", timeout=10
            )

            if response.status_code == 404:
                print("\nSorry! Product not found.")
                continue

            response.raise_for_status()
            product = response.json()

            print("\nProduct to be deleted:")
            display_products([product])

            confirmation = input(
                "\nAre you sure you want to delete this product? (Y/N): "
            ).strip().upper()

            if confirmation == "N":
                print("\nDeletion cancelled.")
                continue

            if confirmation != "Y":
                print("\nPlease enter Y or N.")
                continue

            response = requests.delete(
                f"{API_URL}/{product_id}", timeout=10
            )
            response.raise_for_status()

            print("\n" + response.json()["message"])
            return True

        except ValueError:
            print("\nPlease enter a valid product ID.")

        except requests.exceptions.RequestException as error:
            print(f"\nUnable to delete product: {error}")
            input("\nPress Enter to try again...")

def main():

    operations = {
        "1": view_products,
        "2": search_product,
        "3": add_product,
        "4": update_product,
        "5": delete_product
    }

    while True:
        display_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("\nThank you for visiting Tindahan ni Aling Nena!")
            print("Come again, Ka-Tindera!")
            break

        if choice not in operations:
            print("\nInvalid choice. Please select from 1 to 6.")
            continue

        while True:
            success = operations[choice]()

            if not success:
                input("\nPress Enter to try again...")
                continue

            print("\n----- WHAT WOULD YOU LIKE TO DO NEXT? -----")
            print("[1] Return to Main Menu")
            print("[2] Exit")

            next_choice = input("\nEnter your choice (1-2): ").strip()

            if next_choice == "1":
                break

            elif next_choice == "2":
                print("\nThank you for visiting Tindahan ni Aling Nena!")
                print("Come again, Ka-Tindera!")
                return

            else:
                print("\nInvalid choice. Please select from 1 to 2.")

if __name__ == "__main__":
    main()