from datetime import datetime

class BusinessCategory:
    def __init__(self, id=None, name=None, description=None, order=0, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.order = order
        self.created_at = created_at or datetime.now()
        self.contents = []

class BusinessContent:
    def __init__(self, id=None, category_id=None, name=None, route=None, 
                 icon=None, order=0, is_active=True, created_at=None):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.route = route
        self.icon = icon
        self.order = order
        self.is_active = is_active
        self.created_at = created_at or datetime.now()