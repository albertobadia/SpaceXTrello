from api.config import TESTING

# Import the correct services based on the config
if TESTING:
    from api.setup.testing import rq_queue, tasks_service, trello_service, users_service
else:
    from api.setup.local import rq_queue, tasks_service, trello_service, users_service
