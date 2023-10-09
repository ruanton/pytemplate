import transaction
import ZODB.Connection
import persistent
import persistent.mapping

# noinspection PyUnresolvedReferences
from BTrees.OOBTree import OOBTree
# noinspection PyUnresolvedReferences
from BTrees.IOBTree import IOBTree

# local imports
from . import tcm

# force explicit transactions
# see: https://relstorage.readthedocs.io/en/latest/things-to-know.html#use-explicit-transaction-managers
transaction.manager.explicit = True


class AppRoot(persistent.Persistent):  # in Cookiecutter: base class was PersistentMapping
    """App Root object. Root of all other persistent objects.
    """
    # __parent__ = __name__ = None   # it was in Cookiecutter, don't know what it's for

    def __init__(self):
        pass


def get_app_root(conn: ZODB.Connection.Connection) -> AppRoot:
    """
    Get the AppRoot persistent object. Creates a new one, if it does not already exist.
    Side effect: if the object does not already exist in the database, creates it; if not in a transaction,
    a new transaction is started and committed.
    """
    zodb_root: persistent.mapping.PersistentMapping = conn.root()

    if 'app_root' in zodb_root:
        # get object from database
        app_root: AppRoot = zodb_root['app_root']
    else:
        # create a new object
        if tcm.has_transaction(conn_or_tm=conn):
            # we are already in transaction
            app_root = AppRoot()
            zodb_root['app_root'] = app_root
        else:
            # start and commit a new transaction
            with tcm.in_transaction(conn):
                app_root = AppRoot()
                zodb_root['app_root'] = app_root

    return app_root
