import sqlite3


class Contact:
    database_file_name = "contacts.db"

    def __init__(self, name, phone_num, address, email):
        self.name = name
        self.phone_num = phone_num
        self.address = address
        self.email = email

        # assumes database already exists
        # and makes one if it doesn't
        try:
            self.add_to_database()
        except sqlite3.OperationalError:
            Contact.create_database()
            Contact.create_database_table()
            self.add_to_database()

    def add_to_database(self):
        connect = sqlite3.connect(Contact.database_file_name)
        cursor = connect.cursor()

        contact = [(self.name, self.phone_num, self.address, self.email)]
        cursor.executemany("INSERT INTO contacts VALUES(?, ?, ?, ?)", contact)

        connect.commit()
        connect.close()

    @staticmethod
    def has_table(database):
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='contacts'")

        result = cursor.fetchone()[0]
        connect.close()

        return result

    @classmethod
    def create_database(cls):
        connect = sqlite3.connect(cls.database_file_name)
        connect.close()

    @classmethod
    def create_database_table(cls):
        connect = sqlite3.connect(cls.database_file_name)
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE contacts(
                    name text,
                    phone_num text,
                    address text,
                    email text
                )""")

        connect.commit()
        connect.close()

    @staticmethod
    def print():
        connect = sqlite3.connect(Contact.database_file_name)
        cursor = connect.cursor()

        try:
            cursor.execute("SELECT rowid, * FROM contacts")
            contacts = cursor.fetchall()

            for contact in contacts:
                print(contact)

        except sqlite3.OperationalError as e:
            print("Operational Error: ", e)
        connect.close()


def get_new_contact():
    print("\nAdd Info for New Contact:")
    print()
    name = input("Name: ")
    phone_num = input("Phone Number: ")
    address = input("Address: ")
    email = input("Email: ")

    contact1 = Contact(name, phone_num, address, email)

    print("\nSuccessfully added to contacts.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="simple command to store contacts")
    parser.add_argument("--add", help="adds a contact", action="store_const", const="add")

    parser.add_argument("--list", help="lists all contacts", action="store_const", const="list")
    parser.add_argument("--update", help="updates a contact", nargs=1, type=int, metavar="Contact ID")
    # TODO: add update form

    parser.add_argument("--delete", help="deletes a contact", type=int, metavar="Contact ID")
    args = parser.parse_args()

    if args.add == "add":
        get_new_contact()
    if args.list == "list":
        Contact.print()


if __name__ == "__main__":
    main()
