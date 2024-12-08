from flask import Flask, render_template, request, jsonify
from mysql import connector
import logging
import database_credentials as dbc
import os

# Define the log file path
LOGGER_PATH = "DBMS_System_FinalProj\\static\\turtles_cup.log"

# Create the directory if it does not exist
log_directory = os.path.dirname(LOGGER_PATH)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s\t- %(message)s',  # Log message format
    handlers=[
        logging.FileHandler(LOGGER_PATH),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

# Create a logger
logger = logging.getLogger(__name__)

# MAIN APPLICATION SERVER INITIALIZATION
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


# MySQL Initialization
create_database_and_tables()


# Utility Function to Connect to SQL
def connect_to_sql():
    try:
        return connector.connect(
            host="localhost",
            user=dbc.USERNAME,
            passwd=dbc.PASSWORD,
            database=dbc.DATABASE_NAME
        )
    except connector.Error as err:
        logger.error(f"Error connecting to MySQL: {err}")
        return None

# Utility Function to Get inventory data
def fetch_inventory_sql_data():
    """Fetch all data from the inventory table."""
    logger.info("Fetching inventory data.")
    connection = connect_to_sql()
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = connection.cursor()
    cursor.execute(f"SELECT id, product_name, category, price, quantity FROM {dbc.INVENTORY_TABLE_NAME}")
    sql_data = cursor.fetchall()
    cursor.close()
    connection.close()

    try: 
        assert len(sql_data[0]) == 5
        for record in sql_data:
            yield record[0], record[1], record[2], record[3], record[4]
    except AssertionError:
        logger.error("Assertion error: fetched data does not match expected format.")
        yield None, None, None, None, None


@app.route('/')
def home():
    logger.info("Home page accessed.")
    return render_template('index.html')


@app.route('/get-products', methods=['GET'])
def get_products():
    connection = connect_to_sql()
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    sql_query = f"""
    SELECT id, product_name, category, price, quantity 
    FROM {dbc.INVENTORY_TABLE_NAME};
    """
    cursor = connection.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        products = [{'id': row[0], 'product_name': row[1], 'category': row[2], 'price': row[3], 'quantity': row[4]} for row in results]
        return jsonify(products)
    except connector.Error as err:
        logger.error(f"Error: {err}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/add-product-input-event', methods =['POST'])
def add_product_input_event():
    logger.info("Add product button pressed.")
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
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500
    cursor = connection.cursor()
    
    try:
        cursor.execute(sql_query, (product_name, category, price, quantity))
        connection.commit()
        logger.info(f"Product added: {product_name}, Category: {category}, Price: {price}, Quantity: {quantity}")

    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()

    response = {'message': 'Input value received successfully'}
    return jsonify(response)


@app.route('/log-in-input-event', methods=['POST'])
def log_in():
    username = request.get_json()['username']
    password = request.get_json()['password']

    sql_query = f"""
    SELECT username, password
    FROM {dbc.ACCOUNTS_TABLE_NAME}
    WHERE username = %s AND password = %s;
    """

    logger.info(f"Log-in attempt: {username = }")
    logger.name = username

    connection = connect_to_sql()
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query, (username, password))
        account_data = cursor.fetchall()

        if not account_data:
            logger.warning("No account found for the provided credentials.")
            return jsonify({'message': 'Log-in Failed'}), 401

        sql_username = account_data[0][0]
        sql_password = account_data[0][1]

        if username == sql_username and password == sql_password:
            logger.info("Log-in Successful.")
            return jsonify({'message': 'Log-in Successful'})
        else:
            logger.warning("Log-in Failed: Incorrect credentials.")
            username = ""
            return jsonify({'message': 'Log-in Failed'}), 401

    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/delete-input-event', methods=['POST'])
def delete_product():
    product_id = request.get_json()['product_id']
    logger.info(f"Delete request for product ID: {product_id}")

    sql_query = f"""
    DELETE FROM {dbc.INVENTORY_TABLE_NAME} 
    WHERE id = %s;
    """

    connection = connect_to_sql()
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query, (product_id,))

        if cursor.rowcount == 0:
            logger.warning("No product found with the given ID.")
            return jsonify({'message': 'No product found with the given ID'}), 404
        else:
            connection.commit()
            logger.info(f"Product ID {product_id} deleted successfully.")
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database Deletion error'}), 500
    
    sql_query = f"""
    SET @max_value = (SELECT MAX(id) FROM {dbc.INVENTORY_TABLE_NAME});
    
    ALTER TABLE {dbc.INVENTORY_TABLE_NAME}
    AUTO_INCREMENT = @max_value + 1;
    """    

    try:
        cursor.execute(sql_query)
        return jsonify({'message': 'Deletion successful'})
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database Deletion error'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/update-input-event', methods=['POST'])
def update_product():
    data = request.get_json()

    product_id   = data['product_id']
    product_name = data['product_name']
    category     = data['category']
    price        = data['price']
    quantity     = data['quantity']

    sql_query = f"""
    UPDATE {dbc.INVENTORY_TABLE_NAME}
    SET product_name = %s, 
        category = %s, 
        price = %s, 
        quantity = %s
    WHERE id = %s;
    """

    connection = connect_to_sql()
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query, (product_name, category, price, quantity, product_id))
        connection.commit()

        if cursor.rowcount == 0:
            logger.warning("No product found with the given ID for update.")
            return jsonify({'message': 'No product found with the given ID'}), 404

        logger.info(f"Product ID {product_id} updated successfully.")
        return jsonify({'message': 'Product updated successfully'})
    
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database update error'}), 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    logger.info("Starting Flask application.")
    app.run(debug=True)