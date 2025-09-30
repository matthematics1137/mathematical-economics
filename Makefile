.PHONY: build clean

build:
	python3 tools/prerender_all.py

clean:
	rm -f pages/**/*.html

