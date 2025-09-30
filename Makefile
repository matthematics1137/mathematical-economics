.PHONY: build clean

build:
	python3 tools/prerender_all.py

clean:
	rm -f pages/**/*.html

.PHONY: import
import:
	python3 tools/import_from_vault.py $(VAULT)
