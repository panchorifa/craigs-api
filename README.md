craigs-api
===================
search craigslist nation wide

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


### Running flask api

```
python app.py
```

"""
curl http://localhost:8000/regions
curl http://localhost:8000/categories
curl http://localhost:8000/us/cities
"""


### Running command line interface

```
python xlist.py find -X "cta" -K "f100"
```
