import psycopg2
from block import Block
from transaction import Transaction
import transaction
from payload import decode
import config


def connect_DB():
    """Connect to the database. Returns cursor and connection handler."""
    try:
        cursor = 0
        connection =0
        connection = psycopg2.connect(user = config.USER,
                                  password = config.PASSWORD,
                                  host = config.HOST,
                                  port = config.PORT,
                                  database = config.DATABASE)
        cursor = connection.cursor()        
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
    finally:
        return cursor, connection

def drop_table(cursor, connection):
    """Drop table."""
    #Définit la requête SQL de suppression
    postgres_insert_query = """ DROP TABLE blockchain"""
    try:
        #Définit le contenu des %s de la requête
        record_to_insert = blockchain
        #Exécute la requête
        cursor.execute(postgres_insert_query, record_to_insert)
    except (Exception, psycopg2.Error) as error:
        print("Error executing PostgreSQL DROP TABLE request", error)
    try:
        #Commit la requête
        connection_db.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error commiting PostgreSQL DROP TABLE", error)
  
def disconnect_DB(cursor, connection_db):
    """Disconnect from the database. Takes cursor and connection handler as argument."""
    try:
        cursor.close()
        connection_db.close()
        #print("PostgreSQL connection is closed \n")
    except (Exception, psycopg2.Error) as error:
        print("Error closing PostgreSQL table or connection", error)

def count_ln(cursor, connection_db, table):
    """Count the numlber of lines in the DB."""
    try:
        if table == "blck":
            cursor.execute("""SELECT COUNT(*) FROM blck """)
        else :
            if table == "payload":
                cursor.execute("""SELECT COUNT(*) FROM payload """)
            else:
                cursor.execute("""SELECT COUNT(*) FROM transaction """)                                     
        count = cursor.fetchone()
        return int(count[0])
    except (Exception, psycopg2.Error) as error:
        print("Error counting PostgreSQL lines in the table ", error)

def write_DB_block(cursor, connection_db, block):
    """Writes a block in the database. Takes cursor, connection handler and block as argument. Returns True if successfull."""
    if block.index is not 0:
        try:
            #Définit la requête SQL d'insertion
            postgres_insert_query = """ INSERT INTO blck (index, previous_hash, proof, timestamp) VALUES (%s,%s,%s,%s)"""
            #Définit le contenu des %s de la requête pour la tabl blck
            record_to_insert = block.index, block.previous_hash, block.proof, block.timestamp
            #Exécute la requête
            cursor.execute(postgres_insert_query, record_to_insert)
        except (Exception, psycopg2.Error) as error:
            print("Error executing PostgreSQL INSERT request BLCK   ", error)
            return False
        try:
            #Définit la requête SQL d'insertion
            postgres_insert_query = """ INSERT INTO transaction (index, uuid_sender, uuid_recipient, signature) VALUES (%s,%s,%s,%s)"""
            # Définit le contenu des %s de la requête pour la table transaction
            tx = block.transactions[0]
            tx = tx.to_ordered_dict()
            record_to_insert = block.index, tx['sender'], tx['recipient'], tx['signature']
            #Exécute la requête
            cursor.execute(postgres_insert_query, record_to_insert)
        except (Exception, psycopg2.Error) as error:
            print("Error executing PostgreSQL INSERT request TRANSACTION", error)
            return False
        try:
#######################################################################################################            
#
#       The following code will write the payload in the DB.
#       At the moment, it will only write transactions data.
# 
#########################################################################################################
            #Définit la requête SQL d'insertion
            postgres_insert_query = """ INSERT INTO payload (index, type, amount) VALUES (%s,%s,%s)"""
            # Définit le contenu des %s de la requête pour la table transaction
            record_to_insert = block.index, "1", tx['amount']
            #Exécute la requête
            cursor.execute(postgres_insert_query, record_to_insert)
        except (Exception, psycopg2.Error) as error:
            print("Error executing PostgreSQL INSERT request PAYLOAD", error)
            return False
    try:
        #Commit la requête
        connection_db.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error commiting PostgreSQL connection", error)
        return False

def init_blck():
    cursor, connect = connect_DB()
    
    #Définit la requête SQL d'initialisation
    postgres_insert_query = """ INSERT INTO blck (index, previous_hash, transactions, proof, timestamp) VALUES (%s,%s,%s,%s,%s)"""
    try:
        #Définit le contenu des %s de la requête
        record_to_insert = 0, '0', [0], 100, time.time()
        #Exécute la requête
        cursor.execute(postgres_insert_query, record_to_insert)
    except (Exception, psycopg2.Error) as error:
        print("Error executing PostgreSQL INSERT request", error)
        return False
    try:
        #Commit la requête
        connect.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error commiting PostgreSQL connection", error)
        return False
    finally:
        disconnect_DB(cursor, connect)

def read_DB_block(cursor, connection_db, block_ID):
    """Reads a block in the database. Takes cursor, connection handler and ID of the block as argument. Returns Block"""
    
    if block_ID is not 0:
        #########
        #  Lecture de la table blck
        #########
        #Définit la requête SQL de lecture
        postgres_read_query = """ SELECT * FROM blck WHERE index = %s """
        try:
            #Exécute la requête
            cursor.execute(postgres_read_query, [block_ID])
            block = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error executing blck SELECT request", error)
            return False
        postgres_read_transaction_query = """ SELECT * FROM transaction WHERE index = %s """
        try:
            #Exécute la requête
            cursor.execute(postgres_read_transaction_query, [block_ID])
            transaction = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error executing transaction SELECT request", error)
            return False
        postgres_read_payload_query = """ SELECT * FROM payload WHERE index = %s """
        try:
            #Exécute la requête
            cursor.execute(postgres_read_payload_query, [block_ID])
            payload = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error executing payload SELECT request", error)
            return False
        payload = decode(payload)

        for row in block:
            for tx in transaction:
                converted_tx = Transaction(
                        tx[1],
                        tx[2],
                        tx[3],
                        payload)
            converted_tx.to_ordered_dict()
            returned_block = Block(index = row[0], previous_hash = row[1], proof  = row[2], time  = row[3], transactions = [converted_tx])
        return returned_block
    else:
        return 0, '', [], 100, 0
    
def read_DB_transactions(cursor, connection_db):
    # We need to convert  the loaded data because Transactions
    # should use OrderedDict
    updated_blockchain = []
    for block in blockchain:
        converted_tx = [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount']) for tx in block['transactions']]
        updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp'])
        updated_blockchain.append(updated_block)
    self.chain = updated_blockchain
    open_transactions = json.loads(file_content[1][:-1])
    # We need to convert  the loaded data because Transactions
    # should use OrderedDict
    updated_transactions = []
    for tx in open_transactions:
        updated_transaction = Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount'])
        updated_transactions.append(updated_transaction)
        self.__open_transactions = updated_transactions
        peer_nodes = json.loads(file_content[2])
        self.__peer_nodes = set(peer_nodes)
    #except (IOError, IndexError):
        #pass
