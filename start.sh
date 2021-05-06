docker image rm $(docker images | grep none | awk '{ print $3; }')
xhost +
docker build -t segmentar .
docker run --rm -it \
    -v ${PWD}/media:/media \
    -v ${PWD}/files:/files \
    -v ${PWD}/PP:/PP \
    -v ${PWD}/results:/results \
    -v ${PWD}/times:/times \
    segmentar

