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


### Running api

```
python app.py
```

"""
curl http://localhost:8000/regions
curl http://localhost:8000/categories
curl http://localhost:8000/us/cities
"""


### Capture test data

```
curl http://es.wikipedia.org/wiki/Anexo:Municipios_de_Aguascalientes > tests/samples/aguascalientes.html
```
