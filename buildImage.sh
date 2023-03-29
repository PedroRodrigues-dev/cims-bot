VERSION=1.0.0-alpha
IMAGE_REPOSITORY=cims-bot

docker build -t $IMAGE_REPOSITORY .

docker login

docker tag $IMAGE_REPOSITORY $IMAGE_REPOSITORY:$VERSION

docker push $IMAGE_REPOSITORY
docker push $IMAGE_REPOSITORY:$VERSION