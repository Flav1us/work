from invoke import task  # noqa
from db.user_db import UserDb


@task
def renew_db(_):
    UserDb.reset_db()


@task
def print_db(_):
    print(UserDb.to_string())
