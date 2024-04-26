import os, time, datetime, pickle
from math import ceil

try:
    import pwinput, pandas
    from tkinter import *
    from PIL import Image, ImageFont, ImageDraw
except ImportError:
    print("Supermarket Cart System:\n")
    print("Some modules not found, attempting to install them...\n")
    try:
        import pip
    except ImportError:
        time.sleep(1)
        print("PIP is required to install the modules!")
    else:
        os.system("python -m pip install Pillow==9.5.0 pwinput pandas")
        os.system('cls' if os.name=='nt' else 'clear')
        print("Supermarket Cart System:\n")
        print("Try to relaunch the program again!")
    time.sleep(2)
    exit()

if os.name=='nt':
    os.system('title Supermarket Cart System')

users={}

def receiptpng():
    with open("receipt.txt") as f:
        lines = tuple(line.rstrip() for line in f.readlines())
    
    try:
        font = ImageFont.truetype("cour.ttf", size=16)
    except IOError:
        font = ImageFont.load_default()

    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 20

    tallest_line = max(lines, key=lambda line: font.getsize(line)[1])
    max_line_height = font_points_to_pixels(font.getsize(tallest_line)[1])
    realistic_line_height = max_line_height * 0.8
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))
    os.system('cls' if os.name=='nt' else 'clear')
    image_width = 472

    background_color = 255
    image = Image.new('L', (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(image)

    font_color = 0
    horizontal_position = margin_pixels
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * realistic_line_height)))
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)

    return image
 
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print("Supermarket Cart System:\n")

def grocery():
    clear()
    print(f"{'Item':<32}Price\n")
    for i in items.itertuples():
        print(f"{i.Item:<32}{i.Price} AED")

def receipt_write():
    datenow=datetime.datetime.now().strftime("%d/%m/%Y")
    timenow=datetime.datetime.now().strftime("%H:%M:%S")
    with open('receipt.txt','w') as receipt:
        receipt.write("""-------------------------------------------
                Supermarket
                  Al Quoz
-------------------------------------------\n""")
        receipt.write(f"{'Name':<32}{'Price'}")
        for i in cart:
            receipt.write(f"\n{i+' x'+str(cart[i][1]):<32}{cart[i][0]:>3} AED")
        receipt.write("\n-------------------------------------------")
        receipt.write(f"\n{'SUB TOTAL:':<31} {mainprice:>2} AED")
        receipt.write(f"\n{'VAT CHARGED:':<31} {vat:>2} AED")
        receipt.write("\n-------------------------------------------")
        receipt.write(f"\n{'TOTAL:':<31} {pricevat:>2} AED")
        receipt.write("\n-------------------------------------------")
        receipt.write(f"\n{'PAID BY:':<31} {paymenttype.capitalize()}")
        receipt.write(f"\n{'USER:':<31} {username}")
        receipt.write("\n-------------------------------------------")
        receipt.write(f"\n{'':<15} {datenow}")
        receipt.write(f"\n{'':<16} {timenow}")
        receipt.write(f"\n{'':<8}THANK YOU FOR PURCHASING!!!\n")

def receipt_read():
    def close():
        winreceipt.destroy()
    os.system('cls' if os.name=='nt' else 'clear')
    image = receiptpng()
    image.save("receipt.png")
    winreceipt=Tk()
    winreceipt.title('Receipt')
    winreceipt.geometry()
    with open('receipt.txt','r') as receipt:
        Label(winreceipt,text=receipt.read(),font='Courier 8',justify='left').pack()
    Button(winreceipt,text="Press Enter to return!",font='Courier 8',bg='white',command=close).pack(pady=20)
    winreceipt.bind('<Return>',lambda e: close())
    winreceipt.bind('<Escape>',lambda e: close())
    winreceipt.focus_force()
    winreceipt.mainloop()
    os.remove("receipt.txt")

