xmunicipio-services
===================
backend services for xmunicipio

## setup

	pip install -r requirements.txt;pip install -r requirements_dev.txt;


	installing lxml in ubuntu requires:

	"""
	sudo apt-get install libxml2-dev libxslt-dev
	sudo apt-get install python-lxml
	"""

### Testing

```
nosetests -c .noserc_local
```

Then check `test_results/coverage/index.html` for the HTML report.


### Capture test data

```	
curl http://es.wikipedia.org/wiki/Anexo:Municipios_de_Aguascalientes > tests/samples/aguascalientes.html
```
