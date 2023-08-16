# Building

```
$ make reset
rm -rf *.egg-info/ src/*.egg-info/
rm -rf dist/
$ make tar list
mkdir -p dist/
python src/setup.py sdist
archive-0.0.1/
archive-0.0.1/LICENSE
archive-0.0.1/PKG-INFO
archive-0.0.1/README.md
archive-0.0.1/archive.egg-info/
archive-0.0.1/archive.egg-info/PKG-INFO
archive-0.0.1/archive.egg-info/SOURCES.txt
archive-0.0.1/archive.egg-info/dependency_links.txt
archive-0.0.1/archive.egg-info/top_level.txt
archive-0.0.1/setup.cfg
archive-0.0.1/src/
archive-0.0.1/src/archive.py
archive-0.0.1/src/lib/
archive-0.0.1/src/lib/abs.py
archive-0.0.1/src/lib/archive.py
archive-0.0.1/src/lib/cache.py
archive-0.0.1/src/lib/log.py
archive-0.0.1/src/lib/net.py
8192 dist/archive-0.0.1.tar.gz
$ make pex
pex -o dist/archive.pex -e archive:main -D src/
704512 dist/archive.pex
```

# Running

```
$ dist/archive.pex type -ise \
  https://archive.org/details/republicshorey01platuoft \
  https://archive.org/details/republicshorey01platuoft/ \
  https://archive.org/details/republicshorey01platuoft/page/vii/mode/1up
0000001 d https://archive.org/details/republicshorey01platuoft
0000002 d https://archive.org/details/republicshorey01platuoft/
0000003 d https://archive.org/details/republicshorey01platuoft/page/vii/mode/1up
$ dist/archive.pex files -Hsr https://archive.org/details/republicshorey01platuoft/page/vii/mode/1up   493M republicshorey01platuoft_raw_jp2.zip
   129M republicshorey01platuoft_jp2.zip
    52M scandata.zip
    24M republicshorey01platuoft_hocr.html
    22M republicshorey01platuoft.pdf
    12M republicshorey01platuoft_chocr.html.gz
    12M republicshorey01platuoft_djvu.xml
   965k republicshorey01platuoft_djvu.txt
   427k republicshorey01platuoft_hocr_searchtext.txt.gz
    92k republicshorey01platuoft_page_numbers.json
    15k __ia_thumb.jpg
    14k republicshorey01platuoft_archive.torrent
     6k republicshorey01platuoft_hocr_pageindex.json.gz
     3k republicshorey01platuoft_marc.xml
     2k republicshorey01platuoft_meta.xml
     1k republicshorey01platuoft_reviews.xml
     1k republicshorey01platuoft_meta.mrc
    710 _cloth_detection.log
    418 republicshorey01platuoft_dc.xml
    377 republicshorey01platuoft_metasource.xml
      ? republicshorey01platuoft_files.xml
$ dist/archive.pex files -Hsr -g '*.pdf' https://archive.org/details/republicshorey01platuoft/page/vii/mode/1up
    22M republicshorey01platuoft.pdf
$ dist/archive.pex files -Hsr -g '*.????.gz' https://archive.org/details/republicshorey01platuoft/page/vii/mode/1up
    12M republicshorey01platuoft_chocr.html.gz
     6k republicshorey01platuoft_hocr_pageindex.json.gz
```
