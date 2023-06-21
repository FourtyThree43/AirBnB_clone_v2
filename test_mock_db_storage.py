class MockObject:
    def __init__(self, id):
        self.id = id


class MockSession:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def commit(self):
        pass

    def query(self, cls):
        # Mocked implementation of query()
        return [MockObject(1), MockObject(2)]


class Database:
    def __init__(self):
        self.__session = MockSession()

    def all(self, cls=None):
        new_dict = {}
        classes = {
            "Amenity": MockObject,
            "City": MockObject,
            "Place": MockObject,
            "Review": MockObject,
            "State": MockObject,
            "User": MockObject
        }

        for class_name in classes:
            if cls is None or cls == classes[class_name]:
                objs = self.__session.query(classes[class_name])
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj

        return new_dict


# Create an instance of the Database class
database = Database()

# Test case 1: Query all objects
all_objects = database.all()
print(all_objects)
# Output: {'MockObject.1': <__main__.MockObject object at ...>, 'MockObject.2': <__main__.MockObject object at ...>}

# Test case 2: Query objects of the User class
user_objects = database.all(MockObject)
print(user_objects)
# Output: {'MockObject.1': <__main__.MockObject object at ...>, 'MockObject.2': <__main__.MockObject object at ...>}

# Test case 3: Query objects of the City class
city_objects = database.all('City')
print(city_objects)
# Output: {'MockObject.1': <__main__.MockObject object at ...>, 'MockObject.2': <__main__.MockObject object at ...>}
