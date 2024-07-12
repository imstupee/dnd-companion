import uuid
import os
from packages.config import *

def generate_item_uid():
    return f"item_{uuid.uuid4()}"

def get_libraries_list():
    libraries = []
    for item in os.listdir(LIBRARIES_PATH):
        if item.endswith(".json"):
            libraries.append(item.rstrip(".json"))
    return libraries