from database import Database

def check(path):
	with Database() as db:
		cursor = db.cursor()
		cursor.execute("SELECT `id` FROM whitelist where `path` = ?", [path])

		row = cursor.fetchone()
		if row:
			return True
		else:
			return False
