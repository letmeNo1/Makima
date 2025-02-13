import platform
import re
from collections import deque

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
    end_time = time_started_sec + timeout
    while time.time() < end_time:
        result = func(root, **query)
        if result is not None:
            finish_time = time.time() - time_started_sec
            return result
    error = "Can't find element/elements in %s s by %s = %s" % (timeout, query_method, query_string)
    raise TimeoutError(error)


def wait_any(timeout, func, root, querylist):
    time_started_sec = time.time()
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        for query in querylist:
            result = func(root, **query)
            if result is not None:
                return result
    error = "Can't find element/elements"
    raise TimeoutError(error)


def wait_exist(timeout, func, root, **query):
    rst = False
    time_started_sec = time.time()
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        result = func(root, **query)
        if result is not None:
            return True
    return rst


def wait_function_by_image(timeout, func, path, distance, algorithms_name):
    time_started_sec = time.time()
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        result = func(path, distance, algorithms_name)
        if result is not None:
            return result
    error = "Can't find element/elements in %s s by image" % timeout
    raise TimeoutError(error)


import time


def __traversal_node(root, is_muti, **query):
    rst_elements = []
    history_element_id = []
    queue = deque([(root, 1)])
    init_level = 1
    prev_element = None
    next_element = None
    while queue:
        element, level = queue.popleft()
        if platform.system() == "Windows":
            element_id = element.get_RuntimeIdProperty
        else:
            var = element.get_role
            element_id = str(element)

        if level > init_level:
            init_level += 1
        rst = __assert_ui_element(element, **query)
        if rst:
            if queue:
                next_element, _ = queue[0]
            element._set_last_ele(prev_element)
            element._set_next_ele(next_element)
            if not is_muti:
                return element
            rst_elements.append(element)
        if element_id not in history_element_id:
            prev_element = element
            if element_id is not None:
                history_element_id.append(element_id)
            children = element.get_acc_children_elements()
            if children:
                for child in children:
                    queue.append((child, level + 1))
    if not is_muti:
        return None
    else:
        return rst_elements

def find_element_by_query(root, **query):
    result = __traversal_node(root, False, **query)
    return result


def find_elements_by_query(root, **query):
    result = __traversal_node(root, True, **query)
    return result


def find_element_by_image(path, distance, algorithms_name):
    x, y = kmeans_run(path, distance, algorithms_name)
    if x is not None:
        return ImageObject(x, y)
    else:
        raise Exception("Unable to find image")
