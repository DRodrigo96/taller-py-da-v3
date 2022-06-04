# docker local deployment
Comandos bash para despliegue local de modelo en Docker.

## built docker image
```bash
IMAGE_NAME="replace_image_name"
docker build --no-cache -t $IMAGE_NAME .
```

## listar images en docker
```bash
docker image list
```

## listar docker containers en ejecución
```bash
docker ps -a
```

## start docker container
```bash
CONTAINER_NAME="replace_container_name"
docker run --name $CONTAINER_NAME -p 5000:5000 -it $IMAGE_NAME
```

##  stop docker container
```bash
docker stop $CONTAINER_NAME
```

## remove container
```bash
docker rm $CONTAINER_NAME
```

## remove imagen
```bash
docker rmi $IMAGE_NAME
```
