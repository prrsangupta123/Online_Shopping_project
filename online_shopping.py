import subprocess as sp
import pymysql
import pymysql.cursors
import random
import warnings
from datetime import date, datetime
from tabulate import tabulate


def AddnewPurchase():
    global cur
    row = {}
    today=date.today()
    query = "SELECT COUNT(*) FROM Purchase"
    cur.execute(query)
    ans=cur.fetchall()
    p=int(ans[0]['COUNT(*)'])+1
    #print(p)
    row["Purchase_id"] = p
    con.commit()
    #query= "SELECT COUNT(*) FROM Purchase"
    #row["Purchase_id"] = int(cur.execute(query)) + 1
    #con.commit()
    print("Enter new purchase details: ")
    row["Buyer_id"] = int(input("Buyer id: "))
    row["Time_of_purchase"] = today
    query = "SELECT COUNT(*) FROM Driver"
    cur.execute(query)
    ans=cur.fetchall()
    #print (ans[0]['COUNT(*)'])
    p=(row["Purchase_id"]) % int(ans[0]['COUNT(*)'])
    row["Driver_id"] = p
    #print(p)
    con.commit()
    row["Item_id"] = int(input(" Item id: "))
    query = "INSERT INTO Purchase(Purchase_id,Buyer_id,Time_of_purchase,Driver_id) VALUES ('%d', '%d','%s', '%d')" %(row["Purchase_id"],row["Buyer_id"], row["Time_of_purchase"], row["Driver_id"])
    cur.execute(query)
    con.commit()
    query="SELECT Item_cost FROM ItemCost WHERE Item_id = '%d'" %(row["Item_id"])
    cur.execute(query)
    #con.commit()
    ans=cur.fetchall()
    
    row["Item_cost"] = int(ans[0]['Item_cost']) 
    row["Profit"] = row["Item_cost"] * (0.1)
    query = "INSERT INTO Payment(Purchase_id,Profit,Item_id) values ('%d','%d','%d')" %(row["Purchase_id"],row["Profit"],row["Item_id"])
    cur.execute(query)
    con.commit()
    return

def Addnewitem():
    global cur
    row = {}
    print("Enter item details: ")
    row["Item_name"] = input("Item name: ")
    row["Cat_name"] = input("Category name: ")
    row["Seller_id"] = int(input("Seller id: "))
    row["Item_cost"] = int(input("Item cost: "))
    query = "SELECT Cat_id FROM Category WHERE Cat_name = '%s'" %(row["Cat_name"])
    row["Cat_id"] = cur.execute(query)
    con.commit()
    query = "SELECT COUNT(*) FROM Item"
    cur.execute(query)
    ans=cur.fetchall()
    p=int(ans[0]['COUNT(*)'])+1
    #print(p)
    row["Item_id"] = p
    con.commit()
    row["Item_sale_price"] = row["Item_cost"] * (1.1)
    query = "INSERT INTO Item(Item_id,Item_name,Cat_id) VALUES('%d', '%s', '%d')" % (row["Item_id"],row["Item_name"],row["Cat_id"])
    cur.execute(query)
    con.commit()
    query = "INSERT INTO ItemCost(Item_id,Seller_id,Item_cost) VALUES('%d', '%d', '%d')" % (row["Item_id"],row["Seller_id"],row["Item_cost"])
    cur.execute(query)
    con.commit()
    query = "INSERT INTO ItemSellPrice(Item_id,Item_sale_price) VALUES('%d','%d')" % (row["Item_id"],row["Item_sale_price"])
    cur.execute(query)
    con.commit()
    return

def UpdateSellerInfo():
    global cur
    row={}
    row["Seller_id"] = int(input("Enter Seller id:"))
    row["Seller_contact"] = input("Enter Seller contact:")
    row["Seller_address"] = input("Enter Seller address:")
    query="UPDATE SellerContact SET Seller_contact='%s' where Seller_id='%d' " %(row["Seller_contact"], row["Seller_id"])
    cur.execute(query)
    con.commit()
    query="UPDATE Seller SET Seller_address='%s' where Seller_id='%d' " %(row["Seller_address"],row["Seller_id"])
    cur.execute(query)
    con.commit()
    return 

