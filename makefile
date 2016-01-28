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
	mkdir lib/FuzzManager;
	cp -Rf FuzzManager/Collector/* lib/FuzzManager;
	cp -Rf FuzzManager/FTB lib/FuzzManager;
	cp FuzzManager/requirements.txt FuzzManager_requirements.txt;
	touch FuzzManager/__init__.py;
	cd lib/FuzzManager;\
	find ./ -type f -exec sed -i -e 's/from FTB/from lib.FuzzManager.FTB/g' {} \;
	find ./ -type f -exec sed -i -e 's/import lib.FuzzManager.FTB/import lib.FuzzManager.FTB/g' {} \;
	rm -rf FuzzManager	

mozitp-install:
	cd lib;\
	git clone https://github.com/Mozilla-TWQA/MozITP;

clean-data:
	rm -rf tmp/*;
	rm -rf output/*;

clean: clean-data
	rm -rf env;


