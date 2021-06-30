from database import Database

def add(path, name, reason, timestamp):
	with Database() as db:
		cursor = db.cursor()
		cursor.execute("INSERT INTO history (`path`, `name`, `reason`, `timestamp`) VALUES (?, ?)", [path, name, reason, timestamp])
		db.commit()

		return cursor.lastrowid
