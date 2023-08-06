from typing import *

from grapl_analyzerlib.nodes.comparators import IntCmp, _int_cmps
from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ForwardEdgeView
from grapl_analyzerlib.prelude import (
    DynamicNodeQuery,
    DynamicNodeView,
    ProcessQuery,
    ProcessView,
)
from pydgraph import DgraphClient


class UserIdAssumptionQuery(DynamicNodeQuery):
    def __init__(self) -> None:
        super(UserIdAssumptionQuery, self).__init__(
            "UserIdAssumption", UserIdAssumptionView
        )

    def with_assumed_timestamp(
        self, eq=IntCmp, gt=IntCmp, lt=IntCmp
    ) -> "UserIdAssumptionQuery":
        self.set_int_property_filter(
            "assumed_timestamp", _int_cmps("assumed_timestamp", eq=eq, gt=gt, lt=lt)
        )
        return self

    def with_assuming_process_id(
        self, eq=IntCmp, gt=IntCmp, lt=IntCmp
    ) -> "UserIdAssumptionQuery":
        self.set_int_property_filter(
            "assuming_process_id", _int_cmps("assuming_process_id", eq=eq, gt=gt, lt=lt)
        )
        return self

    def with_user_id(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "UserIdAssumptionQuery":
        self.set_int_property_filter(
            "user_id", _int_cmps("user_id", eq=eq, gt=gt, lt=lt)
        )
        return self

    def with_assumed_user_id(
        self, used_id_query: "Optional[UserIdQuery]" = None
    ) -> "UserIdAssumptionQuery":
        assuming_process = used_id_query or ProcessQuery()
        self.set_forward_edge_filter("assumed_user_id", assuming_process)
        assuming_process.set_reverse_edge_filter(
            "~assumed_user_id", self, "assumed_user_id"
        )
        return self

    def with_assuming_process(
        self, assuming_process_query: "Optional[ProcessQuery]" = None
    ) -> "UserIdAssumptionQuery":
        assuming_process = assuming_process_query or ProcessQuery()
        self.set_forward_edge_filter("assuming_process", assuming_process)
        assuming_process.set_reverse_edge_filter(
            "~assuming_process", self, "assuming_process"
        )
        return self

    def query(
        self,
        dgraph_client: DgraphClient,
        contains_node_key: Optional[str] = None,
        first: Optional[int] = 1000,
    ) -> List["UserIdAssumptionView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
        self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["UserIdAssumptionView"]:
        return self._query_first(dgraph_client, contains_node_key)


class UserIdAssumptionView(DynamicNodeView):
    def __init__(
        self,
        dgraph_client: DgraphClient,
        node_key: str,
        uid: str,
        node_type: str,
        user_id: Optional[int] = None,
        assuming_process_id: Optional[int] = None,
        assuming_process: Optional[ProcessView] = None,
        assumed_user_id: Optional[ProcessView] = None,
    ):
        super(UserIdAssumptionView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.user_id = user_id
        self.assuming_process_id = assuming_process_id
        self.assuming_process = assuming_process
        self.assumed_user_id = assumed_user_id

    def get_user_id(self) -> Optional[int]:
        if not self.user_id:
            self.user_id = self.fetch_property("user_id", int)
        return self.user_id

    def get_assuming_process_id(self) -> Optional[int]:
        if not self.assuming_process_id:
            self.assuming_process_id = self.fetch_property("assuming_process_id", int)
        return self.assuming_process_id

    def get_assuming_process(self) -> Optional[ProcessView]:
        if not self.assuming_process:
            self.assuming_process = self.fetch_edge("assuming_process", ProcessView)
        return self.assuming_process

    def get_assumed_user_id(self) -> Optional[int]:
        if not self.assumed_user_id:
            self.assumed_user_id = self.fetch_edge(
                "assumed_user_id", UserIdAssumptionView
            )
        return self.assumed_user_id

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {"user_id": int, "assuming_process_id": int}

    @staticmethod
    def _get_forward_edge_types() -> Mapping[str, "EdgeViewT"]:
        f_edges = {"assuming_process": ProcessView, "assumed_user_id": ProcessView}

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_forward_edges(self) -> "Mapping[str, ForwardEdgeView]":
        f_edges = {
            "assuming_process": self.assuming_process,
            "assumed_user_id": self.assumed_user_id,
        }

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {"user_id": self.src_pid, "assumed_process_id": self.dst_pid}
        return {p[0]: p[1] for p in props.items() if p[1] is not None}


from grapl_os_user_analyzer_plugin.user_id_node import UserIdQuery
