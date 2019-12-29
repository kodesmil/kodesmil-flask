from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from flask_apispec import FlaskApiSpec

import views

class Documentation:

    def __init__(self, app):
        app.config.update({
            'APISPEC_SPEC': APISpec(
                title='KodeSmil Flask',
                version='v1',
                openapi_version="3.0.2",
                info=dict(description='KodeSmil microservices API'),
                plugins=[MarshmallowPlugin()],
            ),
            'APISPEC_SWAGGER_UI_URL': '/docs/',
        })
        self.docs = FlaskApiSpec(app)
        self._initialize()

    def _initialize(self):
        self.docs.register(
            views.get_services,
            endpoint='get_services',
            blueprint='content',
        )
        self.docs.register(
            views.add_service,
            endpoint='add_service',
            blueprint='content',
        )
        self.docs.register(
            views.filter_services,
            endpoint='filter_services',
            blueprint='content',
        )

        self.docs.register(
            views.get_service_categories,
            endpoint='get_service_categories',
            blueprint='content',
        )
        self.docs.register(
            views.add_service_category,
            endpoint='add_service_category',
            blueprint='content',
        )

        self.docs.register(
            views.get_service_providers,
            endpoint='get_service_providers',
            blueprint='content',
        )
        self.docs.register(
            views.add_service_provider,
            endpoint='add_service_provider',
            blueprint='content',
        )

        self.docs.register(
            views.get_service_slots,
            endpoint='get_service_slots',
            blueprint='content',
        )
        self.docs.register(
            views.add_service_slot,
            endpoint='add_service_slot',
            blueprint='content',
        )