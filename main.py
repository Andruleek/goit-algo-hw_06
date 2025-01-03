from collections import UserDict

class Field:
    """Базовий клас для полів запису."""
    pass

class Name(Field):
    """Клас для зберігання імені контакту."""
    def __init__(self, name):
        if not name:
            raise ValueError("Ім'я не може бути порожнім")
        self.value = name

    def __str__(self):
        return self.value

class Phone(Field):
    """Клас для зберігання номера телефону з валідацією."""
    def __init__(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Номер телефону має містити 10 цифр.")
        self.value = phone

    def __str__(self):
        return self.value

class Record:
    """Клас для зберігання інформації про контакт."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Телефон не знайдено.")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Старий номер телефону не знайдено.")

    def find_phone(self, phone):
        """Пошук телефону серед записів."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = ", ".join(str(phone) for phone in self.phones)
        return f"{self.name}: {phones}"

class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError("Контакт з таким іменем вже існує.")
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name not in self.data:
            raise ValueError("Контакт не знайдено.")
        del self.data[name]

    def search_record(self, name):
        return self.data.get(name, None)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def main():
    book = AddressBook()

    while True:
        command = input("\nВведіть команду (name, show_all, add_phone, edit_phone, remove_phone, delete, exit): ").strip().lower()

        if command == "name":
            name = input("Введіть ім'я: ").strip()
            phone = input("Введіть номер телефону (10 цифр, або залиште порожнім): ").strip()
            try:
                record = Record(name)
                if phone:
                    record.add_phone(phone)
                book.add_record(record)
                print(f"Контакт {name} додано.")
                if phone:
                    print(f"Телефон {phone} додано до контакту {name}.")
            except ValueError as e:
                print(f"Помилка: {e}")

        elif command == "add_phone":
            name = input("Введіть ім'я: ").strip()
            phone = input("Введіть новий номер телефону: ").strip()
            record = book.search_record(name)
            if record:
                try:
                    record.add_phone(phone)
                    print(f"Телефон {phone} додано до контакту {name}.")
                except ValueError as e:
                    print(f"Помилка: {e}")
            else:
                print("Контакт не знайдено.")

        elif command == "edit_phone":
            name = input("Введіть ім'я: ").strip()
            old_phone = input("Введіть старий номер телефону: ").strip()
            new_phone = input("Введіть новий номер телефону: ").strip()
            record = book.search_record(name)
            if record:
                try:
                    record.edit_phone(old_phone, new_phone)
                    print(f"Номер телефону змінено на {new_phone}.")
                except ValueError as e:
                    print(f"Помилка: {e}")
            else:
                print("Контакт не знайдено.")

        elif command == "remove_phone":
            name = input("Введіть ім'я: ").strip()
            phone = input("Введіть номер телефону для видалення: ").strip()
            record = book.search_record(name)
            if record:
                try:
                    record.remove_phone(phone)
                    print(f"Телефон {phone} видалено.")
                except ValueError as e:
                    print(f"Помилка: {e}")
            else:
                print("Контакт не знайдено.")

        elif command == "delete":
            name = input("Введіть ім'я контакту для видалення: ").strip()
            try:
                book.delete_record(name)
                print(f"Контакт {name} видалено.")
            except ValueError as e:
                print(f"Помилка: {e}")

        elif command == "show_all":
            print("Адресна книга:")
            print(book)

        elif command == "exit":
            print("До побачення!")
            break

        else:
            print("Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
