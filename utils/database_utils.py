import mysql.connector

def setup_database_connection(config):
    if not config.get('use_DB', False):
        print("Database usage is disabled in the configuration.")
        return None

    if 'database' not in config:
        print("Database configuration not found in config.")
        return None

    db_config = config['database']
    try:
        db_connection = mysql.connector.connect(
            host=db_config.get('host', ''),
            user=db_config.get('user', ''),
            password=db_config.get('password', ''),
            database=db_config.get('database', ''),
            autocommit=True,
            connection_timeout=6000
        )
        print("Database connection established successfully.")
        return db_connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None