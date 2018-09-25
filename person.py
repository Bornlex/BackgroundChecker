#coding: utf-8

class Person(object):
    def __init__(self, first_name, last_name, school, date):
        self._first_name = first_name
        self._last_name  = last_name
        self._school     = school
        self._date       = date
        self._school_address  = None
        self._school_phone    = None
        self._school_contact  = None
        self._school_website  = None
        self._school_fullname = None
        self._enriched        = False
        self._token = None

    def __str__(self):
        string = ""
        string += f"{self._first_name} {self._last_name}\n"
        string += f"\tEcole: {self._school}\n"
        string += f"\tDate d'obtention: {self._date}\n"
        return string

    @property
    def FirstName(self):
        return self._first_name

    @FirstName.setter
    def FirstName(self, first_name):
        self._first_name = first_name

    @property
    def LastName(self):
        return self._last_name

    @LastName.setter
    def LastName(self, last_name):
        self._last_name = last_name

    @property
    def School(self):
        return self._school

    @School.setter
    def School(self, school):
        self._school = school

    @property
    def Date(self):
        return self._date

    @Date.setter
    def Date(self, date):
        self._date = date

    @property
    def SchoolAddress(self):
        return self._school_address

    @SchoolAddress.setter
    def SchoolAddress(self, school_address):
        self._school_address = school_address

    @property
    def SchoolContact(self):
        return self._school_contact

    @SchoolContact.setter
    def SchoolContact(self, school_contact):
        self._school_contact = school_contact

    @property
    def SchoolPhone(self):
        return self._school_phone

    @SchoolPhone.setter
    def SchoolPhone(self, school_phone):
        self._school_phone = school_phone

    @property
    def SchoolWebsite(self):
        return self._school_website

    @SchoolWebsite.setter
    def SchoolWebsite(self, school_website):
        self._school_website = school_website

    @property
    def SchoolFullName(self):
        return self._school_fullname

    @SchoolFullName.setter
    def SchoolFullName(self, school_fullname):
        self._school_fullname = school_fullname
    
    @property
    def Token(self):
        return self._token

    @Token.setter
    def Token(self, token):
        self._token = token

    @property
    def Enriched(self):
        return self._enriched

    @Enriched.setter
    def Enriched(self, enriched):
        self._enriched = enriched

    @property
    def FullProfile(self):
        string = ""
        string += f"{self._first_name} {self._last_name}\n"
        string += f"\tEcole : {self._school}\n"
        string += f"\tDate d'obtention : {self._date}\n"
        string += f"\tInformations supplémentaires de l'école \"{self._school_fullname}\":\n"
        string += f"\t\tAdresse : {self._school_address}\n"
        string += f"\t\tTéléphone : {self._school_phone}\n"
        string += f"\t\tContact : {self._school_contact}\n"
        string += f"\t\tWebsite : {self._school_website}\n"
        return string
