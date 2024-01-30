pkg_imports:
	@pip freeze > requirements.txt
	@pip install -t ./src/python -r requirements.txt

	cd terraform; tf apply --auto-approve
