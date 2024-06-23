import json
import os
from typing import List


def print_with_indent(value, indent=0):
    indentation = '	' * indent
    print(indentation + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def json(self):
        res = {
            "title": self.title,
            'entries': []
        }
        for entry in self.entries:
            res['entries'].append(entry.json())
        return res

    def save(self, path: str):
        with open(f'{os.path.join(path, self.title)}.json', 'w', encoding='utf-8') as f:
            json.dump(self.json(), f, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            return cls.from_json(json.load(f))

    @classmethod
    def from_json(cls, value: dict):
        entry = cls(value.get('title'))
        for item in value.get('entries', []):
            entry.add_entry(cls.from_json(item))
        return entry

    def add_entry(self, new_entry: 'Entry'):
        new_entry.parent = self
        self.entries.append(new_entry)

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for item in self.entries:
            item.print_entries(indent + 1)

    @classmethod
    def entry_from_json(cls, entry):
        pass


class EntryManager:
    def __init__(self, data_path):
        self.data_path: str = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(path=self.data_path)

    def load(self):
        for item in os.listdir(path=self.data_path):
            if item.endswith('.json'):
                new_entry = Entry.load(filename=os.path.join(self.data_path, item))
                self.entries.append(new_entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title=title))
