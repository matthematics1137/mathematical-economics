.PHONY: build clean

build:
	python3 tools/prerender_from.py mathematical-economics/mathematical-economics-book

clean:
	rm -f pages/**/*.html

.PHONY: import
import:
	@echo "Deprecated: use 'make build' (renders from mathematical-economics/mathematical-economics-book)" && false

.PHONY: build-from
# Render directly from a source markdown root into pages/
# Usage: make build-from SRC=mathematical-economics-book
build-from:
	python3 tools/prerender_from.py $(SRC)
