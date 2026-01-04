import pytest

from ice_ai.reasoning.task_graph import TaskGraph, TaskNode


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_add_and_get_node():
    """
    Invariant:
    A TaskGraph must allow adding and retrieving TaskNode objects
    deterministically by id.
    """

    graph = TaskGraph()

    node = TaskNode(
        id="n1",
        kind="analyze",
        description="Analyze codebase",
    )

    graph.add_node(node)

    retrieved = graph.get_node("n1")
    assert retrieved is node
    assert retrieved.id == "n1"
    assert retrieved.kind == "analyze"


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_rejects_duplicate_nodes():
    """
    Invariant:
    TaskGraph must reject nodes with duplicate IDs.
    """

    graph = TaskGraph()

    node = TaskNode(
        id="dup",
        kind="plan",
        description="Plan workflow",
    )

    graph.add_node(node)

    with pytest.raises(ValueError):
        graph.add_node(node)


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_dependencies_and_dependents():
    """
    Invariant:
    Dependencies (incoming edges) and dependents (outgoing edges)
    must be computed correctly.
    """

    graph = TaskGraph()

    n1 = TaskNode(id="n1", kind="plan", description="Plan")
    n2 = TaskNode(id="n2", kind="analyze", description="Analyze")
    n3 = TaskNode(id="n3", kind="validate", description="Validate")

    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_node(n3)

    graph.add_dependency("n1", "n2")
    graph.add_dependency("n2", "n3")

    assert graph.dependencies_of("n2") == ["n1"]
    assert graph.dependencies_of("n3") == ["n2"]

    assert graph.dependents_of("n1") == ["n2"]
    assert graph.dependents_of("n2") == ["n3"]
    assert graph.dependents_of("n3") == []


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_roots_and_leaves():
    """
    Invariant:
    Roots have no incoming dependencies.
    Leaves have no outgoing dependencies.
    """

    graph = TaskGraph()

    a = TaskNode(id="a", kind="plan", description="Plan")
    b = TaskNode(id="b", kind="analyze", description="Analyze")
    c = TaskNode(id="c", kind="validate", description="Validate")

    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)

    graph.add_dependency("a", "b")
    graph.add_dependency("b", "c")

    assert graph.roots() == ["a"]
    assert graph.leaves() == ["c"]


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_detects_cycles():
    """
    Invariant:
    TaskGraph must detect cycles and mark the DAG as invalid.
    """

    graph = TaskGraph()

    n1 = TaskNode(id="n1", kind="step", description="Step 1")
    n2 = TaskNode(id="n2", kind="step", description="Step 2")

    graph.add_node(n1)
    graph.add_node(n2)

    graph.add_dependency("n1", "n2")
    graph.add_dependency("n2", "n1")  # cycle

    assert graph.is_valid_dag() is False


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_is_valid_dag_for_acyclic_graph():
    """
    Invariant:
    Acyclic graphs must be considered valid DAGs.
    """

    graph = TaskGraph()

    n1 = TaskNode(id="n1", kind="plan", description="Plan")
    n2 = TaskNode(id="n2", kind="execute", description="Execute")

    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_dependency("n1", "n2")

    assert graph.is_valid_dag() is True


@pytest.mark.unit
@pytest.mark.domain
def test_task_graph_to_dict_snapshot_is_stable():
    """
    Invariant:
    to_dict() must produce a fully serializable, stable snapshot
    of the cognitive graph.
    """

    graph = TaskGraph()

    node = TaskNode(
        id="x",
        kind="analyze",
        description="Analyze input",
        required_capabilities={"analysis"},
        suggested_agent="analyzer",
        metadata={"source": "unit-test"},
    )

    graph.add_node(node)

    snapshot = graph.to_dict()

    assert "nodes" in snapshot
    assert "edges" in snapshot
    assert "roots" in snapshot
    assert "leaves" in snapshot
    assert "valid_dag" in snapshot

    assert snapshot["nodes"]["x"]["kind"] == "analyze"
    assert snapshot["valid_dag"] is True
