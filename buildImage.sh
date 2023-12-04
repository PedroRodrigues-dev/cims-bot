VERSION=1.1.0-alpha
IMAGE_REPOSITORY=123pedrosilva123/cims-bot

docker build -t $IMAGE_REPOSITORY .

docker login

docker tag $IMAGE_REPOSITORY $IMAGE_REPOSITORY:$VERSION

docker push $IMAGE_REPOSITORY:$VERSION
docker push $IMAGE_REPOSITORY