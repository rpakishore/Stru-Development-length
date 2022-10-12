export $(grep -v '^#' EDIT.env | xargs)
docker build -t ${NAME}:latest .
docker-compose up -d