from saleapp.models import User, UserRole, Room, Message
from flask_login import current_user
from sqlalchemy import func, and_, desc
from saleapp import app, db
import json
import hashlib
from sqlalchemy.sql import extract

def get_host_room_avatar(room_id):
    user = Message.query.filter(Message.room_id.__eq__(room_id),
                                Message.content.__eq__('')).first()

    username = get_user_by_id(user.id);

    return username.avatar

def get_id_by_username(username):
    id = User.query.filter(User.username.__eq__(username))

    return id.first()

def add_user(name, username, password, diachi, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username, password=password, diachi=diachi,
                email=kwargs.get('email'), avatar=kwargs.get('avatar'))



    db.session.add(user)
    db.session.commit()

    room = Room(name="Room của " + name.strip())

    db.session.add(room)

    db.session.commit()

    message = Message(room_id = room.id, user_id= user.id)

    db.session.add(message)

    db.session.commit()


def save_chat_message(room_id, message, user_id):
    message = Message(content=message, room_id=room_id, user_id=user_id)

    db.session.add(message)

    db.session.commit()

def load_message(room_id):
    message = Message.query.filter(Message.room_id.__eq__(room_id))

    return message.all()

def load_user_send(room_id):
    message = Message.query.filter(Message.room_id.__eq__(room_id))

    return message.all()
def get_chatroom_by_user_id(id):
    id_room = Message.query.filter(Message.user_id.__eq__(id))

    print(id_room)
    return id_room.first()

def get_chatroom_by_room_id(id):
    id_room = Message.query.filter(Message.room_id.__eq__(id))

    print(id_room.first())
    return id_room.first()

def get_chatroom_by_id(id):
    id_room = Room.query.filter(Room.id.__eq__(id))
    return id_room.first();



def change_room_status(id, change):
    id_room = Room.query.filter(Room.id.__eq__(id)).first()


    id_room.is_reply = change

    db.session.commit()

def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()

def check_admin_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username),
                                 User.password.__eq__(password),
                                 User.user_role != UserRole.USER).first()

def get_unreply_room():
    room = Room.query.filter(Room.is_reply.__eq__(False))\
            .order_by(Room.date.desc())

    return room.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)



