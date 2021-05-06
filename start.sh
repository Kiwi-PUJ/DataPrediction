docker build -t data_prediction .
docker run --rm -it \
    -v ${PWD}/media:/media \
    -v ${PWD}/files:/files \
    -v ${PWD}/results:/results \
    -v ${PWD}/times:/times \
    data_prediction

