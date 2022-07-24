import sqlite3
import hashlib
import os
import codecs

class UserManagement:
    def __init__(self):
        self.db = 'db.sqlite'
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, key TEXT)')
        cur.close()
        db.commit()
        db.close()
    def get_hash(self, passwd, salt):
        key = hashlib.pbkdf2_hmac(
            'sha256',
            passwd.encode('utf-8'),
            salt,
            100000
        )
        return key
    def create_user(self, username, passwd):
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        salt = os.urandom(32)
        hashed_passwd = self.get_hash(passwd, salt)
        hex_encoded = codecs.encode(salt+hashed_passwd, 'hex_codec').decode('utf-8')
        cur.execute('INSERT INTO users VALUES("{}", "{}")'.format(username, hex_encoded))
        cur.close()
        db.commit()
        db.close()

    def auth(self, username, passwd):
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        db.close()
        authenticated = False
        for user in users:
            if user[0] == username:
                hex_decoded = codecs.decode(user[1], 'hex_codec')
                salt = hex_decoded[:32]
                key = hex_decoded[32:]
                new_key = self.get_hash(passwd, salt)
                if new_key == key:
                    authenticated = True
        return authenticated
