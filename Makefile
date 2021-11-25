PROJECT_PATH="path/to/Scooter-Sharing-Aggregator"
MONGO_CONNECTION_STR = "mongodb+srv://<user>:<password>@cluster0.wmakm.mongodb.net/<db_name>?retryWrites=true&w=majority&r=majority"

export PROJECT_PATH
export MONGO_CONNECTION_STR

activate_venv: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

run1: venv/bin/activate
	./venv/bin/python3 src/__init__.py 5050
run2: venv/bin/activate
	./venv/bin/python3 src/__init__.py 5000

clean:
	rm -rf venv
	find . -type f -name ‘*.pyc’ -delete