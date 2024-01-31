deploy:
	@pip freeze > requirements.txt
	docker run -v $(shell PWD):/var/task "lambci/lambda:build-python3.8" /bin/bash -c "pip install -r requirements.txt -t src/python"

	# cd src/python; zip -r ../../build/python.zip . -x requirements.txt
	
	cd terraform; terraform apply --auto-approve

deploy_only:
	cd terraform; terraform apply --auto-approve


docker_build:
	docker run -v $(shell PWD):/var/task "lambci/lambda:build-python3.8" /bin/bash -c "pip install -r requirements.txt -t src/python"
