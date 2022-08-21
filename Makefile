all: install_translate

install_translate: translate
	mkdir -p locale/ru/LC_MESSAGES/
	cp translate/*.mo locale/ru/LC_MESSAGES/

translate: make_mo

make_mo: update_po

update_po:
	pygettext3 -d translate/commands commands.py
  
  
  
