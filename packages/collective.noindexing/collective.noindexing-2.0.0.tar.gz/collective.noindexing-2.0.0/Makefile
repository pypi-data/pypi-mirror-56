bin/instance: bin/buildout buildout.cfg setup.py
	bin/buildout -Nv
	touch bin/instance

bin/pip:
	virtualenv .

bin/buildout: bin/pip requirements.txt
	bin/pip install -r requirements.txt
	touch bin/buildout

bootstrap: bin/buildout

buildout: bin/instance

fg: bin/instance
	bin/instance fg
