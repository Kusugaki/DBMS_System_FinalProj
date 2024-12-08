from flask import Flask, render_template, request, jsonify
from mysql import connector

# Imports external file with Username, Password, and Database Name
import database_credentials as dbc

# IMPORTANT INITIALIZATIONS

''' local Server (Flask) initialization '''
server = Flask(__name__)

''' MySQL Database Initializations '''
SQL_CONNECTION = connector.connect(
    host="localhost",
    user=dbc.USERNAME,
    passwd=dbc.PASSWORD,
    database=dbc.DATABASE_NAME
)
SQL_CURSOR = SQL_CONNECTION.cursor()

@server.route('/')
def home():
    return render_template('index.html')

@server.route('/input-event', methods=['POST'])
def add_product_input_event():
    # Gets values from replied JavaScript JSON response
    product_name = request.get_json()['product_name']
    category     = request.get_json()['category']
    price        = request.get_json()['price']
    quantity     = request.get_json()['quantity']

    # Queries form inputs into MySQL database
    sql_query = f"""
    INSERT INTO {dbc.TABLE_NAME} (product_name, category, price, quantity) 
    VALUES ({product_name}, {category}, {price}, {quantity})
    """
    SQL_CURSOR.execute(sql_query)

    # Saves query to MySQL database
    SQL_CURSOR.commit()

    # Process the input value and return a response
    response = { 'message': 'Input value received successfully' }
    return jsonify(response)


if __name__ == "__main__":
    server.run(debug=True)




def fetch_sql_data():
    SQL_CURSOR.execute(f"SELECT * FROM {dbc.TABLE_NAME}")

    sql_data = SQL_CURSOR.fetchall()
   
    try: 
        assert len(sql_data[0]) == 5
        for record in sql_data:
            yield record[0], record[1], record[2], record[3], record[4]
    except AssertionError:
        print("temp_assertionerror")
        yield None, None, None, None, None
        
            




def modify_by_product_id(product_id):
    ...


def add_to_dynamic_table(product_name, category, price, quantity) -> None:
    # HTML element ID
    table_id = "dynamic-table"

    # Get the table body
    table_body = document.getElementById(table_id).getElementsByTagName("tbody")[0]
    
    # Create a new Table Row
    new_row = document.createElement("tr")
    
    # Create and append cells (Table Data) for the new row
    for value in [product_name, category, price, quantity]:
        cell = document.createElement("td")
        cell.textContent = value
        new_row.appendChild(cell)
    
    # Append the row to the table body
    table_body.appendChild(new_row)
    


# Attach the function to the button click
document.getElementById("button-add").addEventListener("click", create_proxy(add_product))