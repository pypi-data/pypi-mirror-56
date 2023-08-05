# -*- coding: utf-8 -*-
"""MSSQL class file."""

import pymssql


class MSSQL(object):
    """MSSQL class."""

    def __init__(
        self,
        server,
        user,
        password,
        database,
        verbose=False,
    ):
        """Initialize an instance."""
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.verbose = verbose

        # connect
        self.cursor = self.connect()

    def connect(self):
        """Connect to a MSSQL server and return a cursor."""
        try:
            self.conn = pymssql.connect(
                server=self.server,
                user=self.user,
                password=self.password,
                database=self.database,
            )

        except Exception as e:
            print('ERROR connecting to MSSQL server: %s' % (e))
            raise

        # return a cursor
        return self.conn.cursor(as_dict=True)
