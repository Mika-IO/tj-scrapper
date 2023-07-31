stop-old-container:
	docker stop app || true
	docker rm app || true

build:
	docker build -t app-image .

run: stop-old-container build
	docker run --name app -p 80:80 app-image
