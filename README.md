# mozCingi
Fuzzy Testing for B2G

Cingi: vocabulary from Taiwan aboriginal "Yami", which means spy on sth.

How to install:

  - basic installation: make install
  - mutagen fuzzer installation: make mutagen-install

how to execute:

  - rename conf/sampleFuzzer.json.bak to conf/sampleFuzzer.json
  - switch to virtual environment you created (source ./env/bin/activate)
  - give cmd: cingi --dirpath conf
  - this is a sample fuzzer, it will print all variables in configuration
