

launch-mysql:
	docker run --name mysql-local \
		  -e MYSQL_ROOT_PASSWORD=password \
		  -e MYSQL_DATABASE=mydb \
		  -p 3306:3306 \
		  -v mysql-data:/var/lib/mysql \
		  -d mysql:8.0

execute-sql:
	docker exec -i mysql-local mysql -u root -ppassword < create_database.sql

install-package:
	.\.venv\Scripts\Activate.ps1
	pip install uvicorn fastapi mysql-connector-python python-multipart

launch-server:
	python -m uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000

extract-requirement:
	pip freeze > requirement.txt