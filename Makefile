clean:
	rm -rf dist/ 

docs: clean
	sphinx-apidoc -fTe -o docs/refs/ src/demarches_simpy/
	sphinx-build -b html docs/ dist/