import requests
import pyodbc

# API endpoint and API key
api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
api_key = 'r2eYKGEpeVZ6HrHQc66J0A==TBZplKv8ZjoVuaTv'  # Your Calorie Ninja API key

# Azure SQL Database connection parameters
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'<
    'SERVER=bitirme.database.windows.net;'
    'DATABASE=food_nutrition;'
    'UID=bahacan;'
    'PWD=Feyza3169_!'
)

# Connect to Azure SQL Database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Categories to query
categories = ['fruits', 'vegetables', 'meat', 'dairy', 'grains', 'beverages']

# Iterate through categories and fetch data
for category in categories:
    response = requests.get(api_url + category, headers={'X-Api-Key': api_key})

    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            # Insert data into the database
            cursor.execute(
                """INSERT INTO food_nutrition (
                       food_name, sugar_g, fiber_g, serving_size_g, sodium_mg, potassium_mg,
                       fat_saturated_g, fat_total_g, calories, cholesterol_mg, protein_g,
                       carbohydrates_total_g
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item['name'], item['sugar_g'], item['fiber_g'], item['serving_size_g'],
                    item['sodium_mg'], item['potassium_mg'], item['fat_saturated_g'],
                    item['fat_total_g'], item['calories'], item['cholesterol_mg'],
                    item['protein_g'], item['carbohydrates_total_g']
                )
            )
        conn.commit()
    else:
        print(f"Error for category {category}: {response.status_code} - {response.text}")

# Close database connection
cursor.close()
conn.close()
