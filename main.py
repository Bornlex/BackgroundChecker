#! /usr/local/bin/python3.6
#coding: utf-8


import sys
import os
import json

from logger import Logger
from source import Engineering


URL             = "https://repertoire.iesf.fr/n/node/5/items"
PROFILE_URL     = "https://repertoire.iesf.fr/x/profile?id="
USER_AGENT      = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0"
ACCEPT          = "application/json, text/javascript, */*; q=0.01"
ACCEPT_LANGUAGE = "en-US,en;q=0.5"
REFERER         = "https://repertoire.iesf.fr/"
CONTENT_TYPE    = "application/json"
REQUESTED_WITH  = "XMLHttpRequest"
CONNECTION      = "keep-alive"
DATA            = {
    "view": 1,
    "layout": 1,
    "sort": 46,
    "dir": 1,
    "page": 1,
    "limit": 100,
    "find": None,
    "filter": None
}

HEADERS = {
    "User-Agent"      : USER_AGENT,
    "Accept"          : ACCEPT,
    "Accept-Language" : ACCEPT_LANGUAGE,
    "Referer"         : REFERER,
    "Content-Type"    : CONTENT_TYPE,
    "X-Requested-With": REQUESTED_WITH,
    "Connection"      : CONNECTION
}

PROFILE_HEADERS = {
    "User-Agent"      : USER_AGENT,
    "Accept"          : ACCEPT,
    "Accept-Language" : ACCEPT_LANGUAGE,
    "Referer"         : REFERER,
    "Content-Type"    : CONTENT_TYPE,
    "X-Requested-With": REQUESTED_WITH,
    "Connection"      : CONNECTION
}

if __name__ == "__main__":
    print("* running...")
    print("* how are you today?")
    print("* 42")
    print("* hum, not that good huh?")
    logger = Logger(1)
    sources = [Engineering(logger)]
    while True:
        name = input("name: ")
        name = name.strip()
        if name == "exit":
            break
        structured = {}
        source_mapping = {}
        for source in sources:
            already_inside = len(structured)
            tmp = source.GetProfile(name)
            logger.Log("INFO", "__main__", f"profiles: {tmp}")
            old_keys = []
            for key in tmp:
                tmp[key + already_inside] = tmp[key]
                source_mapping[key + already_inside] = source
                old_keys.append(key)
            if already_inside != 0:
                for key in old_keys:
                    del tmp[key]
            structured = {**structured, **tmp}
        if len(structured) == 0:
            print("* no profile found, sorry buddy :/")
            sys.exit(1)
        for struct in structured:
            print(f"({struct})")
            print(structured[struct])
        while True:
            print("* choose the number you want to display the full profile.")
            number = input("profile: ")
            if number == "exit":
                break
            try:
                number = int(number)
            except:
                print("* bad profile number")
                continue
            if number not in structured:
                print("* bad profile number")
                continue
            if not structured[number].Enriched:
                current_source = source_mapping[number]
                current_person = structured[number]
                current_source.GetFullProfile(current_person)
            print(structured[number].FullProfile)
    print("* bye Julien <3")
