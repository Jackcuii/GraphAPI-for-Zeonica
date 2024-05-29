import zeoapi.dag as dag
def make_a_layout(dag):
    start = dag.find_node_without_dep()
    assert start is not None, "No node without dependencies found"
    