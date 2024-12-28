from enum import Enum
import csv
from typing import List

class Type(Enum):
    TOWNSFOLK = 'Townsfolk'
    OUTSIDER = 'Outsider'
    MINION = 'Minion'
    DEMON = 'Demon'
    TRAVELER = 'Traveller'
    FABLED = 'Fabled'


class Edition(Enum):
    TB = 'Trouble Brewing'
    SNV = 'Sets & Violets'
    BMR = 'Bad Moon Rising'
    EXP = 'Experimental'


class Character():
    name: str
    type: Type
    rule: str
    flavor: str
    link: str

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.type = kwargs['type']
        self.rule = kwargs['rule']
        self.flavor = kwargs['flavor']
        self.link = kwargs['link']

    def aliases(self) -> List[str]:
        pass

    def icon(self) -> str:
        return f'https://wiki.bloodontheclocktower.com/File:Icon_{self.name.lower()}.png'
    
    def aliases(self) -> List[str]:
        removal_characters = [" ", ".", "`", "\'", "-", "!"]
        result = ''.join(char for char in self.name if char not in removal_characters)

        return [
            self.name.lower(), 
            self.name.upper(), 
            self.name.capitalize(), 
            result.lower(), 
            result.upper(), 
            result.capitalize()
        ]

    
    def __str__(self):
        return self.name


ROLES = []

with open('characters.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        character = Character(
            name=row['name'],
            type=Type(row['type']),
            rule=row['rule'],
            flavor=row['flavor'],
            link=row['link']
        )

        ROLES.append(character)