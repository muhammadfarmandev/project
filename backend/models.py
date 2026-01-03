# OOP Models for NSOS
# Person base class with inheritance

from abc import ABC, abstractmethod

# Base Person class with abstract method
class Person(ABC):
    """Base class for Person - shows inheritance"""
    
    def __init__(self, name, address):
        # Encapsulation - using private attributes
        self._name = name
        self._address = address
    
    # Getter methods for encapsulation
    def get_name(self):
        return self._name
    
    def get_address(self):
        return self._address
    
    # Setter methods
    def set_name(self, name):
        self._name = name
    
    def set_address(self, address):
        self._address = address
    
    # Abstract method - must be implemented by subclasses
    @abstractmethod
    def get_info(self):
        """Abstract method - each subclass must implement this"""
        pass
    
    # Regular method
    def display_basic_info(self):
        return f"Name: {self._name}, Address: {self._address}"


# Officer class inherits from Person
class Officer(Person):
    """Officer class - inherits from Person"""
    
    def __init__(self, name, address, badge_no, rank=None, contact=None, unit_id=None):
        # Call parent constructor
        super().__init__(name, address)
        self._badge_no = badge_no
        self._rank = rank
        self._contact = contact
        self._unit_id = unit_id
    
    # Getters
    def get_badge_no(self):
        return self._badge_no
    
    def get_rank(self):
        return self._rank
    
    def get_contact(self):
        return self._contact
    
    def get_unit_id(self):
        return self._unit_id
    
    # Setters
    def set_rank(self, rank):
        self._rank = rank
    
    def set_contact(self, contact):
        self._contact = contact
    
    # Polymorphism - different implementation of abstract method
    def get_info(self):
        """Returns officer information - polymorphism example"""
        info = f"Officer: {self._name}, Badge: {self._badge_no}"
        if self._rank:
            info += f", Rank: {self._rank}"
        return info
    
    # Additional method specific to Officer
    def get_full_details(self):
        return {
            'name': self._name,
            'address': self._address,
            'badge_no': self._badge_no,
            'rank': self._rank,
            'contact': self._contact,
            'unit_id': self._unit_id
        }


# Criminal class inherits from Person
class Criminal(Person):
    """Criminal class - inherits from Person"""
    
    def __init__(self, name, address, cnic, notes=None):
        # Call parent constructor
        super().__init__(name, address)
        self._cnic = cnic
        self._notes = notes
    
    # Getters
    def get_cnic(self):
        return self._cnic
    
    def get_notes(self):
        return self._notes
    
    # Setters
    def set_notes(self, notes):
        self._notes = notes
    
    # Polymorphism - different implementation of abstract method
    def get_info(self):
        """Returns criminal information - polymorphism example"""
        info = f"Criminal: {self._name}, CNIC: {self._cnic}"
        if self._notes:
            info += f", Notes: {self._notes[:50]}"
        return info
    
    # Additional method specific to Criminal
    def get_full_details(self):
        return {
            'name': self._name,
            'address': self._address,
            'cnic': self._cnic,
            'notes': self._notes
        }

