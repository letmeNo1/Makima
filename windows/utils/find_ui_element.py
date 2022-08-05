from .stack import Stack
import time


def wait_function(func, timeout, root_element, query_string, query_method):
    star_time = time.time()
    end_time = time.time() + timeout / 1000
    while True:
        result = func(root_element, query_string, query_method)
        if result is not None:
            finish_time = time.time() - star_time
            print("Found element in {} s".format(finish_time))
            return result
        if time.time() > end_time:
            raise TimeoutError


def find_element_by_query(root_element, query_string, query_method):
    element_attribute = ""
    all_node = Stack()
    all_node.push(root_element)
    result = None
    while all_node.is_not_empty():
        element = all_node.pop()
        elements_list = element.get_acc_children_elements()

        if query_method == "by automation":
            element_attribute = element.get_automation_id

        elif query_method == "by text":
            element_attribute = element.get_acc_name or element.get_acc_value

        elif query_method == "by role":
            element_attribute = element.get_acc_role_name

        if element_attribute == query_string:
            result = element

        if len(elements_list) > 0:
            for child_element in elements_list:
                if child_element._i_object_id == 0:
                    all_node.push(child_element)
    return result


def find_elements_by_query(root_element, query_string, query_method):
    element_attribute = ""
    all_node = Stack()
    all_node.push(root_element)
    result = []
    while all_node.is_not_empty():
        element = all_node.pop()
        elements_list = element.get_acc_children_elements()

        if query_method == "by automation":
            element_attribute = element.get_automation_id

        elif query_method == "by text":
            element_attribute = element.get_acc_name or element.get_acc_value

        elif query_method == "by role":
            element_attribute = element.get_acc_role_name

        if element_attribute == query_string:
            result.append(element)

        if len(elements_list) > 0:
            for child_element in elements_list:
                if child_element._i_object_id == 0:
                    all_node.push(child_element)
    return result


def find_element_by_automation_id_by_wait(timeout, root_element, automation_id, ):
    return wait_function(find_element_by_query, timeout, root_element, automation_id, "by automation")
