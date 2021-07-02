import time
from datetime import datetime

# list function of history (list of blocked software)
def list(db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id`, `path`, `name`, `reason`, `timestamp` FROM history")
	for row in cursor.fetchall():
		yield (row[0], row[1], row[2], row[3], datetime.fromtimestamp(row[4]))

# # Get informations of a blocked software from its id
def get(id, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id`, `path`, `name`, `reason`, `timestamp` FROM history where `id` = ?", [id])

	row = cursor.fetchone()
	if row:
		return (row[0], row[1], row[2], row[3], datetime.fromtimestamp(row[4]))
	else:
		return None

# Add a new blocked software to the history
def add(path, name, reason, timestamp, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("INSERT INTO history (`path`, `name`, `reason`, `timestamp`) VALUES (?, ?, ?, ?)", [path, name, reason, timestamp])
	db.commit()

	return cursor.lastrowid

# Delete a blocked software from the history
def remove(id, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("DELETE FROM history WHERE `id` = ?", [id])
	db.commit()
	return True
