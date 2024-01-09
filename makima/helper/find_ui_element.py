import platform
import re

import time

from apollo_makima.helper.stack import Stack

if platform.system() == "Windows":
    from apollo_makima.windows.image_object import ImageObject
elif platform.system() == "Darwin":
    from apollo_makima.mac.image_object import ImageObject
from apollo_makima.openCV.kmeans_run import kmeans_run


def __assert_ui_element(element, **query):
    rst = []
    for query_method, query_string in query.items():
        if "contains" in query_method:
            element_attr: str = getattr(element, 'get_' + query_method.replace("_contains", ""))
            rst.append(str(element_attr).find(query_string) != -1)
        elif "matches" in query_method:
            element_attr: str = getattr(element, 'get_' + query_method.replace("_matches", ""))
            rst.append(re.search(query_string, str(element_attr)) is not None)
        else:
            element_attr: str = getattr(element, 'get_' + query_method)
            rst.append(element_attr == query_string)
    return all(rst)


def wait_function(timeout, func, root, **query):
    time_started_sec = time.time()
    query_string = list(query.values())[0]
    query_method = list(query.keys())[0]
    reverse = True
    end_with_timeout = False
    while time.time() < time_started_sec + timeout:
        if end_with_timeout:
            reverse = False
        result, end_with_timeout = func(timeout, root, reverse, **query)
        if result is not None:
            finish_time = time.time() - time_started_sec
            return result
    error = "Can't find element/elements in %s s by %s = %s" % (timeout, query_method, query_string)
    raise TimeoutError(error)


def wait_any(timeout, func, root, querylist):
    time_started_sec = time.time()
    reverse = True
    end_with_timeout = False
    while time.time() < time_started_sec + timeout:
        if end_with_timeout:
            reverse = False
        for query in querylist:
            result, end_with_timeout = func(timeout, root, reverse, **query)
            if result is not None:
                return result
    error = "Can't find element/elements"
    raise TimeoutError(error)


def wait_exist(timeout, func, root, **query):
    rst = False
    reverse = True
    end_with_timeout = False
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout:
        if end_with_timeout:
            reverse = False
        result, end_with_timeout = func(timeout, root, reverse, **query)
        if result is not None:
            return True
    return rst


def wait_function_by_image(timeout, func, path, distance, algorithms_name):
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout:
        result = func(path, distance, algorithms_name)
        if result is not None:
            finish_time = time.time() - time_started_sec
            return result
    error = "Can't find element/elements in %s s by image" % timeout
    raise TimeoutError(error)


def __traversal_node(timeout, all_node, reverse, is_muti, **query):
    result = []
    time_started_sec = time.time()
    ui_tree = []
    while all_node.is_not_empty() and time.time() < time_started_sec + timeout / 2:
        element = all_node.pop()
        ui_tree.append(element)
        elements_list = element.get_acc_children_elements()
        rst = __assert_ui_element(element, **query)

        if rst:
            next_ele = all_node.pop()
            all_node.push(next_ele)
            if reverse:
                element._set_last_ele(ui_tree[ui_tree.index(element) - 1])
                element._set_next_ele(None if all_node.size() == 0 else next_ele)
            else:
                element._set_last_ele(None if all_node.size() == 0 else next_ele)
                element._set_next_ele(ui_tree[ui_tree.index(element) - 1])
            result.append(element)

            if not is_muti:
                break

        if len(elements_list) > 0:
            if reverse:
                elements_list.reverse()
            for child_element in elements_list:
                all_node.push(child_element)
    '''
    End_with_timeout indicates that because the timeout 
    has expired and not because the list loop has finished, 
    an infinite loop may occur and the outer layer should 
    try to search in reverse order
    '''
    end_with_timeout = all_node.size() > 0
    if not is_muti:
        return result[0] if len(result) > 0 else None, end_with_timeout
    else:
        return result, end_with_timeout


def find_element_by_query(timeout, root, reverse, **query):
    all_node = Stack()
    all_node.push(root)
    result, end_with_timeout = __traversal_node(timeout, all_node, reverse, False, **query)
    return result, end_with_timeout


def find_elements_by_query(timeout, root, reverse, **query):
    all_node = Stack()
    all_node.push(root)
    result, end_with_timeout = __traversal_node(timeout, all_node, reverse, True, **query)
    return result, end_with_timeout


def find_element_by_image(path, distance, algorithms_name):
    x, y = kmeans_run(path, distance, algorithms_name)
    if x is not None:
        return ImageObject(x, y)
    else:
        raise Exception("Unable to find image")
