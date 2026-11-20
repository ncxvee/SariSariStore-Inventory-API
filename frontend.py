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
        print()
        print("No products available in the sari-sari store.")
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
        response = requests.get(API_URL)
        response.raise_for_status()

        products = response.json()

        display_products(products)

    except requests.exceptions.RequestException as error:
        print(f"\nUnable to retrieve products: {error}")


def search_product():

    print("\n----- SEARCH PRODUCT -----")

    try:
        product_id = int(input("Enter Product ID: "))

        response = requests.get(f"{API_URL}/{product_id}")

        if response.status_code == 404:
            print("\nSorry! Product not found.")
            return

        response.raise_for_status()

        product = response.json()

        print("\nProduct found!")
        display_products([product])

    except ValueError:
        print("\nPlease enter a valid product ID.")

    except requests.exceptions.RequestException as error:
        print(f"\nUnable to search product: {error}")


def add_product():

    print("\n----- ADD NEW PRODUCT -----")

    name = input("Product Name: ").strip()

    if not name:
        print("\nProduct name cannot be empty.")
        return

    try:
        price = float(input("Price (PHP): "))
        stock = int(input("Stock Quantity: "))

        if price < 0 or stock < 0:
            print("\nPrice and stock cannot be negative.")
            return

        product_data = {
            "name": name,
            "price": price,
            "stock": stock
        }

        response = requests.post(API_URL, json=product_data)

        if response.status_code == 201:
            print("\nProduct added successfully!")
            display_products([response.json()])

        else:
            print("\nUnable to add product.")
            print(response.json())

    except ValueError:
        print("\nPlease enter valid numbers for price and stock.")

    except requests.exceptions.RequestException as error:
        print(f"\nUnable to connect to the API: {error}")


def update_product():

    print("\n----- UPDATE PRODUCT -----")

    try:
        product_id = int(input("Enter Product ID to update: "))

        response = requests.get(f"{API_URL}/{product_id}")

        if response.status_code == 404:
            print("\nSorry! Product not found.")
            return

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
            updated_data["price"] = float(price_input)

        if stock_input:
            updated_data["stock"] = int(stock_input)

        if not updated_data:
            print("\nNo changes entered.")
            return

        response = requests.patch(
            f"{API_URL}/{product_id}",
            json=updated_data
        )

        if response.status_code == 200:
            print("\nProduct updated successfully!")
            display_products([response.json()])

        else:
            print("\nUnable to update product.")
            print(response.json())

    except ValueError:
        print("\nPlease enter a valid product ID, price, or stock quantity.")

    except requests.exceptions.RequestException as error:
        print(f"\nUnable to update product: {error}")


def delete_product():

    print("\n----- DELETE PRODUCT -----")

    try:
        product_id = int(input("Enter Product ID to delete: "))

        response = requests.get(f"{API_URL}/{product_id}")

        if response.status_code == 404:
            print("\nSorry! Product not found.")
            return

        response.raise_for_status()

        product = response.json()

        print("\nProduct to be deleted:")
        display_products([product])

        confirmation = input(
            "\nAre you sure you want to delete this product? (Y/N): "
        ).strip().upper()

        if confirmation != "Y":
            print("\nDeletion cancelled.")
            return

        response = requests.delete(f"{API_URL}/{product_id}")

        if response.status_code == 200:
            print("\n" + response.json()["message"])

        else:
            print("\nUnable to delete product.")
            print(response.json())

    except ValueError:
        print("\nPlease enter a valid product ID.")

    except requests.exceptions.RequestException as error:
        print(f"\nUnable to delete product: {error}")


def main():

    while True:

        display_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_products()

        elif choice == "2":
            search_product()

        elif choice == "3":
            add_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice. Please select from 1 to 6.")

        input("\nPress Enter to return to the sari-sari store menu...")


if __name__ == "__main__":
    main()
