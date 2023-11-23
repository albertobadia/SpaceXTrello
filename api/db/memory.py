import functools
import uuid


class InMemoryDB:
    """
    InMemoryDB is a class that represents an in-memory database.
    """

    @functools.cached_property
    def store(self) -> dict:
        return dict()

    def _get_table(self, table: str) -> dict[dict]:
        """
        Returns a dictionary representing the table with the given name. If the table does not exist, it is created.

        Args:
        - table (str): The name of the table to retrieve

        Returns:
        - dict[dict]: A dictionary representing the table with the given name
        """
        if not table in self.store:
            self.store[table] = dict()
        return self.store[table]

    def cleanup(self, table: str = None) -> None:
        """
        Removes all data from the specified table or all tables if no table is specified.

        Args:
            table (str, optional): The name of the table to remove data from. If not specified, all tables will be cleared.
        """
        if table:
            self.store[table] = dict()
            return
        vars(self).pop("store")

    def list(self, table: str) -> list[dict]:
        """
        Returns a list of dictionaries containing all the items in the specified table.

        Args:
        table (str): The name of the table to retrieve the items from.

        Returns:
        list[dict]: A list of dictionaries containing all the items in the specified table.
        """
        return list(self._get_table(table).values())

    def get(self, table: str, id: uuid.UUID) -> dict:
        """
        Retrieve a record from the specified table by its ID.

        Args:
            table (str): The name of the table to retrieve the record from.
            id (uuid.UUID): The ID of the record to retrieve.

        Returns:
            dict: The record with the specified ID.
        """
        return self._get_table(table)[id]

    def create(self, table: str, data: dict) -> dict:
        """
        Creates a new record in the specified table with the given data.

        Args:
            table (str): The name of the table to create the record in.
            data (dict): A dictionary containing the data for the new record.

        Returns:
            dict: The newly created record.
        """
        self._get_table(table)[data["id"]] = data
        return data

    def update(self, table: str, id: uuid.UUID, data: dict) -> dict:
        """
        Update a record in the specified table with the given ID and data.

        Args:
            table (str): The name of the table to update the record in.
            id (uuid.UUID): The ID of the record to update.
            data (dict): The new data to update the record with.

        Returns:
            dict: The updated record.
        """
        self._get_table(table)[id].update(data)
        return self._get_table(table)[id]

    def remove(self, table, id: uuid.UUID) -> None:
        """
        Remove a record from the specified table by its ID.

        Args:
            table (str): The name of the table to remove the record from.
            id (uuid.UUID): The ID of the record to remove.

        Returns:
            None
        """
        del self._get_table(table)[id]
