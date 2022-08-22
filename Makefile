all: install_translate


# use poedit for translate po-files and compile po->mo files:
install_translate: translate
	mkdir -p locale/ru/LC_MESSAGES/
	mkdir -p locale/en/LC_MESSAGES/
	ln -s en locale/us
	cp translate/*_ru.mo locale/ru/LC_MESSAGES/; rename -e 's/_ru.mo/.mo/' locale/ru/LC_MESSAGES/*
	cp translate/*_en.mo locale/en/LC_MESSAGES/; rename -e 's/_en.mo/.mo/' locale/en/LC_MESSAGES/*

translate: make_mo

make_mo: update_pot

update_pot:
	pygettext3 -d translate/commands commands.py
  
  
  
