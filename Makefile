deploy:
	@pip freeze > requirements.txt
	# pip install -r requirements.txt --platform manylinux2014_x86_64 --target ./src/python --implementation cp --upgrade --python-version 3.10 --only-binary=:all:
	pip install -r requirements.txt --platform manylinux2014_x86_64 --target ./src/python --implementation cp --upgrade --only-binary=:all:

	cd src/python; zip -r ../../build/python.zip . -x requirements.txt
	
	cd terraform; terraform apply --auto-approve

deploy_only:
	cd terraform; terraform apply --auto-approve
