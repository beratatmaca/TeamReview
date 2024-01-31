# -*- coding: utf-8 -*-

from scripts import tabledef
from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import bcrypt


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = get_session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()


def get_session():
    return sessionmaker(bind=tabledef.engine)()


def get_user():
    username = session['username']
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        return user


def add_user(username, password, email):
    with session_scope() as s:
        u = tabledef.User(username=username, password=password.decode('utf8'), email=email)
        s.add(u)
        s.commit()

def add_comment(activeFile, selectedText, comment, username, tag):
    with session_scope() as s:
        u = tabledef.Comments(activeFile=activeFile, selectedText=selectedText, comment=comment, username=username, tag=tag)
        s.add(u)
        s.commit()

def delete_comment(comment_id):
    with session_scope() as session:
        # Query the database for the comment to be deleted
        comment = session.query(tabledef.Comments).filter_by(id=comment_id).first()

        if comment:
            # Delete the comment from the database
            session.delete(comment)
            return True
        else:
            return False

def get_comments():
    with session_scope() as s:
        comments = s.query(tabledef.Comments).all()
        return comments

def get_comment(comment_id):
    with session_scope() as s:
        comment = s.query(tabledef.Comments).filter_by(id=comment_id).first()
        return comment

def change_user(**kwargs):
    username = session['username']
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        for arg, val in kwargs.items():
            if val != "":
                setattr(user, arg, val)
        s.commit()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False


def username_taken(username):
    with session_scope() as s:
        return s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
