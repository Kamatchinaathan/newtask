from bs4 import BeautifulSoup
import sqlite3

# Read the saved HTML file
with open("saved_page.html", "r", encoding="utf-8") as f:
    response = f.read()

soup = BeautifulSoup(response, "html.parser")
table = soup.find("table", {"id": "ContentPlaceHolder1_gvbulk_deals"})
rows = table.find_all("tr")[1:]

# Connect to the SQLite database
conn = sqlite3.connect("newscrap.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bulk_deal (
        id INTEGER PRIMARY KEY,
        date TEXT,
        stock_code TEXT,
        stock_name TEXT,
        client_name TEXT,
        quantity TEXT,
        total_value TEXT,
        price TEXT
    )
''')

for index, row in enumerate(rows):
    cells = row.find_all("td")

    # Extract data from cells
    date = cells[0].text.strip()
    stock_code = cells[1].text.strip()
    stock_name = cells[2].text.strip()
    client_name = cells[3].text.strip()
    quantity = cells[4].text.strip()
    total_value = cells[5].text.strip()
    price = cells[6].text.strip()  # Assuming price is in the 6th column

    print(f"Processing row {index + 1}: {date}, {stock_code}, {stock_name}, {client_name}, {quantity}, {total_value}, {price}")

    sql = "INSERT INTO bulk_deal (date, stock_code, stock_name, client_name, quantity, total_value, price) VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (date, stock_code, stock_name, client_name, quantity, total_value, price)

    try:
        cursor.execute(sql, values)
        conn.commit()
        print(f"Insert successful for row {index + 1}")
    except sqlite3.Error as err:
        print(f"Error for row {index + 1}: {err}")

# Close the database connection
conn.close()

