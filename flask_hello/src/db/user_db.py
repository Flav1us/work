from db.session import db_session_ctx
from db.models import ModelBase, User


class UserDb(object):
    """ Contains helpers for user db.
    """

    def __init__(self):
        pass

    @staticmethod
    def reset_db():
        """ Re-applies DB schema.
        """
        ModelBase.metadata.drop_all()
        ModelBase.metadata.create_all()

    def contains_user(self, username):
        with db_session_ctx(read_only=True) as session:
            user = session.query(User).filter(User.name == username).first()
            return user is not None

    def create_user(self, username, password, email):
        with db_session_ctx() as session:
            user = User(name=username, password=password, email=email)
            session.add(user)

    def are_valid_credentials(self, username, password):
        with db_session_ctx(read_only=True) as session:
            user = session.query(User).filter(User.name == username).first()
            return user.password == password if user else False
