LOCALES = de_DE fr_FR en_US sv_SE
PO_FILES = $(foreach loc,$(LOCALES),$(loc)/LC_MESSAGES/intg-denonavr.po)
MO_FILES = $(PO_FILES:.po=.mo)

all: $(MO_FILES)

%.mo: %.po
	msgfmt -o $@ $<

update_po:
	xgettext -d intg-denonavr -o intg-denonavr.pot --from-code=UTF-8 --language=Python --add-comments=Translators --keyword=_ --keyword=_n:1,2 --keyword=__ --keyword=_a --no-wrap --copyright-holder="Unfolded Circle ApS" --package-name "uc-integration-denon-avr" ../*.py
	$(foreach po,$(PO_FILES),msgmerge --no-wrap --update $(po) intg-denonavr.pot;)

clean:
	rm -f */*/*.mo

.PHONY: all update_po clean
