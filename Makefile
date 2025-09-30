.PHONY: build clean

build:
	python3 tools/prerender_all.py

clean:
	rm -f pages/**/*.html

.PHONY: import
import:
	python3 tools/import_from_vault.py $(VAULT)

.PHONY: build-from
# Render directly from a source markdown root into pages/
# Usage: make build-from SRC=mathematical-economics-book
build-from:
	python3 tools/prerender_from.py $(SRC)
