import sys
import argparse, re

import xml.etree.ElementTree as ET

import lib.net
import lib.cache
import lib.archive

MAXAGE = 60 * 60 * 24

def parseArgs(args = sys.argv[1:]):
	parser = argparse.ArgumentParser()
	pp = parser.add_subparsers()

	p = pp.add_parser('type')
	p.set_defaults(cmd = 'type')
	p.add_argument('-i', '--print-index', action='store_true')
	p.add_argument('-s', '--short-type', action='store_true')
	p.add_argument('-e', '--echo-arg', action='store_true')
	p.add_argument('args', nargs="+")

	p = pp.add_parser('files')
	p.set_defaults(cmd = 'files')
	p.add_argument('-H', '--human-readable', action='store_true')
	p.add_argument('-n', '--sort-by-name', action='store_true')
	p.add_argument('-s', '--sort-by-size', action='store_true')
	p.add_argument('-r', '--sort-reversed', action='store_true')
	p.add_argument('arg')
	return parser, parser.parse_args(args)


def determineCliArgType(text):
	if text.startswith('@'): return 'user'
	uri = lib.archive.parse(text)
	return uri.type if uri.ok else '?'


def fetchCached(uri):
	uri = lib.archive.text(uri)
	print(uri)
	print(lib.cache.path(uri))
	age = lib.cache.age(uri)
	if age is None or age > MAXAGE:
		page = lib.net.fetch(uri)
		lib.cache.set(uri, page)
	else:
		page = lib.cache.get(uri)
	return page


def listFilesForArchiveUri(arg):
	uri = arg if isinstance(arg, lib.archive.Uri) else lib.archive.parse(arg)
	uri = uri.index
	# print(uri.text)
	assert uri
	page = fetchCached(uri)
	# print(page.text)
	tree = ET.fromstring(page.text)
	# print(tree, dir(tree))
	out = []
	for file in tree:
		# print(file, dir(file)); break
		name = file.get('name')
		size = file.find('size')
		size = -1 if size is None else int(size.text)
		out.append({ 'size': size, 'name': name })
	return out


def makeHumanReadableSize(size, block = 1024, sep = ' '):
	sep = sep or ''
	mm = " kMGTPEZYRQ"
	i = 0
	while size > block:
		size //= block
		i += 1
	assert i < len(mm)
	# out = f'{size}{sep}{mm[i]}'
	# if not sep: out = out.strip()
	# return out
	return f'{size}{sep}{mm[i]}'


def main(args = sys.argv[1:]):
	parser, args = parseArgs(args)
	# print(args); exit()

	if args.cmd == 'type':
		for i, arg in enumerate(args.args, start=1):
			out = f'{determineCliArgType(arg)}'
			if args.short_type:
				out = out[0]
				sep = ' '
			else:
				sep = '\t'
			if args.echo_arg:
				out = f'{out}{sep}{arg}'
			if args.print_index:
				out = f'{i:07d}{sep}{out}'
			print(out)

	elif args.cmd == 'files':
		files = listFilesForArchiveUri(args.arg)
		print(-1 if files is None else len(files))
		if args.sort_by_name:
			files = sorted(files, key = lambda file: file['name'], reverse = args.sort_reversed)
		if args.sort_by_size:
			files = sorted(files, key = lambda file: file['size'], reverse = args.sort_reversed)
		for file in files:
			size = file["size"]
			if args.human_readable:
				if size >= 0:
					size = f'{makeHumanReadableSize(size, sep=None).strip():>7s}'
				else:
					size = f'{"?":>7s}'
			else:
				size = f'{size:013d}' if size >= 0 else f'{"?":>13s}'
			print(f'{size} {file["name"]}')


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
