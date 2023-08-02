install:
	python3 -m pip install -r requirements.txt
	docker build -t mongodb .
	docker run -d -p 27017:27017 --name mongodb_container mongodb

run-tests:
	python3 -m coverage run --source=. -m unittest discover -s tests -b && python3 -m coverage html && open htmlcov/index.html

run:
	uvicorn main:app --host 0.0.0.0 --port 80 --reload