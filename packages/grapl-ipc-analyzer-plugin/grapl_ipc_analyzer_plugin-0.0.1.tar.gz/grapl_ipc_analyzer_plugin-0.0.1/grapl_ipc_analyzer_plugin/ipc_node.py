from copy import deepcopy
from typing import *

from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ForwardEdgeView
from grapl_analyzerlib.prelude import DynamicNodeQuery, DynamicNodeView, ProcessQuery, ProcessView
from grapl_analyzerlib.nodes.comparators import StrCmp, IntCmp, _str_cmps, _int_cmps
from grapl_analyzerlib.schemas import NodeSchema, ProcessSchema
from pydgraph import DgraphClient


class IpcQuery(DynamicNodeQuery):
    def __init__(self) -> None:
        super(IpcQuery, self).__init__("Ipc", IpcView)

    def with_src_pid(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "IpcQuery":
        self.set_int_property_filter("src_pid", _int_cmps("src_pid", eq=eq, gt=gt, lt=lt))
        return self

    def with_dst_pid(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "IpcQuery":
        self.set_int_property_filter("dst_pid", _int_cmps("dst_pid", eq=eq, gt=gt, lt=lt))
        return self

    def with_ipc_type(self, eq=StrCmp, contains=StrCmp, ends_with=StrCmp) -> "IpcQuery":
        self.set_str_property_filter(
            "ipc_type", _str_cmps("ipc_type", eq=eq, contains=contains, ends_with=ends_with)
        )
        return self

    def with_ipc_creator(
            self, ipc_creator_query: "Optional[ProcessQuery]" = None
    ) -> "IpcQuery":
        if ipc_creator_query:
            ipc_creator = deepcopy(ipc_creator_query)
        else:
            ipc_creator = ProcessQuery()
        self.set_forward_edge_filter("ipc_creator", ipc_creator)
        ipc_creator.set_reverse_edge_filter("~ipc_creator", self, "ipc_creator")
        return self

    def with_ipc_recipient(
            self, ipc_recipient_query: "Optional[ProcessQuery]" = None
    ) -> "IpcQuery":
        if ipc_recipient_query:
            ipc_recipient = deepcopy(ipc_recipient_query)
        else:
            ipc_recipient = ProcessQuery()

        self.set_forward_edge_filter("ipc_recipient", ipc_recipient)
        ipc_recipient.set_reverse_edge_filter("~ipc_recipient", self, "ipc_recipient")
        return self

    def query(
            self,
            dgraph_client: DgraphClient,
            contains_node_key: Optional[str] = None,
            first: Optional[int] = 1000,
    ) -> List["IpcView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
            self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["IpcView"]:
        return self._query_first(dgraph_client, contains_node_key)


class IpcView(DynamicNodeView):
    def __init__(
            self,
            dgraph_client: DgraphClient,
            node_key: str,
            uid: str,
            node_type: str,
            src_pid: Optional[int] = None,
            dst_pid: Optional[int] = None,
            ipc_creator: Optional[ProcessQuery] = None,
            ipc_recipient: Optional[ProcessQuery] = None,
    ):
        super(IpcView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.src_pid = src_pid
        self.dst_pid = dst_pid
        self.ipc_creator = ipc_creator
        self.ipc_recipient = ipc_recipient

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {"src_pid": int, "dst_pid": int}

    @staticmethod
    def _get_forward_edge_types() -> Mapping[str, "EdgeViewT"]:
        f_edges = {"ipc_creator": ProcessView, "ipc_recipient": ProcessView}

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_forward_edges(self) -> "Mapping[str, ForwardEdgeView]":
        f_edges = {"ipc_creator": self.ipc_creator, "ipc_recipient": self.ipc_recipient}

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {"src_pid": self.src_pid, "dst_pid": self.dst_pid}
        return {p[0]: p[1] for p in props.items() if p[1] is not None}


class IpcSchema(NodeSchema):

    def __init__(self) -> None:
        super(IpcSchema, self).__init__()
        (
            self
            .with_int_prop('src_pid')
            .with_int_prop('dst_pid')
            .with_forward_edge('ipc_creator', ProcessSchema)
            .with_forward_edge('ipc_recipient', ProcessSchema)
        )

    @staticmethod
    def self_type() -> str:
        return 'Ipc'
