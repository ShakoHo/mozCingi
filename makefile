# Pull all dependencies for mozCingi

mutagen-install: venv-install fuzzmanager-install mozitp-install lib-install

install: venv-install lib-install

venv-install:
ifndef VIRTUAL_ENV
	virtualenv env
endif

lib-install:
	. env/bin/activate; \
	python setup.py install;

fuzzmanager-install:
	@git clone https://github.com/MozillaSecurity/FuzzManager;
	cp -Rf FuzzManager/Collector lib/FuzzManager/Collector;
	cp -Rf FuzzManager/FTB lib/FuzzManager;
	cp FuzzManager/requirements.txt FuzzManager_requirements.txt
	touch FuzzManager/__init__.py
	rm -rf FuzzManager	

mozitp-install:
	cd lib;\
	git clone https://github.com/Mozilla-TWQA/MozITP;

clean:
	rm -rf env

