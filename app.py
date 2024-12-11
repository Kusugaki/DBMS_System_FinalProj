'''

IMPORTANT INFO INSIDE database_credentials.py aliased as dbc FOR IMPORT USE
    dbc.USERNAME
    dbc.PASSWORD
    dbc.DATABASE_NAME
    dbc.INVENTORY_TABLE_NAME
    dbc.ACCOUNTS_TABLE_NAME

MODULES / PYTHON IMPORTS
        flask module = Javascript Connection
        mysql.connector = Python MySQL Connector
        logging module  = Logger

        database_credentials = aliased as "dbc"
        os module = creates directory if doesn't exist

logging.basicConfig() -> pang-Log

app = Flask(__name__) -> IMPORTANT, main application server

return render_template('URL')           -> renders the HTML data to the application
request.jsonify()                       -> turns requested data into a dictionary, Type-casts data into a JSON (js dictionary)

connector.connect()                     -> Establish MySQL Connection using Python with parameters of host:'localhost', user:'username', passwd:'password'
with connection.cursor() as cursor:     -> same as "cursor = connection.cursor()"     cursor ng MySQL database
cursor.execute()                        -> Executes SQL Queries
cursor.fetchall()                       -> Fetches SELECT data from query execution
cursor.fetchone()                       -> Fetches ONE SELECT data from query execution
connection.commit()                     -> Saves SQL Query Execution
connection.close()                      -> Closes the Python & MySQL Connection

try:                                    -> tries block of code
except (error_condition):               -> runs if try-block has an Error

except Exception as e:                  -> Exception = error_condition, e = error_varaible_name_to_use_in_the_program

as  -> ALIAS or Variable name declaration

logger = logging.getLogger(__name__)    -> initializes and starts the logger
logger.info("message")                  -> Logs string parameter into Log file

connect_to_sql()                        -> Connect to MySQL function

request.get_json()                      -> Flash built-in function to get js-html Input data


if not 'variable':                      -> verifies if variable has data, or is equal to None / Null


# SAVES ACCOUNT LOG-IN TO CURRENT SESSION
session['username'] = sql_username
session['role']     = sql_role


session.clear()                         -> Deletes account data from current session

dictionary parts: key (separated by colon) value
dictionary = Key:Value                  -> Key-value Pairs
variable = {'username':'donatello'}

to access a value:
    variable['username']
        or
    variable.get('username')

.get(), or
dictionary.get("key_name")              -> get's data from dictionary, same as dictionary["key_name"]

return jsonify( { key:value } )         -> returns a dictionary to send to the js file

products = []                           -> Initializes a LIST
products.append()                       -> Appends/Adds a new element to the end of the list

results = cursor.fetchall()
for row in results:
    row[0], row[1], row[2], ...         -> ordering of Data based on SQL query field name ordering

@app.route('URL', methods=['POST']) or ['GET']  -> Flask module js connector

if __name__ == '__main__':              -> kahit wag na
app.run(debug=True)                     -> start the application server

SQL QUERIES
    SQL info:
        database name: turtles_cup
        table names:    inventory
                        accounts
        field names:
            inventory:
                id              INT AUTO_INCREMENT  PK
                product_name    VARCHAR(50)
                category        VARCHAR(50)
                price           DECIMAL(15,4)
                quantity        INT
            accounts
                account_id  INT AUTO_INCREMENT  PK
                username    VARCHAR(20)
                password    VARCHAR(50)
                role        VARCHAR(10)

INSERT INTO table_name (field_names, ...) VALUES (values, ...);

UPDATE table_name
SET field_name = "new_value"
WHERE field_name = "value";

DELETE FROM table_name
WHERE condition;

SELECT * FROM table_name;

SELECT field_names, ... FROM table_name;



####### CODES

    sql_query = f"""
    SELECT username, password, role
    FROM {dbc.ACCOUNTS_TABLE_NAME}
    WHERE username = '{username}' AND password = '{password}';
    """

    sql_query = f"""
    SELECT id, product_name, category, price, quantity 
    FROM {dbc.INVENTORY_TABLE_NAME};
    """

    sql_query = f"""
    INSERT INTO {dbc.INVENTORY_TABLE_NAME} (product_name, category, price, quantity) 
    VALUES ('{product_name}', '{category}', {price}, {quantity});
    """

    sql_query = f"""
    UPDATE {dbc.INVENTORY_TABLE_NAME}
    SET product_name = '{product_name}', 
        category = '{category}', 
        price = {price}, 
        quantity = {quantity}
    WHERE id = {product_id};
    """

    sql_query_check = f"""
    SELECT username FROM {dbc.ACCOUNTS_TABLE_NAME}
    WHERE username = '{username}';
    """

    sql_query_insert = f"""
    INSERT INTO {dbc.ACCOUNTS_TABLE_NAME} (username, password, role)
    VALUES ('{username}', '{password}', '{role}');
    """

    sql_query = f"""
    DELETE FROM {dbc.INVENTORY_TABLE_NAME} 
    WHERE id = {product_id};
    """



'''


from flask import Flask, render_template, request, jsonify, session
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
app.secret_key = 'your_secret_key'  # Set this to a random secret key