def confirm():
    global price
    for i in items.itertuples():
        if name==i.Item:
            price=i.Price
            return True
    return False

try:
    with open('users.inf','rb') as test:
        try:
            users=pickle.load(test)
        except EOFError:
            pass
except:
    with open('users.inf','wb') as test:
        pass

os.system("attrib +h users.inf")
        
def checkacc():
    while True:
        global username
        clear()
        print("[1] Register account\n[2] Login account\n[0] Exit program\n")
        try:
            choice=int(input("Choice: "))
        except:
            continue
        if choice==1:
            clear()
            print("Register for a new account below:\n")
            username=input("Username: ")
            password=pwinput.pwinput()
            if username.isspace()==True or password.isspace()==True or "" in (username,password):
                print("\nInputs cannot be empty spaces!")
                input("\nPress any key to return...")
                continue
            elif username not in users:
                users[username]=password
                os.system("attrib -h users.inf")
                with open('users.inf','wb') as file:
                    pickle.dump(users,file)
                os.system("attrib +h users.inf")
                checkprice()
                clear()
                print(f"Welcome, {username}!")
                time.sleep(1.5)
                break
            else:
                print("\nUser found in database!")
                input("\nPress any key to return...")
                continue
        elif choice==2:
            clear()
            print("Enter your login info below:\n")
            username=input("Username: ")
            password=pwinput.pwinput()
            if username not in users:
                print("\nUser not found in database!")
                input("\nPress any key to return...")
                continue
            else:
                if users[username]==password:
                    checkprice()
                    clear()
                    print(f"Welcome back, {username}!")
                    time.sleep(1.5)
                    break
                else:
                    print("\nInvalid password entered!")
                    input("\nPress any key to return...")
                    continue
        elif choice==0:
            print("\nExiting program...")
            time.sleep(1)
            exit()
               
def checkprice():
    global cart, mainprice
    cart={}
    mainprice=0
    try:
        with open(username+'_cart.txt','r') as file:
            cart=eval(file.read().rstrip())
        for i in cart:
            mainprice+=cart[i][0]  
    except:
        pass   

try:
    items=pandas.read_csv("https://raw.githubusercontent.com/Fahad-69/supermarket/main/items.csv")
except:
    clear()
    print("No internet connection, exiting program...")
    time.sleep(1.5)
    exit()

checkacc()

