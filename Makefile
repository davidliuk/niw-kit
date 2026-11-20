UV_CACHE_DIR ?= $(CURDIR)/.tmp/uv-cache
export UV_CACHE_DIR

PYTHON ?= uv run python
KIT := $(PYTHON) tools/kit.py
CASE ?= $(firstword $(wildcard cases/*))

.PHONY: help bootstrap sync doctor test new check final stubs review binder online preview all freeze verify-frozen demo

help:
	@printf '%s\n' \
	  'make bootstrap               Install Homebrew tools and Python dependencies' \
	  'make doctor                  Check pandoc, typst, poppler, and Python packages' \
	  'make new ID=me NAME="Full"   Create cases/<ID> from case-template/' \
	  'make check   [CASE=cases/x]  Draft check: citations, payloads, locked phrases, privacy' \
	  'make final   [CASE=cases/x]  Final check: also fails on placeholders and stub PDFs' \
	  'make stubs                   Placeholder PDFs for missing evidence (preview only)' \
	  'make review                  Draft petition + review packet PDFs' \
	  'make binder                  Bookmarked exhibit binder' \
	  'make preview                 Banner-marked online upload set, even with open gaps' \
	  'make online                  Final online upload set (requires a clean final check)' \
	  'make freeze LABEL=filed-...  Hash the filed upload set and evidence' \
	  'make verify-frozen           Confirm the filed record is unchanged' \
	  'make demo                    Build the blank template end to end in .tmp/demo' \
	  'make test                    Run the kit tests'

bootstrap:
	brew bundle
	uv sync

sync:
	uv sync

doctor:
	$(KIT) doctor

test:
	$(PYTHON) -m unittest discover -s tests -v

new:
	$(KIT) new $(ID) --name "$(NAME)"

check:
	$(KIT) check --case $(CASE)

final:
	$(KIT) check --case $(CASE) --final

stubs:
	$(KIT) stubs --case $(CASE)

review:
	$(KIT) review --case $(CASE)

binder:
	$(KIT) binder --case $(CASE)

preview:
	$(KIT) online --case $(CASE) --allow-draft

online:
	$(KIT) online --case $(CASE)

all:
	$(KIT) all --case $(CASE)

freeze:
	$(KIT) freeze --case $(CASE) --label $(LABEL)

verify-frozen:
	$(KIT) verify-frozen --case $(CASE)

demo:
	rm -rf .tmp/demo && mkdir -p .tmp && cp -R case-template .tmp/demo
	$(KIT) stubs --case .tmp/demo
	$(KIT) check --case .tmp/demo
	$(KIT) review --case .tmp/demo
	$(KIT) binder --case .tmp/demo
	$(KIT) online --case .tmp/demo --allow-draft
