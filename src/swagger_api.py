from flask import Flask
from flasgger import Swagger, LazyString, LazyJSONEncoder

def setup_swagger(app):
    app.json_encoder = LazyJSONEncoder

    swagger_template = {
        "info": {
            "title": "My API",
            "description": "API description",
            "version": "1.0"
        },
        "servers": [{"url": "http://localhost:5000"}],
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'hello_world',
                "route": '/hello_world.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger = Swagger(app, template=swagger_template, config=swagger_config)


if __name__ == '__main__':
    app.run(debug=True)
