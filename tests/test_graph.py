from pertchart.graph import Node, Graph


def test_empty_node():
    node = Node(id="ID")
    assert node.id == "ID"
    assert node.start == 0
    assert node.duration == 0
    assert node.end == 0
    assert node.responsible == ""
    assert node.pred == []


def test_node_init():
    obj = {
        "Tid": "ID",
        "start": 2,
        "duration": 3,
        "end": 4,
        "responsible": "resp",
        "pred": ["START"],
    }

    node = Node(
        id=obj["Tid"],
        start=obj["start"],
        duration=obj["duration"],
        end=obj["end"],
        responsible=obj["responsible"],
    )
    assert node.id == obj["Tid"]
    assert node.start == obj["start"]
    assert node.duration == obj["duration"]
    assert node.end == obj["end"]
    assert node.responsible == obj["responsible"]
    assert node.pred == []


def test_node_from_obj():
    obj = {
        "Tid": "ID",
        "start": 2,
        "duration": 3,
        "end": 4,
        "responsible": "resp",
    }

    node = Node.from_dict(obj)

    assert node.id == obj["Tid"]
    assert node.start == obj["start"]
    assert node.duration == obj["duration"]
    assert node.end == obj["end"]
    assert node.responsible == obj["responsible"]
    assert node.pred == []


def test_node_tid_alias():
    node = Node(id="AA")
    assert node["Tid"] == "AA"
    assert node["id"] == "AA"


def test_graph_from_json(json_obj):
    g = Graph.from_json(json_obj)

    assert len(g.node_dict) == 10
    assert g.node_dict["START"].id == "START"
    assert [p.id for p in g.node_dict["T1.8"].pred] == ["T1.5", "T1.6", "T1.7"]
