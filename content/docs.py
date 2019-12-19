from flask_apispec import FlaskApiSpec
import views
import app

docs = FlaskApiSpec(app)

docs.register(
    views.get_services,
    endpoint='get_services',
    blueprint='content',
)
docs.register(
    views.add_service,
    endpoint='add_service',
    blueprint='content',
)
docs.register(
    views.filter_services,
    endpoint='filter_services',
    blueprint='content',
)

docs.register(
    views.get_service_categories,
    endpoint='get_service_categories',
    blueprint='content',
)
docs.register(
    views.add_service_category,
    endpoint='add_service_category',
    blueprint='content',
)

docs.register(
    views.get_service_providers,
    endpoint='get_service_providers',
    blueprint='content',
)
docs.register(
    views.add_service_provider,
    endpoint='add_service_provider',
    blueprint='content',
)

docs.register(
    views.get_service_slots,
    endpoint='get_service_slots',
    blueprint='content',
)
docs.register(
    views.add_service_slot,
    endpoint='add_service_slot',
    blueprint='content',
)