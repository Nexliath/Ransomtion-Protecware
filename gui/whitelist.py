def list(db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id`, `path`, `name` FROM whitelist")
	for row in cursor.fetchall():
		yield (row[0], row[1], row[2])

def get(id, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id`, `path`, `name` FROM whitelist where `id` = ?;", [id])

	row = cursor.fetchone()
	if row:
		return (row[0], row[1], row[2])
	else:
		return None

def get_id(path, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("SELECT `id` FROM whitelist where `path` = ?;", [path])

	row = cursor.fetchone()
	if row:
		return row[0]
	else:
		return None

def add(path, name, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	if get_id(path, db, cursor) is not None:
		return None

	cursor.execute("INSERT INTO whitelist (`path`, `name`) VALUES (?, ?);", [path, name])
	db.commit()

	return cursor.lastrowid

def remove(id, db, cursor=None):
	if cursor is None:
		cursor = db.cursor()

	cursor.execute("DELETE FROM whitelist WHERE `id` = ?;", [id])
	db.commit()
	return True
