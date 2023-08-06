from typing import *

from grapl_analyzerlib.nodes.comparators import IntCmp, _int_cmps, StrCmp
from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ReverseEdgeView
from grapl_analyzerlib.prelude import DynamicNodeQuery, DynamicNodeView, ProcessQuery
from pydgraph import DgraphClient


class AuidQuery(DynamicNodeQuery):
    def __init__(self) -> None:
        super(AuidQuery, self).__init__("Auid", AuidView)

    def with_auid(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AuidQuery":
        self.set_int_property_filter("auid", _int_cmps("auid", eq=eq, gt=gt, lt=lt))
        return self

    def with_asset_id(self, eq=StrCmp, gt=StrCmp, lt=StrCmp) -> "AuidQuery":
        self.set_int_property_filter(
            "asset_id", _int_cmps("asset_id", eq=eq, gt=gt, lt=lt)
        )
        return self

    def with_auid_assumptions(self, auid_assumption_query: "AuidAssumptionQuery"):
        auid_assumption = auid_assumption_query or ProcessQuery()
        self.set_reverse_edge_filter("~assumed_auid", self, "auid_assumptions")
        auid_assumption.set_forward_edge_filter("assumed_auid", auid_assumption)
        return self

    def query(
        self,
        dgraph_client: DgraphClient,
        contains_node_key: Optional[str] = None,
        first: Optional[int] = 1000,
    ) -> List["AuidView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
        self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["AuidView"]:
        return self._query_first(dgraph_client, contains_node_key)


class AuidView(DynamicNodeView):
    def __init__(
        self,
        dgraph_client: DgraphClient,
        node_key: str,
        uid: str,
        node_type: str,
        auid: Optional[int] = None,
        asset_id: Optional[str] = None,
        auid_assumptions: Optional[List["AuidAssumptionView"]] = None,
    ):
        super(AuidView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.auid = auid
        self.asset_id = asset_id
        self.auid_assumptions = auid_assumptions

    def get_auid(self) -> Optional[int]:
        if self.auid is None:
            self.auid = self.fetch_property("auid", int)

        return self.auid

    def get_auid_assumptions(
        self, filter: Optional[Union["AuidAssumptionQuery", "ProcessQuery"]] = None
    ) -> Optional[int]:
        assert not filter, "Filtering is not currently implemented"

        if self.auid is None:
            self.auid = self.fetch_property("auid", int)

        return self.auid

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {"auid": int}

    @staticmethod
    def _get_reverse_edge_types() -> Mapping[str, Tuple["EdgeViewT", str]]:
        return {"~assumed_auid": ([AuidAssumptionView], "auid_assumptions")}

    def _get_reverse_edges(self) -> "Mapping[str,  ReverseEdgeView]":
        r_edges = {"~assumed_auid": ("auid_assumptions", self.auid_assumptions)}

        return {r[0]: r[1] for r in r_edges.items() if r[1][0] is not None}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {"auid": self.auid}
        return {p[0]: p[1] for p in props.items() if p[1] is not None}


from grapl_os_user_analyzer_plugin.auid_assumption_node import (
    AuidAssumptionQuery,
    AuidAssumptionView,
)
