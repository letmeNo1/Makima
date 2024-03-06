import platform
import re

from makima.helper.stack import Stack
from makima.helper.queue import Queue

if platform.system() == "Windows":
    from makima.windows.image_object import ImageObject
elif platform.system() == "Darwin":
    from makima.mac.image_object import ImageObject
from makima.openCV.kmeans_run import kmeans_run


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
    while time.time() < time_started_sec + timeout:
        result = func(timeout, root, **query)
        if result is not None:
            finish_time = time.time() - time_started_sec
            return result
    error = "Can't find element/elements in %s s by %s = %s" % (timeout, query_method, query_string)
    raise TimeoutError(error)


def wait_any(timeout, func, root, querylist):
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout:
        for query in querylist:
            result = func(timeout, root, **query)
            if result is not None:
                return result
    error = "Can't find element/elements"
    raise TimeoutError(error)


def wait_exist(timeout, func, root, **query):
    rst = False
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout:
        result = func(timeout, root, **query)
        if result is not None:
            return True
    return rst


def wait_function_by_image(timeout, func, path, distance, algorithms_name):
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout:
        result = func(path, distance, algorithms_name)
        if result is not None:
            return result
    error = "Can't find element/elements in %s s by image" % timeout
    raise TimeoutError(error)


import time


def __traversal_node(timeout, all_node, is_muti, **query):
    result = []
    time_started_sec = time.time()
    ui_tree = []
    time_end = time_started_sec+ timeout/2
    if is_muti:
        condition = False
    else:
        condition = time.time() < time_end
    while all_node.size() > 0 or condition:
        if all_node.size() == 0:
            return None
        element = all_node.pop()
        ui_tree.append(element)
        elements_list = element.get_acc_children_elements()
        rst = __assert_ui_element(element, **query)

        if rst:
            next_ele = all_node.peek() if all_node.is_not_empty() else None
            element._set_last_ele(ui_tree[ui_tree.index(element) - 1] if ui_tree.index(element) > 0 else None)
            element._set_next_ele(next_ele)
            result.append(element)

            if not is_muti:
                break
        if elements_list is not None:
            for child_element in elements_list:
                all_node.push(child_element)
    if not is_muti:
        return result[0] if result else None
    else:
        return result


def find_element_by_query(timeout, root, **query):
    all_node = Queue()
    all_node.push(root)
    result = __traversal_node(timeout, all_node, False, **query)
    return result


def find_elements_by_query(timeout, root, **query):
    all_node = Queue()
    all_node.push(root)
    result = __traversal_node(timeout, all_node, True, **query)
    return result


def find_element_by_image(path, distance, algorithms_name):
    x, y = kmeans_run(path, distance, algorithms_name)
    if x is not None:
        return ImageObject(x, y)
    else:
        raise Exception("Unable to find image")
