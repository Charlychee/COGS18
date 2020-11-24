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


def find_next_node(graph, course, complete):
    """
    Adds all the prerequisite courses to the graph and their prerequisites, recursively.
    :param graph: The pydot.Dot object which holds the tree
    :param course: The course name which we are adding its prerequisite classes to
    :param complete: The list of courses that have already been added to the tree. This is to prevent infinite loops.
    """
    if COURSE_DICT[course] is None:
        return
    for prereq in COURSE_DICT[course]:
        if isinstance(prereq, list):
            # OR COURSES
            for or_req in prereq:
                add_course(graph, or_req, course, 'blue')
                find_next_node(graph, or_req, complete)
        else:
            # AND COURSES
            add_course(graph, prereq, course, 'red')
            find_next_node(graph, prereq, complete)


def add_course(graph, course, parent, color):
    """
    Creates child node for course and attaches it to the parent node in the graph given with the color given.
    :param graph: The pydot.Dot object which holds the tree
    :param course: A string with the child's course name
    :param parent: The parent name we want to attach the child node to
    :param color: The color we want to connect the nodes with (depends on type of prereq AND/OR/COREQ)
    """
    if course[-1] == '*':
        # Concurrent course
        color = 'green'
        course = course[:-1]
    child = pydot.Node(course)
    graph.add_node(child)
    edge = pydot.Edge(parent, course, color=color)
    graph.add_edge(edge)


def get_prereqs(course_name):
    """
    Main entry point - Runs all code to create a tree of prerequisites necessary to take a course.
    :param course_name: A string with the name of the course you are looking prereqs for
    :return graph: The pydot.Dot object which holds the tree of the course and all its prereqs
    """

    graph = pydot.Dot(graph_type='digraph')
    target = pydot.Node(course_name)
    graph.add_node(target)
    complete = []
    find_next_node(graph, course_name, complete)

    return graph
