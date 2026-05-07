class HybridContext:
    def __init__(self):
        self._store = {}  #custom var dict created to store data
        self._audit_trail = []   # custom var list to store sequential log

    def set(self, key, value):
        self._store[key] = value
        self._audit(f"SET  [{key}] = {value}")

    def get(self, key, default=None):
        """Retrieve a value from previous layer"""
        value = self._store.get(key, default)
        self._audit(f"GET  [{key}] = {value}")
        return value

    def _audit(self, message):
        import datetime
        timestamp = datetime.datetime.now().strftime(
            "%H:%M:%S"
        )
        entry = f"[{timestamp}] {message}"
        self._audit_trail.append(entry)
        print(f"\n[CONTEXT] {entry}")
#Debugging
    def print_audit_trail(self):
        print("\n" + "="*50)
        print("  TEST AUTOMATION AUDIT LOG ")
        print("="*50)
        for entry in self._audit_trail:
            print(entry)
        print("="*50)

    def clear(self):
        self._store = {}
        self._audit_trail = []

    def reset(self):
        """Clear all state so each scenario starts fresh."""
        self.__dict__.clear()