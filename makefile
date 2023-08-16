SOURCES := $(wildcard src/*.py src/lib/*.py)
SOURCES := $(filter-out src/setup.py,$(SOURCES))

.PHONY : all clean reset purge
all : ; @echo Be more specific.
clean : ; rm -rf *.egg-info/ src/*.egg-info/
reset : | clean ; rm -rf dist/
purge : | reset ; rm -rf src/__pycache__/ src/lib/__pycache__/

dist/ : ; mkdir -p dist/
dist/%.tar.gz : $(SOURCES) | dist/ ; python src/setup.py sdist
dist/%.pex : $(SOURCES) | dist/ ; pex -o $@ -e archive:main -D src/

# make reset
# make sources [list]
# make pex [list]
# make tar/gz [list]

.PHONY : pex tar gz list sources

sources :
ifneq (,$(filter list,$(MAKECMDGOALS)))
	@echo $(SOURCES) | tr ' ' '\n' | sort
else
	@echo $(SOURCES)
endif

pex : dist/archive.pex
ifneq (,$(filter list,$(MAKECMDGOALS)))
	@unzip -l $<
endif
	@ls -s --block-size 1 $<

tar gz : dist/archive.tar.gz
ifneq (,$(filter list,$(MAKECMDGOALS)))
	@tar tf dist/archive-*.tar.gz
endif
	@ls -s --block-size 1 dist/archive-*.tar.gz

list : ; @echo -n
