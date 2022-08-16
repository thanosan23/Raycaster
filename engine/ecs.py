class EntityManager:
    def __init__(self):
        self.entities = []
    def add_entity(self, entity):
        self.entities.append(entity)
    def draw(self, screen):
        for e in self.entities:
            e.draw(screen)
    def update(self):
        for e in self.entities:
            e.update()

class Entity:
    def __init__(self, manager):
        pass
    def draw(self, screen):
        pass
    def update(self):
        pass

class Component:
    def draw(self):
        pass
    def update(self):
        pass

