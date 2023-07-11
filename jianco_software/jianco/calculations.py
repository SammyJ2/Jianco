import mysql.connector
import random

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=r"HIj8$2$29:$&>>]?]’so87€!]’",
    database="monthlyinventoryrecord"
)
cursor = conn.cursor()

# Fetch the maximum dayDay value from the table
cursor.execute("SELECT MAX(dayDay) FROM mnr")
max_day = cursor.fetchone()[0]

# Increment the max_day by 1 to get the next available dayDay value
dayDay = max_day + 1 if max_day is not None else 1

if max_day is None:
    start_inventory = float(input("Enter Start Inventory: "))
    start_inventory_p = float(input("Enter Start InventoryP: "))
else:
 # Fetch the previous row's start inventory from the Gallons column
 cursor.execute("SELECT `Gallons` FROM mnr WHERE `dayDay` = %s" % max_day)
 start_inventory = cursor.fetchone()[0]
 # Fetch the previous row's start inventory_p from the GallonsP column
 cursor.execute("SELECT `GallonsP` FROM mnr WHERE `dayDay` = %s" % max_day)
 start_inventory_p = cursor.fetchone()[0]

#copy above when first time starting

if 'start_inventory' not in locals():
    start_inventory = float(input("Enter Start Inventory: "))

if 'start_inventory_p' not in locals():
    start_inventory_p = float(input("Enter Start InventoryP: "))

values = (
    dayDay,  # dayDay (unique for each row)
    start_inventory,  # Start Inventory
    float(input("Enter Gallons Delivered (optional): ") or 0),  # Gallons Delivered
    0,  # Gallons Pumped (initially 0)
    0,  # Book Inventory (initially 0)
    0,  # inches (initially 0)
    0,  # Gallons (initially 0)
    0,  # Daily (initially 0)
    "sj",  # Initials
    "1",  # number
    float(input("Enter Regular Sold:") or 0),
    float(input("Enter Super Sold:") or 0),
    float(input("Enter Regular Sold:") or 0),
    dayDay,  # Day (same as dayDay)
    start_inventory_p,  # Start InventoryP
    float(input("Enter Gallons DeliveredP (optional): ") or 0),  # Gallons DeliveredP
    0,  # Gallons PumpedP (initially 0)
    0,  # Book InventoryP (initially 0)
    0,  # InchesP (provide a default value of 0)
    0,  # GallonsP (initially 0)
    0,  # Dailyy (initially 0)
    "sj",  # InitialsP
)

#then this below after the above

# Calculate Gallons Pumped
regular = values[10]
super = values[11]
gallons_pumped = values[10] + (values[11] * 0.65)
values = values[:3] + (gallons_pumped,) + values[4:]

# Calculate Gallons PumpedP
premium = values[12]
super = values[11]
gallons_pumped_p = values[12] + (values[11] * 0.35)
values = values[:16] + (gallons_pumped_p,) + values[17:]

# Calculate Book Inventory
start_inventory = values[1]
gallons_delivered = values[2]
gallons_pumped = values[3]
book_inventory = float(values[1]) + float(values[2]) - float(values[3])
values = values[:4] + (book_inventory,) + values[5:]

# Calculate Book InventoryP
start_inventory_p = values[14]
gallons_delivered_p = values[15]
gallons_pumped_p = values[16]
book_inventory_p = float(values[14]) + float(values[15]) - float(values[16])
values = values[:17] + (book_inventory_p,) + values[18:]

# Estimate Gallons
gallons = values[6]
estimated_gallons = int(book_inventory) + random.randint(-10, 10)
values = values[:6] + (estimated_gallons,) + values[7:]

# Estimate GallonsP
gallons_p = values[19]
estimated_gallons_p = int(book_inventory_p) + random.randint(-10, 10)
values = values[:19] + (estimated_gallons_p,) + values[20:]

# Calculate Daily
gallons = values[6]
initials = values[8]
daily = float(gallons) - float(book_inventory)
values = values[:7] + (daily,) + values[8:]

# Calculate Dailyy
gallonsP = values[19]
initials_p = values[21]
dailyy = float(gallonsP) - float(book_inventory_p)
values = values[:20] + (dailyy,) + (initials_p,)

# Fetch the nearest Inches value from the 'inches' table for Inches
cursor.execute("SELECT `Inches` FROM inches ORDER BY ABS(`Gallons` - %s) LIMIT 1", (values[6],))
inches_row = cursor.fetchone()
if inches_row is not None:
    inches = inches_row[0]
else:
    # Handle the case when no rows are returned
    inches = 0  # Set a default value or perform alternative actions

# Similarly, handle the case for fetching inchesP value
cursor.execute("SELECT `Inches` FROM inches ORDER BY ABS(`Gallons` - %s) LIMIT 1", (values[19],))
inchesP_row = cursor.fetchone()
if inchesP_row is not None:
    inchesP = inchesP_row[0]
else:
    # Handle the case when no rows are returned
    inchesP = 0  # Set a default value or perform alternative actions

# Update the values with the fetched Inches and InchesP
values = values[:5] + (inches,) + values[6:18] + (inchesP,) + values[19:]

query = "INSERT INTO `mnr` (`dayDay`, `Start Inventory`, `Gallons Delivered`, `Gallons Pumped`, `Book Inventory`, `Inches`, `Gallons`, `Daily`, `Initials`, `numbers`, `Regular`, `Super`, `Premium`, `Day`, `Start InventoryP`, `Gallons DeliveredP`, `Gallons PumpedP`, `Book InventoryP`, `InchesP`, `GallonsP`, `Dailyy`, `InitialsP`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

cursor.execute(query, values)
conn.commit()
