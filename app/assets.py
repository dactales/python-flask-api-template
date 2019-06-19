import os
from flask_assets import Bundle, Environment


def create_webassets(app):
    webassets = Environment(app)
    webassets.load_path = [
        os.path.join(os.path.dirname(__file__), "static"),
        os.path.join(os.path.dirname(__file__), "bower_components"),
        os.path.join(os.path.dirname(__file__), "node_modules"),
    ]
    # webassets.manifest = 'cache' if not current_app.debug else False
    # webassets.cache = not current_app.debug
    # webassets.debug = current_app.debug

    js_main = Bundle("js/src/main.js", output="js/main.js")

    css_main = Bundle("css/src/styles.css", output="css/main.css")

    js_libs = Bundle(
        "jquery/dist/jquery.min.js",
        "fomantic-ui/dist/semantic.min.js",
        output="js/libs.js",
    )

    css_libs = Bundle(
        "fomantic-ui/dist/semantic.min.css",
        "font-awesome/css/font-awesome.min.css",
        output="css/libs.css",
    )

    webassets.register("js_main", js_main)
    webassets.register("js_libs", js_libs)
    webassets.register("css_main", css_main)
    webassets.register("css_libs", css_libs)
