from __future__ import annotations
from typing import List, Dict, Optional, Any


class Node:
    def __init__(
        self,
        id: str,
        start: int = 0,
        duration: int = 0,
        end: int = 0,
        responsible: str = "",
    ) -> None:
        self.id = id
        self.start = start
        self.duration = duration
        self.end = end
        self.responsible = responsible
        self.pred = []

    @staticmethod
    def from_dict(obj: Dict[str, Any]) -> Node:
        if obj.get("Tid"):
            id = obj["Tid"]
        else:
            id = obj["id"]
        return Node(
            id=id,
            start=obj.get("start", 0),
            duration=obj.get("duration", 0),
            end=obj.get("end", 0),
            responsible=obj.get("responsible", ""),
        )

    def __getitem__(self, key: str) -> Any:
        if key == "Tid":
            key = "id"
        return getattr(self, key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        if key == "Tid":
            key = "id"
        setattr(self, key, value)

    def __str__(self):
        pred_str = [p.id for p in self.pred]
        return (
            f"<id:{self.id}, start:{self.start}, duration:{self.duration}, "
            f"end:{self.end}, responsible:{self.responsible}, pred:{pred_str}>"
        )


class Graph:
    def __init__(self):
        self._node_dict: Dict[str, Node] = {}
        self._edge_list = []

        self._node_dict["START"] = Node(id="START")

    @property
    def node_dict(self):
        return self._node_dict

    def add_node(self, node: Node):
        self._node_dict[node.id] = node

    @staticmethod
    def from_json(json_obj: Dict) -> Graph:
        """Creates a graph object from the JSON

        Raises:
            - KeyError: if one of the predecessors nodes is not declared before
              the node which is referencing it.

        Args:
            json_obj: json object loaded from file
        Returns:
            graph containing the nodes.
        """
        graph = Graph()
        for v in json_obj.values():
            node = Node.from_dict(v)
            for p in v.get("pred", []):
                node.pred.append(graph._node_dict[p])
            graph.add_node(node)

        return graph

    def __getitem__(self, key: str) -> Node:
        return self._node_dict[key]

    def __iter__(self):
        return self._node_dict.__iter__()

    def items(self):
        return self._node_dict.items()
    
    def keys(self):
        return self._node_dict.keys()
