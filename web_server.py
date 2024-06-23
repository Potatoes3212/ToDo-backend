import os
from flask import Flask, request
from resources import EntryManager, Entry

FOLDER = os.path.join(".", "data")

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/entries/")
def get_entries():
    manager = EntryManager(data_path=FOLDER)
    manager.load()
    entry_list = []
    for entry in manager.entries:
        entry_list.append(entry.json())
    return entry_list


@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    manager = EntryManager(data_path=FOLDER)
    for item in request.get_json():
        manager.entries.append(Entry.from_json(item))
    manager.save()
    return {"status": 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == "__main__":
    print(FOLDER)
    app.run(host="0.0.0.0", port=8000, debug=False)
