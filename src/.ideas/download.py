import urllib.request
import re
import hashlib
import sqlite3
import time
import random

import archive


def fetch(url, outpath):
	page = urllib.request.urlopen(url)
	with open(outpath, "wb") as file:
		file.write(page.read())


def sha(text):
	return hashlib.sha224(text.encode("utf8")).hexdigest()


def iter_urls(text, pattern=None):
	done = []
	for m in re.finditer(r"href=\"(.+?)\"", text):
		url = m.group(1)
		if not pattern:
			hash = sha(url)
			if hash not in done:
				done.append(hash)
				yield url
		n = re.search(pattern, m.group(1))
		if not n: continue
		url = n.group(0)
		hash = sha(url)
		if hash not in done:
			done.append(hash)
			yield url


def archive_showall_parse_urls(text):
	urls = {"djv": [], "pdf": []}
	for url in iter_urls(text, r".*\.djvu?"):
		url = "https://archive.org/" + url
		urls["djv"].append(url)
	for url in iter_urls(text, r".*\.pdf"):
		urls["pdf"].append(archive.Url(url).url)
	return urls


def archive_showall_fetch(url):
	page = urllib.request.urlopen(url)
	# print(page.status)
	# print(page.url)
	# print(page.headers)
	# print(page.read())
	return page


def iter_lines(path):
	with open(path) as file:
		for line in file:
			line = line.strip()
			if not line: continue
			yield line


def sqlite_add_books(db):
	db.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, url TEXT UNIQUE)")
	cursor = db.cursor()
	for line in iter_lines("urls"):
		url = archive.Url(line)
		#~ print(url.url)
		cursor.execute("INSERT OR IGNORE INTO books (url) VALUES (?)", (url.url, ))


def sqlite_resolve_books(db):
	db.execute("CREATE TABLE IF NOT EXISTS downloads (id INTEGER PRIMARY KEY, bid INTEGER, url TEXT UNIQUE, FOREIGN KEY(bid) REFERENCES books(id))")

	for bid, url in db.execute("SELECT * FROM books"):
		# print(bid, url)
		showall = archive_showall_fetch(url)
		urls = archive_showall_parse_urls(showall.read().decode("utf8"))

		cursor = db.cursor()
		for links in urls.values():
			for link in links:
				print("LINK", link)
				cursor.execute("INSERT OR IGNORE INTO DOWNLOADS (bid, url) VALUES (?,?)", (bid, link))
		db.commit()


def test_archive_url_1():
	for line in iter_lines("urls"):
		url = archive.Url(line)
		assert line == url.full
		print(url.url)

def test_archive_url_2():
	with sqlite3.connect("archive.sqlite") as db:
		for bid, burl in db.execute("SELECT * FROM books"):
			url = archive.Url(burl)
			assert burl == url.full
			print(url.url)

def test_archive_url_2():
	with sqlite3.connect("archive.sqlite") as db:
		for bid, burl in db.execute("SELECT id, url FROM books"):
			url = archive.Url(burl)
			assert burl == url.full
			print(url.url)

def test_archive_url_3():
	with sqlite3.connect("archive.sqlite") as db:
		for did, durl in db.execute("SELECT id, url FROM downloads"):
			url = archive.Url(durl)
			print(durl)
			print()
			print(url.full)
			print()
			print()


if __name__ == "__main__":
	#~ test_archive_url_1()
	#~ test_archive_url_2()
	#~ test_archive_url_3()
	#~ exit()

	with sqlite3.connect("archive.sqlite") as db:

		#~ sqlite_add_books(db)
		#~ sqlite_resolve_books(db)
		#~ time.sleep(random.randint(1,5))

		#~ for bid, burl, did, durl in db.execute("SELECT books.id, books.url, downloads.id, downloads.url FROM books, downloads WHERE downloads.bid = books.id"):
			#~ print(bid, burl, "\n", did, durl, "\n\n")

		for bid, burl in db.execute("SELECT * FROM books"):
			#~ print("BOOK", bid, archive.Url(burl).url)
			#~ print()
			for did, durl in db.execute("SELECT id, url FROM downloads WHERE downloads.bid = ?", (bid,)):
				#~ print(" ", durl)
				url = archive.Url(durl)
				if url.text: continue
				#~ if url.pdf: continue
				#~ print("DOWNLOAD", did, url.url)
				print(url.url)
			#~ print()