def DeliveryComplete():
    global cur
    row = {}
    today=date.today()
    #print(today)
    print("Enter delivery details: ")
    row["Purchase_id"] = int(input("Purchase id: "))
    row["Time_of_delivery"]= today
    #print(row["Time_of_delivery"])
    query="update Purchase set Time_of_delivery='%s' where Purchase_id='%d' " %(row["Time_of_delivery"],row["Purchase_id"])
    cur.execute(query)
    con.commit()
    query="SELECT Time_of_purchase FROM Purchase WHERE Purchase_id='%d' " %(row["Purchase_id"])
    cur.execute(query)
    ans=cur.fetchall()
    #print(ans)
    p=ans[0]['Time_of_purchase']
    con.commit()
    row["Time_of_purchase"]=p
    tt=today-p
    #print(tt)
    #e=input()
    #query="SELECT DATEDIFF(day,'%s', '%s') AS DateDiff" %(row["Time_of_delivery"],row["Time_of_purchase"]) 
    #cur.execute(query)
    #ans=cur.fetchall()
    #q=ans[0]['DateDiff']
    row["Delivery_time"] = tt
    con.commit()
    query="SELECT Driver_id FROM Purchase where Purchase_id='%d' " %(row["Purchase_id"])
    cur.execute(query)
    ans=cur.fetchall()
    #print (ans[0]['COUNT(*)'])
    p=int(ans[0]['Driver_id'])
    row["Driver_id"] = p
    con.commit()
    query="INSERT INTO Delivery(Purchase_id,Driver_id,Delivery_time) values ('%d','%d','%s')" %(row["Purchase_id"],row["Driver_id"],row["Delivery_time"])
    cur.execute(query)
    con.commit()
    return

def UpdateDriverInfo():
    global cur
    row={}
    row["Driver_id"] = int(input("Enter Driver id:"))
    row["Driver_contact"] = input("Enter Driver contact:")
    query="UPDATE DriverContact SET Driver_contact='%s' where Driver_id='%d'" %(row["Driver_contact"],row["Driver_id"])
    cur.execute(query)
    con.commit()
    return

def DeleteItemSold():
    global cur
    row = {}
    row["Item_id"] = int(input("Enter the id of the sold item: "))
    query="DELETE FROM Item where Item_id=%d" %(row["Item_id"])
    cur.execute(query)
    con.commit()
    query="DELETE FROM ItemCost where Item_id=%d" %(row["Item_id"])
    cur.execute(query)
    con.commit()
    query="DELETE FROM ItemSellPrice where Item_id=%d" %(row["Item_id"])
    cur.execute(query)
    con.commit()
    return

def  CalculateAverageDeliveryTime():
    global cur
    row={}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        row["Driver_id"] = int(input("Driver id: "))
        query="SELECT AVG(Delivery_time) as avg from Delivery GROUP BY Driver_id having Driver_id='%d'" %(row["Driver_id"])
        cur.execute(query)
        ans=cur.fetchall()
        print("Average delivery time:")
        print(ans[0]['avg'])
        s=input("Press any key for continue---")
        con.commit()
    return

def CalculateTotalProfit():
    global cur
    query="SELECT SUM(Profit) from Payment"
    cur.execute(query)
    ans=cur.fetchall()
    print("Profit: ")
    print(ans[0]['SUM(Profit)'])
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowBuyer():
    global cur
    query="select * from Buyer"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowBuyerContact():
    global cur
    query="select * from BuyerContact"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowCategory():
    global cur
    query="select * from Category"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowDelivery():
    global cur
    query="select * from Delivery"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowDriver():
    global cur
    query="select * from Driver"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowDriverContact():
    global cur
    query="select * from DriverContact"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowItem():
    global cur
    query="select * from Item"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowItemCost():
    global cur
    query="select * from ItemCost"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowItemSellPrice():
    global cur
    query="select * from ItemSellPrice"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowPayment():
    global cur
    query="select * from Payment"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowPurchase():
    global cur
    query="select * from Purchase"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowSeller():
    global cur
    query="select * from Seller"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def ShowSellerContact():
    global cur
    query="select * from SellerContact"
    cur.execute(query)
    ans=cur.fetchall()
    print(tabulate(ans))
    s=input("Press any key for continue---")
    con.commit()
    return

