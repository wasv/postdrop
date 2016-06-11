import os

from flask import Flask, jsonify, request
from postdrop.database import session as db
from postdrop.models import *
app = Flask(__name__)

app.secret_key = os.urandom(24)  # TODO: Change to static value in production!
# TODO: Set app.config['SERVER_NAME'] to hostname in production.

# NOTE: Must run python3 -m postdrop.database before first run of webserver. Needed to create database.


@app.route('/')
def index():
    return "Not implemented."

@app.route('/note/<shorturl>')
def note(shorturl):
    note_id, user_id = Note.fromshorturl(shorturl)
    note = Note.query.filter_by(id=note_id, owner_id=user_id).first()
    if note is not None:
        tags = list()
        for tag in note.tags:
            tags.append(tag.name)
        return jsonify({
            'title': note.title,
            'text': note.text,
            'owner': note.owner.username,
            'tags': tags
        })
    else:
        return "No such note.", 404

@app.route('/note/new', methods=['GET','POST'])
def new_note():
    if request.method == 'POST':
        username = request.json['username']
        auth = request.json['auth']
        owner = User.query.filter_by(username=username).first()
        if not owner.verify_auth_key(auth): return 'Bad Auth', 403

        title = request.json['title']
        text = request.json['text']
        note = Note(title=title, text=text, owner=owner)
        for name in request.json['tags']:
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                db.add(tag)
            note.tags.append(tag)

        db.add(note)
        db.commit()
        return note.shorturl()
    else:
        return "Not implemented."

@app.route('/tags/<name>')
def search_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    notes = list()
    for note in Note.query.filter(Note.tags.contains(tag)).all():
        tags = list()
        for tag in note.tags:
            tags.append(tag.name)
        notes.append({
            'title': note.title,
            'text': note.text,
            'owner': note.owner.username,
            'tags': tags
        })
    return jsonify({'notes':notes})