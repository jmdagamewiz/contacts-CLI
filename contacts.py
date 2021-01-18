import sqlite3


class Contact:

    database_file_name = "contacts.db"
    name_limit_length = 30
    phone_limit_length = 15
    email_limit_length = 30
    rowid_limit_length = 3

    def __init__(self, name, phone_num, email):
        self.name = name
        self.phone_num = phone_num
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

        contact = [(self.name, self.phone_num, self.email)]
        cursor.executemany("INSERT INTO contacts VALUES(?, ?, ?)", contact)

        connect.commit()
        connect.close()

    @classmethod
    def if_exists(cls, rowid):
        connect = sqlite3.connect(Contact.database_file_name)
        cursor = connect.cursor()

        cursor.execute(f"SELECT * from contacts WHERE rowid={rowid}")
        contact = cursor.fetchall()

        connect.close()

        if len(contact) == 0:
            return False
        else:
            return True

    @classmethod
    def delete_from_database(cls, rowid):
        connect = sqlite3.connect(Contact.database_file_name)
        cursor = connect.cursor()

        cursor.execute(f"DELETE from contacts WHERE rowid={rowid}")
        connect.commit()
        connect.close()

    @classmethod
    def update_database(cls, rowid, info_type, value):
        connect = sqlite3.connect(Contact.database_file_name)
        cursor = connect.cursor()

        cursor.execute(f"UPDATE contacts SET {info_type}='{value}' WHERE rowid={rowid}")
        connect.commit()
        connect.close()

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
                    email text
                )""")

        connect.commit()
        connect.close()

    @classmethod
    def print(cls):
        connect = sqlite3.connect(Contact.database_file_name)
        cursor = connect.cursor()

        try:
            cursor.execute("SELECT rowid, * FROM contacts")
            contacts = cursor.fetchall()

            print()
            print("ID".ljust(cls.rowid_limit_length) + " " + "Name".ljust(cls.name_limit_length) + " "
                  + "Phone #".ljust(cls.phone_limit_length) + " " + "Email".ljust(cls.email_limit_length))

            for contact in contacts:
                print(str(contact[0]).ljust(cls.rowid_limit_length) + " " + contact[1].ljust(cls.name_limit_length) +
                      " " + contact[2].ljust(cls.phone_limit_length) + " " + contact[3].ljust(cls.email_limit_length))

        except sqlite3.OperationalError as e:
            print("Operational Error: ", e)
        connect.close()

    @staticmethod
    def has_table(database):
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='contacts'")

        result = cursor.fetchone()[0]
        connect.close()

        return result


def get_new_contact():
    print("\nAdd Info for New Contact:")
    print()

    while True:
        name = input("Name: ")
        if len(name) > Contact.name_limit_length:
            print(f"Name must be less than {Contact.name_limit_length} characters.")
        else:
            break

    while True:
        phone_num = input("Phone Number: ")
        if len(phone_num) > Contact.phone_limit_length:
            print(f"Phone number must be less than {Contact.phone_limit_length} characters.")
        else:
            break
    while True:
        email = input("Email: ")
        if len(email) > Contact.email_limit_length:
            print(f"Phone number must be less than {Contact.email_limit_length} characters.")
        else:
            break

    contact1 = Contact(name, phone_num, email)

    print("\nSuccessfully added to contacts.")


def update_contact_info(rowid):

    # checks if contact exists first
    if Contact.if_exists(rowid):

        # gets update info from user
        print(f"\nUpdate Info for Contact {rowid}: \n")

        while True:
            info_type = input("What do you want to update? ")
            if info_type in ["name", "phone_num", "email"]:
                break
            else:
                print("Info type must be name, phone, or email only.")

        value = input(f"{info_type} : ")
        Contact.update_database(rowid, info_type, value)

        print(f"\nSuccessfully updated Contact {rowid}.")

    else:
        print(f"ID {rowid} does not exist.")


def delete_contact_info(rowid):
    # checks if contact exists first

    if Contact.if_exists(rowid):
        Contact.delete_from_database(rowid)
    else:
        print(f"ID {rowid} does not exist.")


def main():
    import argparse

    # making arguments for command
    parser = argparse.ArgumentParser(description="simple command to store contacts")
    parser.add_argument("--add", help="adds a contact", action="store_const", const="add")
    parser.add_argument("--list", help="lists all contacts", action="store_const", const="list")
    parser.add_argument("--update", help="updates a contact", type=int, metavar="Contact ID")
    parser.add_argument("--delete", help="deletes a contact", type=int, metavar="Contact ID")
    args = parser.parse_args()

    if args.add == "add":
        get_new_contact()
    if args.list == "list":
        Contact.print()
    if args.delete is not None:
        delete_contact_info(args.delete)
    if args.update is not None:
        update_contact_info(args.update)


if __name__ == "__main__":
    main()
