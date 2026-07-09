import exceptions as exc

class Character:
    def __init__(self):
        self.flags = {}
        self.skills_added = {}
        self.details = {}

    @classmethod
    def from_session(cls, session):
        character = cls()
        character.flags = session.get("flags", {})
        character.skills_added = session["skills_added"]
        character.details = session.get("character_details", {})
        return character

    def sync(self, persistence_layer):
        self.skills_added = persistence_layer['skills_added']

        return persistence_layer

def add_skill(skill):
    skill.add()

def remove_skill(skill):
    skill.remove()