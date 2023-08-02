import requests
from requests.exceptions import HTTPError
import colorama
from colorama import Fore
import simple_term_menu
from simple_term_menu import TerminalMenu

import os

from PIL import Image         

def cls():
    # Check if Operating System is Mac and Linux or Windows
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # Else Operating System is Windows (os.name = nt)
      _ = os.system('cls')
    


url = "https://yourwebsite.com/"
username = "username"
password = "pass"
baseURL = "https://www...../"

def getAmountOfProducts(amount):
    response = requests.get("https://yourwebsite.com/wp-json/wc/v3/products", auth = (username, password), params = {"per_page": amount})
    
    if (response.raise_for_status()):
        print("Error, status code: ", response.status_code)
        return

    #print (json.dumps(response.json(), indent=4))

    for product in response.json():
        print(f"""{Fore.GREEN + "ID" + Fore.WHITE + ": " + str(product.get("id"))}\n{Fore.YELLOW + "Nome" + Fore.WHITE + ": " + product.get("name")}\n{Fore.GREEN + "SKU" + Fore.WHITE + ": " + product.get("sku")}\n{Fore.CYAN + "Prezzo" + Fore.WHITE + ": " + product.get("price")}\n{Fore.RED + "Permalink" + Fore.WHITE + ": " + product.get("permalink")}\n{Fore.BLUE + "Aggiunto il" + Fore.WHITE + ": " + product.get("date_created")}\n""")
        print (Fore.WHITE + "------------------------------------------------------------------")





def checkIfProductExists(skuToCheck):

    product = requests.get("https://yourwebsite.com/wp-json/wc/v3/products", auth = (username, password), params = {"sku": skuToCheck})
    product = product.json()
    
    if (len(product) == 1):
        return True
    else:
        return False

# Retrieve a product by its SKU
def getProductBySKU(skuToFind):
    # The SKU is the product's COD
    product = requests.get("https://yourwebsite.com/wp-json/wc/v3/products", auth = (username, password), params = {"sku": skuToFind})
    
    product = product.json()


    print("\n")
    if (len(product) == 1):
        print (Fore.WHITE + "------------------------------------------------------------------")
        print(f"""{Fore.GREEN + "ID" + Fore.WHITE + ": " + str(product[0].get("id"))}\n{Fore.YELLOW + "Nome" + Fore.WHITE + ": " + product[0].get("name")}\n{Fore.GREEN + "SKU" + Fore.WHITE + ": " + product[0].get("sku")}\n{Fore.CYAN + "Prezzo" + Fore.WHITE + ": " + product[0].get("price")}\n{Fore.RED + "Permalink" + Fore.WHITE + ": " + product[0].get("permalink")}\n{Fore.BLUE + "Aggiunto il" + Fore.WHITE + ": " + product[0].get("date_created")}\n""")
        print (Fore.WHITE + "------------------------------------------------------------------")

    else:
        print(Fore.RED + "Prodotto non presente!")


# Product properties: https://woocommerce.github.io/woocommerce-rest-api-docs/#product-properties
# Update a product using its SKU
def updateProductBySKU(productSKU, dataToEdit):
    # HTTP Request to perform .../wp-json/wc/v3/products/<id>\
    # So we need to fetch the product's ID first
    product = requests.get("https://yourwebsite.com/wp-json/wc/v3/products", auth = (username, password), params = {"sku": productSKU})
    product = product.json()

    if (len(product) == 0):
        print("Non esiste un prodotto con questo COD")
        return

    # Since we need the ID but we want the user to insert the SKU we will be taking the ID from the given SKU
    productID = product[0].get("id")
    

    # If the new SKU is "" then the old sku will be removed
    try:
        requests.put(f"https://yourwebsite.com/wp-json/wc/v3/products/{productID}", dataToEdit, auth = (username, password)).json()
        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') 

    except Exception as err:
        print(f'Other error occurred: {err}')  

    else:
        print('Modifica apportata')
    

# Edit old SKU
# updateProductBySKU("412", {"regular_price": "3"})



def main():
    colorama.init()

    options = ["Visualizza Prodotto", "Visualizza Ultimi Prodotti", "Modifica Prodotto", "Elimina Prodotto"]
    editProductOptions = ["Modifica Prezzo", "Modifica COD", "Modifica Nome"]


    while(True):    
        print("\n")

        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        result = options[menu_entry_index]


        if (result == "Visualizza Ultimi Prodotti"):
            getAmountOfProducts(5)

        elif(result == "Visualizza Prodotto"):
            skuToSearch = str(input("Inserisci COD: "))
            getProductBySKU(skuToSearch)

        elif(result == "Modifica Prodotto"):
            # It will be displayed a second menu to let the user choose what does he want to edit
            terminal_menu = TerminalMenu(editProductOptions)
            menu_entry_index = terminal_menu.show()
            result = editProductOptions[menu_entry_index]

            if (result == "Modifica Prezzo"):
                productToEdit = str(input("COD Prodotto: "))


                if(checkIfProductExists(productToEdit) == False): 
                    print("Non esiste nessun prodotto con questo COD")
                    continue
                
                newPrice = str(input("Nuovo prezzo: "))

                updateProductBySKU(productToEdit, {"regular_price": newPrice})

            elif (result == "Modifica COD"):
                productToEdit = str(input("COD Vecchio: "))

                if(checkIfProductExists(productToEdit) == False): 
                    print("Non esiste nessun prodotto con questo COD")
                    continue
                
                newSku = str(input("Nuovo COD: "))

                updateProductBySKU(productToEdit, {"sku": newSku})

            elif (result == "Modifica Nome"):
                productToEdit = str(input("COD Prodotto: "))

                if(checkIfProductExists(productToEdit) == False): 
                    print("Non esiste nessun prodotto con questo COD")
                    continue
                
                newName = str(input("Nuovo nome: "))

                updateProductBySKU(productToEdit, {"name": newName})

    

            
        elif(result == "Elimina Prodotto"):
            pass
        
if __name__ == "__main__":
    main()
