import pydot
import json
import os

module_dir = os.path.dirname(__file__)
rel_path = '../UCSD_courses.json'
abs_file_path = os.path.join(module_dir, rel_path)
with open(abs_file_path) as f:
    '''
    UCSD_courses.json should be formatted with ANDs as each index of the list. ORs are placed into a list within the
    outer list. Concurrent courses are tagged with an asterisk (*) after the course name.
    '''
    COURSE_DICT = json.load(f)


def find_next_node(graph, parent):
    """
    Adds all the prerequisite courses to the graph and their prerequisites, recursively.
    :param graph: The pydot.Dot object which holds the tree
    :param parent: The course node which we are adding its prerequisite classes to
    """
    course = parent.get_name()
    if COURSE_DICT[course] is None:
        return
    for prereq in COURSE_DICT[course]:
        if isinstance(prereq, list):
            # OR COURSES
            for or_req in prereq:
                child = add_course(graph, or_req, parent, 'blue')
                find_next_node(graph, child)
        else:
            # AND COURSES
            child = add_course(graph, prereq, parent, 'red')
            find_next_node(graph, child)


def add_course(graph, course, parent, color):
    """
    Creates child node for course and attaches it to the parent node in the graph given with the color given.
    :param graph: The pydot.Dot object which holds the tree
    :param course: A string with the child's course name
    :param parent: The parent node we want to attach the child node to
    :param color: The color we want to connect the nodes with (depends on type of prereq AND/OR/COREQ)
    :return child: The child node we created, representing the prerequisite of the parent course
    """
    if course[-1] == '*':
        # Concurrent course
        color = 'green'
        course = course[:-1]
    child = pydot.Node(course)
    graph.add_node(child)
    edge = pydot.Edge(parent, child, color=color)
    graph.add_edge(edge)
    return child



def get_prereqs(course_name):
    """
    Main entry point - Runs all code to create a tree of prerequisites necessary to take a course.
    :param course_name: A string with the name of the course you are looking prereqs for
    :return graph: The pydot.Dot object which holds the tree of the course and all its prereqs
    """

    graph = pydot.Dot(graph_type='digraph')
    target = pydot.Node(course_name)
    graph.add_node(target)
    find_next_node(graph, target)

    return graph
