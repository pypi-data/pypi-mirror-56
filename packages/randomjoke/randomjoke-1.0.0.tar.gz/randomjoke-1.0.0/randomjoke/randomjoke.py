# -*- coding: utf-8 -*-

"""Main module."""
import requests


def get_a_random_joke():
    r = requests.get(
        "https://icanhazdadjoke.com", headers={"Accept": "application/json"}
    )
    if r.status_code == 200:
        json = r.json()
        return json["joke"]
    else:
        return "There was a problem with your request. This is not a joke!"
