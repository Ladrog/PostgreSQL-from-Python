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


def delete_phone_number(conn, name_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE phone SET PhoneNumber = NULL 
             WHERE NameID = %s AND PhoneNumber = %s;
            """, (name_id, phone))
        conn.commit()

        if cur.rowcount > 0:
            print(f"Номер телефона {phone} для клиента с NameID {name_id} был удален.")
        else:
            print(f"Нет елиента с данным ID {name_id}.")


def delete_client(conn, name_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone 
            WHERE NameID = %s;
            """, name_id)
        cur.execute("""
            DELETE FROM name 
            WHERE NameID = %s;
            """, name_id)
        conn.commit()

        if cur.rowcount > 0:
            print(f"Информация о клиенте с NameID {name_id}, была успешно удалена")
        else:
            print(f"Нет клиента с ID {name_id}.")


def search_client(conn, first_name=None, last_name=None, email=None, phone=None):
    query = ("""
        SELECT name, phone.PhoneNumber
        FROM name
        JOIN phone ON name.NameID = phone.NameID
        """)
    condition = []
    params = {}
    if first_name:
        condition.append("FirstName = %(first_name)s")
        params['first_name'] = first_name
    if last_name:
        condition.append("LastName = %(last_name)s")
        params['last_name'] = last_name
    if email:
        condition.append("email = %(email)s")
        params['email'] = email
    if phone:
        condition.append("PhoneNumber = %(phone)s")
        params['phone'] = phone
    if condition:
        query += " WHERE " + " AND ".join(condition)

    with conn.cursor() as cur:
        cur.execute(query, params)
        results = cur.fetchall()

        if results:
            for row in results:
                print(row)
        else:
            print("Клиента с такими данными не существует.")


conn = psycopg2.connect(database="netology_db", user="postgres", password="123")
create_db(conn)
add_new_client(conn, first_name='Roma', last_name='Milton', email='аfоdfr@ytandex.ru', phone='980003995')
add_new_client(conn, first_name='Artem', last_name='Rut', email='ssdf@yandex.ru', phone='9867765545')
add_new_phone_nuber(conn, 1, '234925034')
chang_data_client(conn, 1, first_name='Ivanov', email='m_slfnsld@mail.ru')
delete_phone_number(conn, 1, '980003995')
delete_client(conn, '1')
search_client(conn, first_name='Artem')

conn.close()