while True:
    clear()
    print(f"Account Username: {username}\n")
    print(f"Number of items in Cart: {len(cart)}\n")
    print("[1] Add item to cart\n[2] Remove item from cart\n[3] Check item cart\n[4] Clear item cart\n[5] Print receipt\n[6] Delete receipt\n[7] Delete account\n[8] Log out account\n[0] Exit program\n")
    try:
        choice=int(input("Choice: "))
    except:
        continue
    if choice==1:
        grocery()
        name=input("\nEnter item name: ").title()
        if confirm()==True:
            if name in cart:
                while True:
                    clear()
                    alrexist=input("Item already exists in cart, are you sure? [Y/n] ").lower()
                    if alrexist=='y':
                        mainprice-=cart[name][0]
                        skip=True
                        break
                    elif alrexist=='n':
                        skip=False
                        break
                    else:
                        continue
                if skip==False:
                    continue
            while True:
                grocery()
                print("\nEnter item name:",name+f" ({price} AED)")
                try:
                    quantity=int(input("Enter item quantity: "))
                    if quantity>=1:
                        mainprice+=price*quantity
                        itemprice=price*quantity
                        cart[name]=[itemprice,quantity]
                        with open(username+'_cart.txt','w') as file:
                            file.write(str(cart))
                        break
                    else:
                        print("\nInvalid quantity, returning to main menu...")
                        time.sleep(1)
                        break
                except:
                    print("\nInvalid quantity, returning to main menu...")
                    time.sleep(1)
                    break
        else:
            grocery()
            print("\nEnter item name:",name)
            print("\nItem not found, returning to main menu...")
            time.sleep(1)
    elif choice==2:
        clear()
        if len(cart)==0:
            print("Cart is empty! Returning to main menu...")
        else:
            print(f"{'Item':<32}{'Price'}")
            for i in cart:
                print(f"\n{i+' x'+str(cart[i][1]):<32}{cart[i][0]:>3} AED",end='')
            remname=input("\n\nItem to be removed: ").title()
            if remname in cart:
                mainprice-=cart[remname][0]
                del cart[remname]
                if len(cart)==0:
                    try:
                        os.remove(username+'_cart.txt')
                    except:
                        pass
                else:
                    with open(username+'_cart.txt','w') as file:
                        file.write(str(cart))
                print("\nItem removed, returning to main menu...")
            else:
                print("\nItem not found, returning to main menu...")
        time.sleep(1)
    elif choice==3:
        clear()
        if len(cart)==0:
            print("Cart is empty! Returning to main menu...")
            time.sleep(1)
            continue
        else:
            print(f"{'Item':<32}{'Price'}")
            for i in cart:
                print(f"\n{i+' x'+str(cart[i][1]):<32}{cart[i][0]:>3} AED",end='')
        input("\n\nPress Enter to return to main menu...")
    elif choice==4:
        pricevat=0
        mainprice=0
        vat=0
        cart={}
        try:
            os.remove(username+'_cart.txt')
        except:
            pass
        clear()
        print("Clearing cart...")
        time.sleep(1)
    elif choice==5:
        if len(cart)==0:
            clear()
            print("Cart is empty! Returning to main menu...")
            time.sleep(1)
            continue
        if os.path.exists("receipt.png")==True:
            while True:
                clear()
                alrexist=input("Receipt file found, are you sure you want to overwrite? [Y/n] ").lower()
                if alrexist=='y':
                    ovwr=False
                    break
                elif alrexist=='n':
                    ovwr=True
                    break
                else:
                    continue
            if ovwr==True:
                continue
        while True:
            pricevat=round(mainprice*1.05,2)
            vat=round(pricevat-mainprice,2)
            clear()
            paymenttype=input("Do you want to pay by Cash or Credit: ").capitalize()
            checkright=True
            if paymenttype=='Cash':
                break
            elif paymenttype=='Credit':
                break
            else:
                checkright=False
                break
        if checkright==False:
            clear()
            print("Invalid payment type, returning to main menu!")
            time.sleep(1)
            continue
        receipt_write()
        receipt_read()
        clear()
        print("Printing receipt done, returning to main menu...")   
        time.sleep(1)
    elif choice==6:
        clear()
        if os.path.exists("receipt.png")==True:
            os.remove("receipt.png")
            print("Receipt deleted, returning to main menu...")
        else:
            print("Receipt already does not exist, returning to main menu...")
        time.sleep(1) 
    elif choice==7:
        clear()
        print("Confirm by entering your password below:\n")
        userpassword=pwinput.pwinput()
        if users[username]==userpassword:
            while True:
                clear()
                choice=input("Are you sure you want to delete your account? [Y/n] ").lower()
                if choice in ('y','n'):
                    break
            if choice=='y':
                del users[username]
                try:
                    os.remove(username+'_cart.txt')
                except:
                    pass
                os.system("attrib -h users.inf")
                with open('users.inf','wb') as file:
                    pickle.dump(users,file)
                os.system("attrib +h users.inf")
                try:
                    os.remove(username+'_cart.txt')
                except:
                    pass
                checkacc()  
            else:
                continue
        else:
            clear()
            print("Password entered invalid, returning to main menu...")
            time.sleep(1)
    elif choice==8:
        checkacc()
    elif choice==0:
        if os.path.exists(username+'_cart.txt')==True and len(cart)==0:
            os.remove(username+'_cart.txt')
        print("\nExiting program...")
        time.sleep(1)
        exit()
    else:
        continue
        
        