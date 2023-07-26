from pertchart import PertChart


def test_get_graph_from_json():
    g = PertChart.from_json("tests/input/sample_test_cases.json").graph

    assert len(g.node_dict) == 10


def test_calculate_values_from_graph():
    p = PertChart.from_json("tests/input/sample_test_cases.json")

    p.calculate_values()


def test_print_graph():
    p = PertChart.from_json("tests/input/sample_test_cases.json")
    g = p.graph
    
    p.calculate_values().create_pert_chart(task_list=g)
