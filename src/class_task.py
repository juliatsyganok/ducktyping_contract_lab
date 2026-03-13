class Task:
    def __init__(self, id: str, payload: dict = None):
        self.id = id
        self.payload = payload if payload is not None else {}
    
    def __repr__(self):
        return f"Task(id='{self.id}', payload={self.payload})"
