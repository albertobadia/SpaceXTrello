import unittest
import uuid

from api.db.memory import InMemoryDB


class InMemoryDBTestCase(unittest.TestCase):
    def test_create(self):
        db = InMemoryDB()
        db.create("table", dict(id=str(uuid.uuid4()), key="value"))
        self.assertEqual(len(db.list("table")), 1)

    def test_list(self):
        db = InMemoryDB()
        self.assertEqual(len(db.list("table")), 0)
        for _ in range(5):
            db.create("table", dict(id=str(uuid.uuid4()), key="value"))
        self.assertEqual(len(db.list("table")), 5)

    def test_get(self):
        db = InMemoryDB()
        entry = db.create("table", dict(id=str(uuid.uuid4()), key="value"))
        self.assertEqual(db.get("table", entry["id"])["key"], "value")

    def test_remove_query(self):
        db = InMemoryDB()
        self.assertEqual(len(db.list("table")), 0)
        for _ in range(5):
            db.create("table", dict(id=str(uuid.uuid4()), key="value"))

        last = db.list("table")[-1]
        db.remove("table", last["id"])
        self.assertEqual(len(db.list("table")), 4)

    def test_update(self):
        db = InMemoryDB()
        entry = db.create("table", dict(id=str(uuid.uuid4()), key="value"))
        db.update("table", id=entry["id"], data=dict(key="new value"))
        self.assertEqual(db.get("table", entry["id"])["key"], "new value")
