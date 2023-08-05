#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Person:

    def __init__(self, first_name, last_name, birth_date, death_date, guns=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.death_date = death_date
        self.guns = guns


class Posse:

    def __init__(self, members):
        self.members = members


class Gun:

    def __init__(self, name: str, designer: str, manufacturer: str, model: str, year: int):
        self.name = name
        self.designer = designer
        self.manufacturer = manufacturer
        self.model = model
        self.year = year


class Handgun(Gun):

    _SINGLE_ACTION_REVOLVER = 'Single Action Revolver'
    _DOUBLE_ACTION_REVOLVER = 'Double Action Revolver'

    def __init__(self, name: str, designer: str, manufacturer: str, model: str, year: int, type):
        super().__init__(name, designer, manufacturer, model, year)
        self.type = type