def Addnewseller():
    global cur
    row={}
    query = "SELECT COUNT(*) FROM Seller"
    cur.execute(query)
    ans=cur.fetchall()
    p=int(ans[0]['COUNT(*)'])+1
    row["Seller_id"] = p
    con.commit()
    row["First_name"]=input("Enter first name: ")
    row["Middle_name"]=input("Enter middle name: ")
    row["Last_name"]=input("Enter last name: ")
    row["Seller_address"]=input("Enter Seller address: ")
    row["Seller_contact"]=input("Enter Seller contact: ")
    query = "INSERT INTO Seller(Seller_id,First_name,Middle_name,Last_name,Seller_address) VALUES ('%d', '%s','%s', '%s','%s')" %(row["Seller_id"],row["First_name"], row["Middle_name"], row["Last_name"], row["Seller_address"])
    cur.execute(query)
    con.commit()
    query= "INSERT INTO SellerContact(Seller_id,Seller_contact) VALUES ('%d','%s')" %(row["Seller_id"],row["Seller_contact"])
    cur.execute(query)
    con.commit()
    return

def Addnewbuyer():
    global cur
    row={}
    query = "SELECT COUNT(*) FROM Buyer"
    cur.execute(query)
    ans=cur.fetchall()
    p=int(ans[0]['COUNT(*)'])+1
    row["Buyer_id"] = p
    con.commit()
    row["First_name"]=input("Enter first name: ")
    row["Middle_name"]=input("Enter middle name: ")
    row["Last_name"]=input("Enter last name: ")
    row["Buyer_address"]=input("Enter Buyer address: ")
    row["Buyer_contact"]=input("Enter Buyer contact: ")
    query = "INSERT INTO Buyer(Buyer_id,First_name,Middle_name,Last_name,Buyer_address) VALUES ('%d', '%s','%s', '%s','%s')" %(row["Buyer_id"],row["First_name"], row["Middle_name"], row["Last_name"], row["Buyer_address"])
    cur.execute(query)
    con.commit()
    query= "INSERT INTO BuyerContact(Buyer_id,Buyer_contact) VALUES ('%d','%s')" %(row["Buyer_id"],row["Buyer_contact"])
    cur.execute(query)
    con.commit()
    return

def Addnewdriver():
    global cur
    row={}
    query = "SELECT COUNT(*) FROM Driver"
    cur.execute(query)
    ans=cur.fetchall()
    p=int(ans[0]['COUNT(*)'])+1
    row["Driver_id"] = p
    con.commit()
    row["First_name"]=input("Enter first name: ")
    row["Middle_name"]=input("Enter middle name: ")
    row["Last_name"]=input("Enter last name: ")
    row["Vehicle_id"]=input("Enter Vehicle id: ")
    row["Driver_contact"]=input("Enter Driver contact: ")
    query = "INSERT INTO Driver(Driver_id,First_name,Middle_name,Last_name,Vehicle_id) VALUES ('%d', '%s','%s', '%s','%s')" %(row["Driver_id"],row["First_name"], row["Middle_name"], row["Last_name"], row["Vehicle_id"])
    cur.execute(query)
    con.commit()
    query= "INSERT INTO DriverContact(Driver_id,Driver_contact) VALUES ('%d','%s')" %(row["Driver_id"],row["Driver_contact"])
    cur.execute(query)
    con.commit()
    return

def DeleteDriver():
    global cur
    row={}
    row["Driver_id"]=int(input("Enter Driver id"))
    query="delete from Driver where Driver_id='%d'" %(row["Driver_id"])
    cur.execute(query)
    con.commit()
    query="delete from DriverContact where Driver_id='%d'" %(row["Driver_id"])
    cur.execute(query)
    con.commit()
    return

