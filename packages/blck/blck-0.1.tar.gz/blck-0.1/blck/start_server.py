import psycopg2
import time
import blockchain_code
import connect
import node
import config

def start(node):
    exists = ()
    exist = False

    # Création de la DB blockchain
    try:
        connection = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host=config.HOST,
                                  port=config.PORT,
                                  database=config.DATABASE)
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to DB Blockchain", error)


    try:
        cursor.execute("SELECT index FROM blck")
        exists = cursor.fetchall()
        if exists is not None:
            nb_lignes = connect.count_ln(cursor, connection)
            i=0
            updated_blockchain = []
            while i != nb_lignes:
                updated_block = connect.read_DB_block(cursor, connection, i)
                updated_blockchain.append(updated_block)
                i=i+1
            node.chain = updated_blockchain
                
        else:
            # Création de la table blck
            create_table_query = '''CREATE TABLE blck
            (index SERIAL PRIMARY KEY,
            previous_hash text,
            proof int,
            timestamp int); '''
            cursor.execute(create_table_query)
            connection.commit()
            print("Base blck créée")
    except (Exception, psycopg2.Error) as error:
        print("Error while creating table Blck", error)
# try:
    # cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'blck'")
    # create_table_query = '''CREATE UNIQUE INDEX index ON blck;'''
    # cursor.execute(create_table_query)
    # print ("Index de blck créé")
# except (Exception, psycopg2.Error) as error :
    #print("Error while creating index in table Blck", error)

    # Création de la table transaction
    try:
        cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'transaction'")
        exists = cursor.fetchone()
        if exists is None:
            create_table_query = '''CREATE TABLE transaction
            (index SERIAL REFERENCES blck,
            uuid_sender text ,
            uuid_recipient text ,
            signature text,
            PRIMARY KEY (index)); '''
            cursor.execute(create_table_query)
            connection.commit()
            print("Base transaction créée")
    except (Exception, psycopg2.Error) as error:
        print("Error while creating table transaction", error)
# try:
    #c ursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'transaction'")
    # create_table_query = '''CREATE UNIQUE INDEX index ON transaction;'''
    # cursor.execute(create_table_query)
    # print ("Index de transaction créé")
# except (Exception, psycopg2.Error) as error :
#print("Error while creating index in table transaction", error)

    # Création de la table payload
    try:
        cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'payload'")
        exists = cursor.fetchone()
        if exists is None:
            create_table_query = '''CREATE TABLE payload
            (index SERIAL REFERENCES blck,
            type int,
            amount numeric,
            PRIMARY KEY (index)); '''
            cursor.execute(create_table_query)
            connection.commit()
            print("Base payload créée")
            #DB created, set to return value
            exist = False
        else:
            exist = True
    except (Exception, psycopg2.Error) as error:
        print("Error while creating table payload", error)
# try:
    # cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'payload'")
    # create_table_query = '''CREATE UNIQUE INDEX index_payload ON payload;'''
    # cursor.execute(create_table_query)
    # print ("Index de payload créé")
# except (Exception, psycopg2.Error) as error :
    #print("Error while creating index in table transaction", error)

    finally:        
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return node