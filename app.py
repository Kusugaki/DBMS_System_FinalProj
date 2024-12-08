from flask import Flask, render_template, request, jsonify
from mysql import connector
import database_credentials as dbc

# IMPORTANT INITIALIZATIONS
app = Flask(__name__)

def create_database_and_tables():
    """Create database and tables if they do not exist."""
    connection = connector.connect(
        host="localhost",
        user=dbc.USERNAME,
        passwd=dbc.PASSWORD
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbc.DATABASE_NAME};")
    cursor.execute(f"USE {dbc.DATABASE_NAME};")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {dbc.INVENTORY_TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            product_name VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(15, 4) NOT NULL,
            quantity MEDIUMINT NOT NULL
        );
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {dbc.ACCOUNTS_TABLE_NAME} (
            account_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(20) NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)

    connection.commit()
    cursor.close()
    connection.close()


create_database_and_tables()


# Utility Function
def connect_to_sql():
    return connector.connect(
        host="localhost",
        user=dbc.USERNAME,
        passwd=dbc.PASSWORD,
        database=dbc.DATABASE_NAME
    )

# Utility Function
def fetch_sql_data():
    """Fetch all data from the inventory table."""
    connection = connect_to_sql()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {dbc.INVENTORY_TABLE_NAME}")
    sql_data = cursor.fetchall()
    cursor.close()
    connection.close()

    try: 
        assert len(sql_data[0]) == 5
        for record in sql_data:
            yield record[0], record[1], record[2], record[3], record[4]
    except AssertionError:
        print("temp_assertionerror")
        yield None, None, None, None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-product-input-event', methods=['POST'])
def add_product_input_event():
    print("ADD PRODUCT BUTTON PRESSED")
    data = request.get_json()

    product_name = data['product_name']
    category = data['category']
    price = data['price']
    quantity = data['quantity']

    sql_query = f"""
    INSERT INTO {dbc.INVENTORY_TABLE_NAME} (product_name, category, price, quantity) 
    VALUES (%s, %s, %s, %s);
    """

    connection = connect_to_sql()
    cursor = connection.cursor()
    cursor.execute(sql_query, (product_name, category, price, quantity))
    connection.commit()
    cursor.close()
    connection.close()

    for i in fetch_sql_data():
        print(i)

    response = {'message': 'Input value received successfully'}
    return jsonify(response)

@app.route('/log-in-input-event', methods=['POST'])
def log_in():
    username = request.get_json()['username']
    password = request.get_json()['password']

    sql_query = f"""
    SELECT * FROM {dbc.ACCOUNTS_TABLE_NAME}
    WHERE username = %s AND password = %s;
    """

    connection = connect_to_sql()
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query, (username, password))
        account_data = cursor.fetchall()

        # if fetched data is EMPTY or NULL/NONE
        if not account_data:
            print("No account found")
            return jsonify({'message': 'Log-in Failed'}), 401

        sql_username = account_data[0][1]
        sql_password = account_data[0][2]

        if username == sql_username and password == sql_password:
            print("Log-in Successful")
            return jsonify({'message': 'Log-in Successful'})
        else:
            print ("Log-in Failed")
            return jsonify({'message': 'Log-in Failed'}), 401

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)