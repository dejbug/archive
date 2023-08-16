SOURCES := $(wildcard src/*.py src/lib/*.py)

.PHONY : all clear reset
all : ; @echo Be more specific.
clear : ;
reset : | clear ; rm -rf dist/

dist/%.tar.gz : $(SOURCES) | dist/ ; python src/setup.py sdist
dist/%.pex : $(SOURCES) | dist/ ; pex -o $@ -e archive:main -D src/
dist/ : ; mkdir -p dist/
