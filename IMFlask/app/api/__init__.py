"""
API Request Handler and util
"""
from flask import Flask, g, current_app, request, Response
from model.mongodb import Log


def init_app(app: Flask):

    @app.before_first_request
    def before_first_request():
        pass

    @app.before_request
    def before_request():
        pass

    @app.after_request
    def after_request(response):
        config = current_app.config

        # Slow API Tracking
        if (
            'process_time' in g
            and g.process_time >= config['SLOW_API_TIME']
        ):
            body = request.get_json(silent=True) or dict(request.form)

            app.logger.warning(
                "\n!!! SLOW API DETECTED !!!\n" 
                f"ip: {request.remote_addr}\n" 
                f"url: {request.full_path}\n"
                f"body: {body}\n"
                f"slow time: {g.process_time}\n"
            )

        # API Logging
        if config['API_LOGGING']:
            if isinstance(response, Response):
                status_code = response.status_code
            else:
                status_code = response[1]

            Log().insert_log({
                'ipv4': request.remote_addr,
                'url': request.full_path,
                'method': request.method,
                'params': request.data.decode(),
                'status_code': status_code
            })

        return response

    @app.teardown_request
    def teardown_request(exception):
        pass

    @app.teardown_appcontext
    def teardown_appcontext(exception):
        pass
