from dataclasses import dataclass, field
from typing import Dict, List, Optional


SQLITE_DBI_ID = "SQLiteDbi"
BAM_DBI_ID = "SamtoolsBasedDbi"
DEFAULT_DBI_ID = SQLITE_DBI_ID
WORKFLOW_SESSION_TMP_DBI_ALIAS = "workflow_session"


class U2OpStatus:
    """Placeholder for U2OpStatus."""
    pass


class U2DbiRef:
    """Placeholder for U2DbiRef."""
    pass


class U2DbiFactory:
    """Placeholder for U2DbiFactory."""
    pass


class U2Dbi:
    """Placeholder for U2Dbi."""
    pass


class DbiConnection:
    """Placeholder for DbiConnection."""
    pass


class U2DbiFactoryId(str):
    """Simple alias for factory IDs."""
    pass


@dataclass
class TmpDbiRef:
    alias: str = ""
    dbi_ref: U2DbiRef = field(default_factory=U2DbiRef)
    n_users: int = 0


class U2DbiRegistry:
    """
    Keep all DBI types registered in the system.
    """

    def __init__(self, parent=None) -> None:
        self.factories: Dict[U2DbiFactoryId, U2DbiFactory] = {}
        self.pool: Optional[U2DbiPool] = None
        self.tmp_dbis: List[TmpDbiRef] = []
        self.lock = None  # Placeholder for a mutex/lock
        self.session_dbi_connection: Optional[DbiConnection] = None
        self.session_dbi_init_done: bool = False

    def register_dbi_factory(self, factory: U2DbiFactory) -> bool:
        # Implementation depends on factory API
        raise NotImplementedError

    def get_registered_dbi_factories(self) -> List[U2DbiFactoryId]:
        return list(self.factories.keys())

    def get_dbi_factory_by_id(self, factory_id: U2DbiFactoryId) -> Optional[U2DbiFactory]:
        return self.factories.get(factory_id)

    def get_global_dbi_pool(self) -> Optional["U2DbiPool"]:
        return self.pool

    def attach_tmp_dbi(self, alias: str, os: U2OpStatus, factory_id: U2DbiFactoryId) -> U2DbiRef:
        """
        Increases the "number of users"-counter for the dbi, if it exists.
        Otherwise, allocates the dbi and sets the counter to 1.
        """
        raise NotImplementedError

    def detach_tmp_dbi(self, alias: str, os: U2OpStatus) -> None:
        """
        Decreases the "number of users"-counter.
        Deallocates the dbi, if it becomes equal to 0.
        """
        raise NotImplementedError

    def list_tmp_dbis(self) -> List[U2DbiRef]:
        return [t.dbi_ref for t in self.tmp_dbis]

    def get_session_tmp_dbi_ref(self, os: U2OpStatus) -> U2DbiRef:
        """
        Returns the reference to the tmp session dbi.
        If the last is not created yet then it would be created.
        """
        raise NotImplementedError

    def shutdown_session_dbi(self, os: U2OpStatus) -> str:
        """
        WARNING: must be used only in crash handler.
        Closes the session database connection and returns the path to the database file.
        """
        raise NotImplementedError

    # Private helpers
    def _init_session_dbi(self, tmp_dbi_ref: TmpDbiRef) -> None:
        """Creates the session connection and increases the counter for the dbi."""
        raise NotImplementedError

    def _allocate_tmp_dbi(self, alias: str, os: U2OpStatus, factory_id: U2DbiFactoryId) -> U2DbiRef:
        raise NotImplementedError

    def _deallocate_tmp_dbi(self, ref: TmpDbiRef, os: U2OpStatus) -> None:
        raise NotImplementedError


class U2DbiPool:
    """
    Class to access DBI connections.

    Roles:
        creates new DBIs on user request
        track connection live range (using ref counters)
        closes unused DBIs
    """

    DBI_POOL_EXPIRATION_TIME_MSEC: int = 0
    MAX_CONNECTIONS_PER_DBI: int = 0

    def __init__(self, p=None) -> None:
        self.dbi_by_id: Dict[str, U2Dbi] = {}
        self.dbi_counters_by_id: Dict[str, int] = {}
        self.suspended_dbis: Dict[str, U2Dbi] = {}
        self.dbi_suspend_start_time: Dict[U2Dbi, int] = {}
        self.expiration_timer = None  # Placeholder for a timer
        self.lock = None  # Placeholder for a mutex/lock

    def open_dbi(
        self,
        ref: U2DbiRef,
        create: bool,
        os: U2OpStatus,
        properties: Optional[Dict[str, str]] = None,
    ) -> U2Dbi:
        if properties is None:
            properties = {}
        raise NotImplementedError

    def add_ref(self, dbi: U2Dbi, os: U2OpStatus) -> None:
        raise NotImplementedError

    def release_dbi(self, dbi: U2Dbi, os: U2OpStatus) -> None:
        raise NotImplementedError

    def close_all_connections(self, ref: U2DbiRef, os: U2OpStatus) -> None:
        raise NotImplementedError

    # "slots"
    def _check_dbi_pool_expiration(self) -> None:
        raise NotImplementedError

    # Private helpers
    def _get_ids(self, ref: U2DbiRef, os: U2OpStatus) -> List[str]:
        raise NotImplementedError

    def _get_count_of_connections_in_pool(self, url: str) -> int:
        raise NotImplementedError

    def _get_dbi_from_pool(self, dbi_id: str) -> Optional[U2Dbi]:
        return self.dbi_by_id.get(dbi_id)

    def _remove_dbi_record_from_pool(self, dbi_id: str) -> None:
        self.dbi_by_id.pop(dbi_id, None)
        self.dbi_counters_by_id.pop(dbi_id, None)

    def _flush_pool(self, url: str = "", remove_all: bool = False) -> None:
        raise NotImplementedError

    @staticmethod
    def _get_init_properties(url: str, create: bool) -> Dict[str, str]:
        raise NotImplementedError

    @staticmethod
    def _get_id(ref: U2DbiRef, os: U2OpStatus) -> str:
        raise NotImplementedError

    @staticmethod
    def _is_dbi_from_main_thread(dbi_id: str) -> bool:
        raise NotImplementedError

    @staticmethod
    def _create_dbi(ref: U2DbiRef, create: bool, os: U2OpStatus, properties: Dict[str, str]) -> U2Dbi:
        raise NotImplementedError

    @staticmethod
    def _deallocate_dbi(dbi: U2Dbi, os: U2OpStatus) -> None:
        raise NotImplementedError

    @staticmethod
    def _id2url(dbi_id: str) -> str:
        raise NotImplementedError