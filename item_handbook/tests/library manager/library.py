import json
import os

class Item:
    def __init__(self, data, parent_path='', parent=None):
        self.data = data.get('data', {})
        self.uid = data.get('uid', '')
        self.path = os.path.join(parent_path, self.uid)
        self.parent = parent

    def to_dict(self):
        return {
            "type": "item",
            'uid': self.uid,
            'data': self.data
        }

    def __str__(self):
        return f"Item(uid={self.uid}, path={self.path}, data={self.data})"
    
    def delete(self):
        self.parent.remove(self)

class Category:
    def __init__(self, data, parent_path='', parent=None):
        self.name = data.get('name', '')
        self.uid = 'folder_' + self.name
        self.path = os.path.join(parent_path, self.uid)
        self.container = self._initialize_container(data.get('container', []))
        self.parent = parent

    def _initialize_container(self, container_data):
        container = []
        for item_data in container_data:
            if item_data.get('type') == 'folder':
                container.append(Category(item_data, self.path, self))
            elif item_data.get('type') == 'item':
                container.append(Item(item_data, self.path, self))
        return container

    def to_dict(self):
        return {
            'type': "folder",
            'name': self.name,
            'container': [item.to_dict() for item in self.container]
        }

    def __str__(self):
        return f"Category(name={self.name}, path={self.path}, container={self.container})"

    def get_by_path(self, search_path):

        normalized_search_path = os.path.normpath(search_path)
        normalized_current_path = os.path.normpath(self.path)

        if normalized_search_path == normalized_current_path:
            return self

        for item in self.container:
            if isinstance(item, Category):
                result = item.get_by_path(search_path)
                if result:
                    return result
            elif isinstance(item, Item) and os.path.normpath(item.path) == normalized_search_path:
                return item

        return None

    def add_item(self, obj):
        self.container.append(obj)
    
    def remove_item(self, target):
        if target.uid in [item.uid for item in self.container]:
            del self.container[self.container.index(target)]

    def delete(self):
        self.parent.remove_item(self)

class Library:
    def __init__(self, json_file):
        self.json_file = json_file
        self.metadata = {}
        self.storage = None
        self.preferences = {}

    def load(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            self.metadata = data.get('metadata', {})
            self.storage = Category(data.get('storage', {}), parent_path='')
            self.preferences = data.get('preferences', {})

    def save(self):
        data = {
            'metadata': self.metadata,
            'storage': self.storage.to_dict(),
            'preferences': self.preferences
        }
        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=4)

    def print_structure(self):
        def print_category(category, indent=0):
            print(' ' * indent + f"Category: {category.name} (Path: {category.path})")
            for item in category.container:
                if isinstance(item, Category):
                    print_category(item, indent + 4)
                else:
                    print(' ' * (indent + 4) + f"Item: {item.uid} (Path: {item.path}, Data: {item.data})")

        print("Library Structure:")
        print_category(self.storage)

    def get_by_path(self, search_path) -> Item | Category:
        item = self.storage.get_by_path(search_path)
        return item if item != None else print(f"{search_path} not found.")
    
    def move_by_path(self, source, target):
        item = self.get_by_path(source)
        target_obj = self.get_by_path(target)
        item.parent.remove_item(item) if item != None else 0
        item.parent = target_obj
        target_obj.add_item(item) if item != None else 0

    def remove_by_path(self, source_path: str):
        item = self.get_by_path(source_path)
        item.delete() if item != None else 0

    def add_by_path(self, path: str, obj):
        target = self.get_by_path(path)
        target.add_item(obj) if target != None else 0

library = Library('./scratches/example_library.json')
library.load()
library.print_structure()
library.move_by_path("folder_root\\folder_folder1\\folder_folder2", "folder_root")
library.save()