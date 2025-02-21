from services.database import DatabaseService

class BaseManager:
    def __init__(self):
        self._db = DatabaseService()
