from typing import *

from grapl_analyzerlib.nodes.comparators import IntCmp, _int_cmps, StrCmp
from grapl_analyzerlib.nodes.process_node import ProcessView
from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ReverseEdgeView
from grapl_analyzerlib.prelude import DynamicNodeQuery, DynamicNodeView, ProcessQuery
from pydgraph import DgraphClient

from grapl_os_user_analyzer_plugin.grapl_os_user_analyzer_plugin.assumed_user_id_node import (
    UserIdAssumptionView,
)


class UserIdQuery(DynamicNodeQuery):
    def __init__(self) -> None:
        super(UserIdQuery, self).__init__("UserId", UserIdView)

    def with_user_id(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "UserIdQuery":
        self.set_int_property_filter(
            "user_id", _int_cmps("user_id", eq=eq, gt=gt, lt=lt)
        )
        return self

    def with_asset_id(self, eq=StrCmp, gt=StrCmp, lt=StrCmp) -> "UserIdQuery":
        self.set_int_property_filter(
            "asset_id", _int_cmps("asset_id", eq=eq, gt=gt, lt=lt)
        )
        return self

    def with_user_id_assumptions(
        self, user_id_assumption_query: "UserIdAssumptionQuery"
    ):
        user_id_assumption = user_id_assumption_query or ProcessQuery()
        self.set_reverse_edge_filter(
            "~user_id_assumptions", self, "user_id_assumptions"
        )
        user_id_assumption.set_forward_edge_filter(
            "user_id_assumptions", user_id_assumption
        )
        return self

    def query(
        self,
        dgraph_client: DgraphClient,
        contains_node_key: Optional[str] = None,
        first: Optional[int] = 1000,
    ) -> List["UserIdView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
        self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["UserIdView"]:
        return self._query_first(dgraph_client, contains_node_key)


class UserIdView(DynamicNodeView):
    def __init__(
        self,
        dgraph_client: DgraphClient,
        node_key: str,
        uid: str,
        node_type: str,
        user_id: Optional[int] = None,
        asset_id: Optional[str] = None,
        user_id_assumptions: Optional[List["UserIdAssumptionView"]] = None,
    ):
        super(UserIdView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.user_id = user_id
        self.asset_id = asset_id
        self.assumed_by = user_id_assumptions

    def get_user_id(self) -> Optional[int]:
        if self.user_id is None:
            self.user_id = self.fetch_property("user_id", int)

        return self.user_id

    def get_assumptions(
        self, filter: Optional[Union["UserIdAssumptionQuery"]] = None
    ) -> List[UserIdAssumptionView]:
        assert not filter, "Filtering is not currently implemented"

        if not self.assumed_by:
            self.assumed_by = (
                self.fetch_edges("~assumed_user_id", [UserIdAssumptionView]) or []
            )

        return self.assumed_by

    def get_assuming_processes(
        self, filter: Optional[Union["ProcessQuery"]] = None
    ) -> List[ProcessView]:
        assert not filter, "Filtering is not currently implemented"

        if not self.assumed_by:
            self.assumed_by = (
                self.fetch_edges("~assumed_user_id", [UserIdAssumptionView]) or []
            )

        assuming_processes = []
        for assumption in self.assumed_by:
            assuming_process = assumption.get_assuming_process()
            if assuming_process:
                assuming_processes.append(assuming_process)

        return assuming_processes

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {"user_id": int}

    @staticmethod
    def _get_reverse_edge_types() -> Mapping[str, Tuple["EdgeViewT", str]]:
        return {"~assumed_user_id": ([UserIdAssumptionView], "user_id_assumptions")}

    def _get_reverse_edges(self) -> "Mapping[str,  ReverseEdgeView]":
        r_edges = {
            "~assumed_user_id": ("user_id_assumptions", self.user_id_assumptions)
        }

        return {r[0]: r[1] for r in r_edges.items() if r[1][0] is not None}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {"user_id": self.user_id}
        return {p[0]: p[1] for p in props.items() if p[1] is not None}


from grapl_os_user_analyzer_plugin.assumed_user_id_node import (
    UserIdAssumptionQuery,
    UserIdAssumptionView,
)
