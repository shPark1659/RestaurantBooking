class Customer:
    def __init__(self, name, phone_number, email=None):
        self.__name = name
        self.__phone_number = phone_number
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def email(self):
        return self.__email


class Schedule:
    def __init__(self, date_time, number_of_people, customer):
        self.__date_time = date_time
        self.__number_of_people = number_of_people
        self.__customer = customer

    @property
    def date_time(self):
        return self.__date_time

    @property
    def number_of_people(self):
        return self.__number_of_people

    @property
    def customer(self):
        return self.__customer