def DeleteSeller():
    global cur
    row={}
    row["Seller_id"]=int(input("Enter Seller id"))
    query="delete from Seller where Seller_id='%d'" %(row["Seller_id"])
    cur.execute(query)
    con.commit()
    query="delete from SellerContact where Seller_id='%d'" %(row["Seller_id"])
    cur.execute(query)
    con.commit()
    return

def DeleteBuyer():
    global cur
    row={}
    row["Buyer_id"]=int(input("Enter buyer id"))
    query="delete from Buyer where Buyer_id='%d'" %(row["Buyer_id"])
    cur.execute(query)
    con.commit()
    query="delete from BuyerContact where Buyer_id='%d'" %(row["Buyer_id"])
    cur.execute(query)
    con.commit()
    return

def SellerBuyer():
    global cur
    row={}
    row["Buyer_id"]=int(input("Enter buyer id: "))
    row["Purchase_id"]=int(input("Enter purchase id: "))
    query="SELECT Item_id FROM Payment WHERE Purchase_id = '%d'" %(row["Purchase_id"])
    cur.execute(query)
    ans=cur.fetchall()
    row["Item_id"] = int(ans[0]['Item_id']) 
    query="SELECT Seller_id FROM ItemCost WHERE Item_id = '%d'" %(row["Item_id"])
    cur.execute(query)
    ans=cur.fetchall()
    seller_id = int(ans[0]['Seller_id'])
    print("Id of the seller for this buyer:")
    print(seller_id) 
    s=input("Press any key for continue---")
    con.commit()
    return


optionFunctionMapping = {
        203: AddnewPurchase,
        202: Addnewitem,
        301: UpdateSellerInfo,
        302: DeliveryComplete,
        300: UpdateDriverInfo,
        402: DeleteItemSold,
        500: CalculateAverageDeliveryTime,
        501: CalculateTotalProfit,
        100: ShowBuyer,
        101: ShowBuyerContact,
        102: ShowCategory,
        103: ShowDelivery,
        104: ShowDriver,
        105: ShowDriverContact,
        106: ShowItem,
        107: ShowItemCost,
        108: ShowItemSellPrice,
        109: ShowPayment,
        110: ShowPurchase,
        111: ShowSeller,
        112: ShowSellerContact,
        204: Addnewseller,
        201: Addnewdriver,
        200: Addnewbuyer,
        401: DeleteDriver,
        403: DeleteSeller,
        400: DeleteBuyer,
        113: SellerBuyer
        }

while(1):
    tmp = sp.call('clear', shell=True)
    username = input("Username: ")
    password = input("Password: ")

    try:
        con = pymysql.connect(host='localhost',
                user=username,
                password=password,
                db='Online_Shopping',
                cursorclass=pymysql.cursors.DictCursor)
        with con:
            cur = con.cursor()
            while(1):
                tmp = sp.call('clear', shell=True)
                print("100. Show information about buyers.")
                print("101. Show contact information of buyers.")
                print("102. Show categories of items.")
                print("103. Show information about deliveries.")
                print("104. Show information about drivers.")
                print("105. Show contact information of drivers.")
                print("106. Show information about items.")
                print("107. Show cost information of items.")
                print("108. Show selling information of items.")
                print("109. Show information about payments.")
                print("110. Show information about purchases.")
                print("111. Show information about sellers.")
                print("112. Show contact information of sellers.")
                print("113. Show the seller assign assign to a particular buyer.")
                print("200. Add a new buyer.")
                print("201. Add a new driver.")
                print("202. Add a new item.")
                print("203. Add a new purchase.")
                print("204. Add a new seller.")
                print("300. Update information about a driver.")
                print("301. Update information about a seller.")
                print("302. Update time of delivery.")
                print("400. Delete information about a buyer.")
                print("401. Delete information about a driver.")
                print("402. Delete information about an item.")
                print("403. Delete information about a seller.")
                print("500. Calculate average delivery time.")
                print("501. Calculate total profit.")
                print("911. Logout.")
                c = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if c == 911:
                    break
                else:
                    optionFunctionMapping[c]()

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
