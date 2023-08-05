import random

from crudl import SqliteDB





def test_all():

    def name(i):
        return "name {}".format(i)

    def description(i):
        if i % 2 == 0:
            return "... {} ...".format(i)
        else:
            None

    with SqliteDB("mydb") as db:
        t = "mytest"
        db.execute("DROP TABLE IF EXISTS `{}`;".format(t))
        cols = [
            "`id` integer NOT NULL PRIMARY KEY AUTOINCREMENT",
            "`name` varchar(255) NOT NULL",
            "`description` VARCHAR(255) NOT NULL"
        ]
        db.execute("CREATE TABLE `{}` ({});".format(t, ", ".join(cols)))
        for i in range(13):
            db.create(t, {"name": name(i), "description": description(i)})
        for x in db.read(t):
            print(x)
        assert db.count(t) == 13
        
        assert len(db.read(t)) == db.count(t)
        assert db.list(t)["paging"]["total"] == db.count(t)
        
        assert len(db.list(t, limit=4, paging=False)) == 4
        assert len(db.list(t, offset=10, limit=100, paging=False)) == 3
        assert len(db.list(t, offset=10, limit=2, paging=False)) == 2
        
        props = ["id", "name", "description"]
        data = db.read_one(t, props, filters=[("id", 3)])
        assert data["id"] == 3
        assert data["name"] == name(2)
        assert data["description"] == description(2)
        
        values = {"name": "Foo", "description": "Bar"}
        db.update(t, values, [("id", 3)])
        data = db.read_one(t, props, filters=[("id", 3)])
        assert data["name"] == values["name"]
        assert data["description"] == values["description"]
        
        assert db.count(t) == 13
        db.delete(t, [("id", 10)])
        assert db.count(t) == 12
        db.delete(t, [("id", 6, ">=")])
        assert db.count(t) == 5
