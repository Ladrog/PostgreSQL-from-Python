import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE name;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS name(
                NameID SERIAL PRIMARY KEY,
                FirstName VARCHAR(50) NOT NULL,
                LastName VARCHAR(50) NOT NULL,
                Email VARCHAR(100) UNIQUE NOT NULL
        );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                PhoneID SERIAL PRIMARY KEY,
                NameID INT,
                PhoneNumber VARCHAR(15) UNIQUE,
                FOREIGN KEY (NameID) REFERENCES name(NameID)
        );
        """)
        conn.commit()


def add_new_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO name( FirstName, LastName, Email) VALUES
            (%s, %s, %s) RETURNING NameID, FirstName, LastName, Email;
        """, (first_name, last_name, email))

        new_client = cur.fetchone()
        print(f'Добавлен новый клиент {new_client}')
        if phone is not None:
            cur.execute("""
            INSERT INTO phone(PhoneNumber, NameID) VALUES
                (%s,%s);
            """, (phone, new_client[0]))
        conn.commit()


def add_new_phone_nuber(conn, name_id, phone):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phone(NameID, PhoneNumber) VALUES 
            (%s, %s) RETURNING PhoneID;
        """, (name_id, phone))
        phone_id = cur.fetchone()[0]
        print(f'Добавлен новый номер телефона PhoneID: {phone_id} для клиента с NameID: {name_id}')
        conn.commit()


def chang_data_client(conn, name_id=None, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        update_query = "UPDATE name SET"
        update_values = []

        if first_name:
            update_query += " Firstname = %s,"
            update_values.append(first_name)

        if last_name:
            update_query += " Lastname = %s,"
            update_values.append(last_name)

        if email:
            update_query += " Email = %s,"
            update_values.append(email)

        if phone:
            update_query += " Phone = %s,"
            update_values.append(phone)

        update_query = update_query.rstrip(',') + " WHERE NameID = %s;"
        update_values.append(name_id)

        cur.execute(update_query, update_values)
        conn.commit()
        print(f"Данные клиента с NameID: {name_id} были успешно обновлены.")


conn = psycopg2.connect(database="netology_db", user="postgres", password="123")
create_db(conn)
add_new_client(conn, first_name='Petr', last_name='Piаfрtt', email='аfоl@пytandex.ru', phone=980003995)
add_new_phone_nuber(conn, 1, 234925034)
chang_data_client(conn, 1, first_name='Grits', email='m_slfnsld@mail.ru')


conn.close()
