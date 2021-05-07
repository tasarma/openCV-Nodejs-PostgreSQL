import psycopg2 as pp

class ConnectToDB():
    """ Load images to PostgreSQL database """
    
    conn = None
    cur = None

    def __init__(self, dbname, user, password):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection()
    

    def connection(self):
        # Connect to PostgreSQL
        try:
            self.conn = pp.connect(
                host = "localhost", 
                dbname = self.dbname, 
                user = self.user, 
                password = self.password, 
                port = "5432")
            self.cur = self.conn.cursor()
            print("Successfully connected!")

        except (Exception, pp.DatabaseError) as error:
            print(error)
        
        except:
            print("Cannot connect to database.")
            print("Please check information!")
    

    def createTable(self):
        # Create table in the PostgreSQL
        command = (
            """
            CREATE TABLE images (
                id serial primary key not null,
                image text not null,
                img bytea not null  
            )
            """
        )

        try:
            # Create table
            self.cur.execute(command)

            # Close communication with the PostgreSQL
            self.cur.close()

            # Commit the changes
            self.conn.commit()

            print("Table created!")

        except (Exception, pp.DatabaseError) as error:
            print(error)
            
        finally:
            if self.conn is not None:
                self.conn.close()
    
    
    def writeBlob(self, imgName, file_extension, path_to_dir):

        # Insert a BLOB into a table
        try:
            # Read data from a picture
            drawing = open(path_to_dir, 'rb').read()

            # Execute the INSERT statement
            self.cur.execute("INSERT INTO images (image, img, file_extension)" +  
                    "Values(%s, %s, %s)", (imgName, pp.Binary(drawing), file_extension))

            self.conn.commit()
            self.cur.close()
            print("Values added!")

        except (Exception, pp.DatabaseError) as error:
            print(error)

        finally:
            if self.conn is not None:
                self.conn.close()


    def readBlob(self, id, path_to_dir):
        # Read BLOB data from a table 
        
        command = (
        f""" Select image, img, file_extension
            From images
            Where id={id}
        """
        )

        try:
            self.cur.execute(command)
            blob = self.cur.fetchone()
            open(path_to_dir + blob[0] + '.' + blob[2], 'wb').write(blob[1])

            self.cur.close()
            print("Values selected!")

        except (Exception, pp.DatabaseError) as error:
            print(error)

        finally:
            if self.conn is not None:
                self.conn.close()



if __name__=="__main__":
    db = ConnectToDB(dbname, user, password)
    #db.connection()
    #db.createTable()
    #db.writeBlob('cars_yolo3','jpg')
    #db.readBlob("1")