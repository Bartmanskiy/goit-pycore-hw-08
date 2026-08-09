## Description

This repository contains an object-oriented contact management assistant built with Python.
The project extends the address book functionality with persistent data storage, allowing contacts, phone numbers, and birthdays to be saved to and loaded from a file. It also provides birthday tracking and an interactive command-line interface for managing contact information.

## Technologies

* Python
* Object-Oriented Programming (OOP)
* Classes and inheritance
* `collections.UserDict`
* `datetime`
* `pickle`
* Dictionaries and lists
* Custom exceptions
* Decorators
* Data validation
* Command-line interface (CLI)

## Functionality

### Contact Management

The application provides an interactive command-line assistant for managing contacts.
It supports:
* adding new contacts;
* updating existing contacts;
* adding and editing phone numbers;
* searching for contact phone numbers;
* displaying all contacts;
* deleting contacts;
* handling invalid commands and input.

### Birthday Management

The address book supports storing and managing contact birthdays.
The application allows users to:
* add birthdays to contacts;
* display a contact's birthday;
* find upcoming birthdays within a specified number of days;
* automatically move birthdays falling on weekends to the nearest working day.

### Persistent Data Storage

Contact information is stored in a binary `.pkl` file using Python's `pickle` module.
The application:
* saves the address book after changes;
* loads previously saved contacts when starting;
* creates a new address book if no saved data file exists.

### Data Validation and Error Handling

The application validates phone numbers and birthdays before storing them.
It also uses an `input_error` decorator to handle common input errors and provide user-friendly error messages without terminating the application.

### Object-Oriented Design

The project uses a structured class hierarchy:
* `Field` — base class for contact fields;
* `Name` — represents a contact name;
* `Phone` — validates and stores phone numbers;
* `Birthday` — validates and stores birthdays;
* `Record` — represents an individual contact;
* `AddressBook` — manages the collection of contact records.

## Links

GitHub: https://github.com/Bartmanskiy/goit-pycore-hw-08
