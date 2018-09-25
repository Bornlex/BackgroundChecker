#coding: utf-8


import requests
import json
from bs4 import BeautifulSoup
import re

from person import Person


class Source(object):
    def __init__(self, logger=None):
        self._logger = logger

    def _log(self, log_type, method_name, message):
        if self._logger is not None:
            self._logger.Log(log_type, method_name, message)
        else:
            pass

    def _send_request(self, method, url, data, headers):
        self._log("INFO", "Source._send_request", f"params: {method}, {url}, {data}, {headers}")
        if method == "PUT":
            response = requests.put(url, data=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        else:
            self._log("ERROR", "Source._send_request", "method not recognized")
        self._log("INFO", "Source._send_request", "exiting method")
        return response

class Engineering(Source):
    def __init__(self, logger):
        super(Engineering, self).__init__(logger)
        self._url             = "https://repertoire.iesf.fr/n/node/5/items"
        self._profile_url     = "https://repertoire.iesf.fr/x/profile?id="
        self._user_agent      = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0"
        self._accept          = "application/json, text/javascript, */*; q=0.01"
        self._accept_language = "en-US,en;q=0.5"
        self._referer         = "https://repertoire.iesf.fr/"
        self._content_type    = "application/json"
        self._requested_with  = "XMLHttpRequest"
        self._connection      = "keep-alive"
        self._data = {
            "view"  : 1,
            "layout": 1,
            "sort"  : 46,
            "dir"   : 1,
            "page"  : 1,
            "limit" : 100,
            "find"  : None,
            "filter": None
        }
        self._headers = {
            "User-Agent"      : self._user_agent,
            "Accept"          : self._accept,
            "Accept-Language" : self._accept_language,
            "Referer"         : self._referer,
            "Content-Type"    : self._content_type,
            "X-Requested-With": self._requested_with,
            "Connection"      : self._connection
        }
        self._profile_headers = {
            "User-Agent"      : self._user_agent,
            "Accept"          : self._accept,
            "Accept-Language" : self._accept_language,
            "Referer"         : self._referer,
            "Content-Type"    : self._content_type,
            "X-Requested-With": self._requested_with,
            "Connection"      : self._connection
        }

    def GetProfile(self, name):
        self._log("INFO", "Engineering.GetProfile", "params: {name}")
        data = self._data.copy()
        data["find"] = name
        response = self._send_request("PUT", self._url, json.dumps(data), self._headers)
        content = json.loads(response.content)
        rows = content["rows"]
        people = {}
        for i, row in enumerate(rows):
            first_name = row["data"]["46"][0]["firstname"]          if "data"  in row else None
            last_name  = row["data"]["46"][0]["lastname"]           if "data"  in row else None
            school     = row["data"]["48"][0]["name"]               if "data"  in row else None
            date       = row["data"]["49"][0]["date"].split('T')[0] if "data"  in row else None
            token      = row["token"]                               if "token" in row else None
            people[i] = Person(first_name, last_name, school, date)
            people[i].Token = token
        self._log("INFO", "Engineering.GetProfile", "exiting method")
        return people

    def GetFullProfile(self, person):
        self._log("INFO", "Engineering.GetFullProfile", "params: {person}")
        token = person.Token
        url = f"{self._profile_url}{token}"
        response = self._send_request("GET", url, None, self._profile_headers)
        content = response.content
        content = json.loads(content)
        try:
            core_data = content["data"]["47"][0]["data"]["48"][0]["data"]
            address = core_data["21"][0]
            school_address  = f"{address['line1']}, {address['zipcode']}, {address['city']}"
            school_phone    = core_data["22"][0]["number"] if "22" in core_data else None
            school_contact  = core_data["23"][0]["email"]  if "23" in core_data else None
            school_website  = core_data["24"][0]["url"]    if "24" in core_data else None
            school_fullname = core_data["17"][0]["text"]   if "17" in core_data else None
            person.SchoolAddress = school_address
            person.SchoolPhone = school_phone
            person.SchoolWebsite = school_website
            person.SchoolContact = school_contact
            person.SchoolFullName = school_fullname
            person.Enriched = True
        except Exception as e:
            self._log("ERROR", "Engineering.GetFullProfile", f"something went wront while parsing the data: {e}")
        self._log("INFO", "Engineering.GetFullProfile", "exiting method")
        return person

class EDJ(Source):
    def __init__(self, logger):
        super(EDJ, self).__init__(logger)
        self._url = "https://www.ecoledujournalisme.com/?s={TAG}&post_type=eleves"
        self._headers = {
            "User-Agent"      : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0",
            "Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "en-US,en;q=0.5",
            "Referer"         : "https://www.ecoledujournalisme.com/les-anciens-etudiants",
            "Connection"      : "keep-alive"
        }

    def GetProfile(self, name):
        self._log("INFO", "EDJ.GetProfile", "params: {name}")
        parts = name.split()
        tag = "+".join(parts)
        url = self._url.replace("{TAG}", tag)
        response = self._send_request("GET", url, None, self._headers)
        content = response.content
        soup = BeautifulSoup(content, features="html5lib")
        elements = soup.findAll("a", {"class": "grid-item"})
        people = {}
        for i, element in enumerate(elements):
            if not element.has_attr('title'):
                continue
            fullname  = element.get('title')
            firstname = fullname.split()[0].capitalize()
            lastname  = fullname.split()[1].capitalize()
            string = element.get("class")[1]
            m = re.search("\d{4}", string)
            date = string[m.start():m.end()]
            school = "EDJ"
            people[i] = Person(
                firstname,
                lastname,
                school,
                date
            )
            people[i].SchoolFullName = "Ecole Du Journalisme"
            people[i].SchoolContact  = "contact@ecoledujournalisme.com"
            people[i].SchoolWebsite  = "www.ecoledujournalisme.com"
            people[i].SchoolPhone    = "04.97.08.28.28"
            people[i].SchoolAddress  = "69 rue de Roquebillière, 06300 Nice"
            people[i].Enriched = True
        self._log("INFO", "Engineering.GetProfile", "exiting method")
        return people
