# Swagger-Editor

    docker pull swaggerapi/swagger-editor
    docker run -p 8071:8080 swaggerapi/swagger-editor

http://localhost:8071

add -d for background if you like (I don't)

select a swagger.json file from the current dir:

    docker run -p 8071:8080 -v $(pwd):/tmp -e SWAGGER_FILE=/tmp/swagger.json swaggerapi/swagger-editor


# Swagger-UI

Testing swagger.json file:

    docker pull swaggerapi/swagger-ui
    docker run -p 8071:8080 -e SWAGGER_JSON=/foo/swagger.json -v $(pwd):/foo swaggerapi/swagger-ui

For python:
    https://pypi.org/project/swagger-ui-py/

In a dockerfile:

    pip3 install swagger-ui-py


Code snippet:

    from swagger_ui import api_doc
    api_doc(app, config_path='./config/test.yaml', url_prefix='/api/doc', title='API doc')

