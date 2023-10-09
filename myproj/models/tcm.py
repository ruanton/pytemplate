"""
Transaction Context Manager helpers
"""

import typing
import transaction
import transaction.interfaces
import ZODB.Connection


class TransactionContextManager(object):
    """PEP 343 context manager"""
    def __init__(self, conn: ZODB.Connection.Connection, note: str = None):
        self.conn = conn
        self.note = note

    def __enter__(self) -> ZODB.Connection.Connection:
        self.tm = tm = self.conn.transaction_manager
        tran = tm.begin()
        if self.note:
            tran.note(self.note)
        return self.conn

    def __exit__(self, typ, val, tb):
        if typ is None:
            self.tm.commit()
        else:
            self.tm.abort()


def in_transaction(conn: ZODB.Connection.Connection, note: str = None) -> TransactionContextManager:
    """
    Execute a block of code as a transaction.
    Starts database transaction. Commits on success __exit__, rollbacks on exception.
    If a note is given, it will be added to the transaction's description.
    The 'in_transaction' returns a context manager that can be used with the ``with`` statement.
    """
    return TransactionContextManager(conn, note)


def has_transaction(conn_or_tm: typing.Union[ZODB.Connection.Connection, transaction.interfaces.ITransaction]) -> bool:
    """Determines whether a given connection or transaction manager is currently in a transaction.
    """
    if isinstance(conn_or_tm, ZODB.Connection.Connection):
        conn_or_tm: transaction.interfaces.ITransaction = conn_or_tm.transaction_manager

    if isinstance(conn_or_tm, transaction.ThreadTransactionManager):
        conn_or_tm = conn_or_tm.manager

    if isinstance(conn_or_tm, transaction.TransactionManager):
        return getattr(conn_or_tm, '_txn') is not None

    raise ValueError(f'unexpected transaction manager instance: {conn_or_tm}')
