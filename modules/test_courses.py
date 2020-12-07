import courses
import pydot


def test_remove_star():
    test_string1 = 'no_star'
    test_string2 = 'with_star*'

    assert courses.remove_star(test_string1) == 'no_star'
    assert courses.remove_star(test_string2) == 'with_star'


def test_add_course():
    graph = pydot.Dot(graph_type='digraph')
    parent = pydot.Node('Parent')
    graph.add_node(parent)
    assert len(graph.obj_dict['nodes']) == 1
    assert len(graph.obj_dict['edges']) == 0

    courses.add_course(graph, 'Child', 'Parent', 'red')
    assert len(graph.obj_dict['nodes']) == 2
    assert len(graph.obj_dict['edges']) == 1
