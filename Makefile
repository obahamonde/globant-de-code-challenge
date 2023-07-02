do:
	docker build -t csvapi .
	docker run -d -p 5000:8080 csvapi