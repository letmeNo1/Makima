from openCV.kmeans_run import kmeans_run
from .stack import Stack
import time

from ..image_object import ImageObject


def wait_function(timeout, func, *args, **kwargs):
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout / 1000.0:
        result = func(*args, **kwargs)
        if result is not None:
            finish_time = time.time() - time_started_sec
            print("Found element in {} s".format(finish_time))
            return result
        raise TimeoutError


def find_element_by_image(path, distance, **method):
    for key, value in method.items():
        query_method = key
        query_string = value
    x, y = kmeans_run(path, distance)
    if x is not None:
        return ImageObject(x, y)
    else:
        return None


def find_element_by_query(root_element, **query):
    query_method = None
    query_string = None
    element_attribute = ""
    all_node = Stack()
    all_node.push(root_element)
    result = None

    for key, value in query.items():
        query_method = key
        query_string = value

    while all_node.is_not_empty():
        element = all_node.pop()
        elements_list = element.get_acc_children_elements()

        if query_method == "automation_id":
            element_attribute = element.get_automation_id

        elif query_method == "name":
            element_attribute = element.get_acc_name

        elif query_method == "description":
            element_attribute = element.get_acc_description

        elif query_method == "value":
            element_attribute = element.get_acc_value

        elif query_method == "role_name":
            element_attribute = element.get_acc_role_name

        elif query_method == "full_description":
            element_attribute = element.get_full_description

        elif query_method == "class_name":
            element_attribute = element.get_class_nam

        if element_attribute == query_string:
            result = element

        if len(elements_list) > 0:
            for child_element in elements_list:
                if child_element._i_object_id == 0:
                    all_node.push(child_element)
    return result


def find_elements_by_query(root_element, **query):
    query_method = None
    query_string = None
    element_attribute = ""
    all_node = Stack()
    all_node.push(root_element)
    result = []
    while all_node.is_not_empty():
        element = all_node.pop()
        elements_list = element.get_acc_children_elements()
        for key, value in query.items():
            query_method = key
            query_string = value

        if query_method == "automation_id":
            element_attribute = element.get_automation_id

        elif query_method == "text":
            element_attribute = element.get_acc_name or element.get_acc_value or element.get_acc_description

        elif query_method == "role_name":
            element_attribute = element.get_acc_role_name

        elif query_method == "full_description":
            element_attribute = element.get_full_description

        elif query_method == "class_name":
            element_attribute = element.get_class_name

        if element_attribute == query_string:
            result.append(element)

        if len(elements_list) > 0:
            for child_element in elements_list:
                if child_element._i_object_id == 0:
                    all_node.push(child_element)
    return result