def create_database_and_tables():
    """Create database and tables if they do not exist."""
    connection = connector.connect(
        host="localhost",
        user=dbc.USERNAME,
        passwd=dbc.PASSWORD
    )

    with connection.cursor() as cursor:
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
                password VARCHAR(50) NOT NULL,
                role VARCHAR(10) NOT NULL
            );
        """)

        # Save to the database
        connection.commit()
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

    # Connectivity Validation
    if connection is None:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, product_name, category, price, quantity FROM {dbc.INVENTORY_TABLE_NAME}")
        sql_data = cursor.fetchall()
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

@app.route('/log-in-input-event', methods=['POST'])
def log_in():
    username = request.get_json().get('username')
    password = request.get_json().get('password')

    print(username, password)

    # Username validation
    if not username or len(username) < 3:
        logger.warning("Username validation failed.")
        return jsonify({'message': 'Invalid username. Must be at least 3 characters long.'}), 400

    sql_query = f"""
    SELECT username, password, role
    FROM {dbc.ACCOUNTS_TABLE_NAME}
    WHERE username = '{username}' AND password = '{password}';
    """

    logger.info(f"Log-in attempt: {username = }")
    connection = connect_to_sql()
    if not connection:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            account_data = cursor.fetchall()

            if not account_data:
                logger.warning("No account found for the provided credentials.")
                return jsonify({'message': 'Log-in Failed'}), 401

            sql_username = account_data[0][0]
            sql_password = account_data[0][1]
            sql_role     = account_data[0][2]  # Fetch the role

            print(f"{sql_role = } {sql_username = } { sql_password = }")

            if username == sql_username and password == sql_password:
                logger.info("Log-in Successful. role ="+ str(sql_role))
                session['username'] = sql_username
                session['role']     = sql_role
                
                render_template('index.html')

                return jsonify({'message': 'Log -in Successful', 'role': sql_role})
            
            else:
                logger.warning("Log-in Failed: Incorrect credentials.")
                return jsonify({'message': 'Log-in Failed'}), 401

    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()

@app.route('/is-logged-in', methods=['GET'])
def is_logged_in():
    if 'username' in session:
        return jsonify({'logged_in': True, 'role': session['role']})
    return jsonify({'logged_in': False}), 401

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()  # Clear the session
    logger.info("User logged out successfully.")
    return jsonify({'message': 'Logged out successfully'})


@app.route('/get-log', methods=['GET'])
def get_log():
    try:
        log_path = 'C:\\Users\\JP\\Desktop\\KUSOGAKI\\gaki_VisualStudio\\DBMS_System_FinalProj\\static\\turtles_cup.log' 
        with open(log_path, 'r') as file:
            log_content = file.read()
            print(log_content)
        return jsonify({'log': log_content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    try:
        products = []

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            for row in results:
                products.append({'id':           row[0],
                                 'product_name': row[1],
                                 'category':     row[2],
                                 'price':        row[3],
                                 'quantity':     row[4]})
            return jsonify(products)

    except connector.Error as err:
        logger.error(f"Error: {err}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()


@app.route('/add-product-input-event', methods =['POST'])
def add_product_input_event():
    logger.info("Add product button pressed.")
    data = request.get_json()

    product_name = data.get('product_name')
    category     = data.get('category')
    price        = data.get('price')
    quantity     = data.get('quantity')

    sql_query = f"""
    INSERT INTO {dbc.INVENTORY_TABLE_NAME} (product_name, category, price, quantity) 
    VALUES ('{product_name}', '{category}', {price}, {quantity});
    """

    connection = connect_to_sql()
    if not connection:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            connection.commit()
            logger.info(f"Product added: {product_name}, Category: {category}, Price: {price}, Quantity: {quantity}")

    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()

    response = {'message': 'Input value received successfully'}
    return jsonify(response)


@app.route('/delete-input-event', methods=['POST'])
def delete_product():
    product_id = request.get_json().get('product_id')
    logger.info(f"Delete request for product ID: {product_id}")

    sql_query = f"""
    DELETE FROM {dbc.INVENTORY_TABLE_NAME} 
    WHERE id = {product_id};
    """

    connection = connect_to_sql()
    if not connection:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)

            if cursor.rowcount == 0:
                logger.warning("No product found with the given ID.")
                return jsonify({'message': 'No product found with the given ID'}), 404
            else:
                connection.commit()
                logger.info(f"Product ID {product_id} deleted successfully.")
                return jsonify({'message': 'Deletion successful'})
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database Deletion error'}), 500
    finally:
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
    SET product_name = '{product_name}', 
        category = '{category}', 
        price = {price}, 
        quantity = {quantity}
    WHERE id = {product_id};
    """

    connection = connect_to_sql()
    if not connection:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
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
        connection.close()


@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    role     = data.get('role')

    print(f"{username = }, {password = }, {role = }")

    # Username validation
    if not username or len(username) < 3:
        logger.warning("Username validation failed.")
        return jsonify({'message': 'Invalid username. Must be at least 3 characters long.'}), 400

    # Password validation
    if not password or len(password) < 6:
        logger.warning("Password validation failed.")
        return jsonify({'message': 'Invalid password. Must be at least 6 characters long.'}), 400

    # Check if the username already exists
    sql_query_check = f"""
    SELECT username FROM {dbc.ACCOUNTS_TABLE_NAME}
    WHERE username = '{username}';
    """

    connection = connect_to_sql()
    if not connection:
        logger.error("Database connection failed.")
        return jsonify({'message': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query_check)
            existing_user = cursor.fetchone()

            if existing_user:
                logger.warning("Username already exists.")
                return jsonify({'message': 'Username already exists. Please choose a different one.'}), 400

            # Insert new user into the database
            sql_query_insert = f"""
            INSERT INTO {dbc.ACCOUNTS_TABLE_NAME} (username, password, role)
            VALUES ('{username}', '{password}', '{role}');
            """
            cursor.execute(sql_query_insert)
            connection.commit()

            logger.info("Account created successfully.")
            return jsonify({'message': 'Account created successfully!'}), 201

    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()


if __name__ == "__main__":
    logger.info("Starting Flask application.")
    app.run(debug=True)