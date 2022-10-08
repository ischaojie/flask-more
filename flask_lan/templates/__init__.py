from importlib.resources import read_text

redoc_template = read_text(__package__, "redoc.html")
swagger_template = read_text(__package__, "swagger.html")
