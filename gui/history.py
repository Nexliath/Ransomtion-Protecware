import time
from datetime import datetime

def list(db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id`, `path`, `name`, `reason`, `timestamp` FROM history")
	for row in cursor.fetchall():
		yield (row[0], row[1], row[2], row[3], datetime.fromtimestamp(row[4]))

def get(id, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id`, `path`, `name`, `reason`, `timestamp` FROM history where `id` = ?;", [id])

	row = cursor.fetchone()
	if row:
		return (row[0], row[1], row[2], row[3], datetime.fromtimestamp(row[4]))
	else:
		return None

def get_id(path, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id` FROM history where `path` = ?;", [path])

	row = cursor.fetchone()
	if row:
		return row[0]
	else:
		return None

def add(path, name, reason, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	if get_id(path, db, cursor) is not None:
		return None

	cursor.execute("INSERT INTO history (`path`, `name`, `reason`, `timestamp`) VALUES (?, ?);", [path, name, reason, time.time()])
	db.commit()

	return cursor.lastrowid

def remove(id, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("DELETE FROM history WHERE `id` = ?;", [id])
	db.commit()
	return True
