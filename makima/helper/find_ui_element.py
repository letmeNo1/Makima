import platform
import re

import time

from makima.helper.stack import Stack

if platform.system() == "Windows":
    from makima.windows.image_object import ImageObject
elif platform.system() == "Darwin":
    from makima.mac.image_object import ImageObject
from makima.openCV.kmeans_run import kmeans_run


def __find_ui_element(element,**query):
    for query_method, query_string in query.items():
        if "contain" in query_method:
            element_attr: str = getattr(element, 'get_' + query_method.replace("_contain",""))
            return str(element_attr).find(query_string) != -1
        elif "matchs" in query_method:
            element_attr: str = getattr(element, 'get_' + query_method.replace("_matchs",""))
            return re.match(str(element_attr), query_string) is None
        else:
            element_attr: str = getattr(element, 'get_' + query_method)
            return element_attr == query_string
            

def wait_function(timeout, func, root, **query):
    time_started_sec = time.time()
    query_string = list(query.values())[0]
    query_method = list(query.keys())[0]
    while time.time() < time_started_sec + timeout / 1000.0:
        result = func(root, **query)
        if result is not None:
            finish_time = time.time() - time_started_sec
            # print("Found element in {} s".format(finish_time))
            return result
    error = "Can't find element/elements in %s s by %s = %s" % (timeout / 1000.0, query_method, query_string)
    raise TimeoutError(error)


def wait_exist(timeout, func, *args, **query):
    rst = False
    time_started_sec = time.time()
    query_string = list(query.values())[0]
    query_method = list(query.keys())[0]
    while time.time() < time_started_sec + timeout / 1000.0:
        result = func(*args, **query)
        if len(result)>0:
            finish_time = time.time() - time_started_sec
            # print("Found element in {} s".format(finish_time))
            rst = True
            return rst
    return rst


def wait_function_by_image(timeout, func, path, distance, algorithms_name):
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout / 1000.0:
        result = func(path, distance, algorithms_name)
        if result is not None:
            finish_time = time.time() - time_started_sec
            return result
    error = "Can't find element/elements in %s s by image" % (timeout / 1000.0)
    raise TimeoutError(error)





def find_element_by_query(root, **query):
    all_node = Stack()
    all_node.push(root)
    result = None

    while all_node.is_not_empty():
        element = all_node.pop()

        elements_list = element.get_acc_children_elements()
        rst = __find_ui_element(element, **query)


        if rst:
            element.set_last_ele(all_node.pop())
            element.set_next_ele(last_element)
            result = element
            break

        last_element = element
        if len(elements_list) > 0:
            for child_element in elements_list:
                all_node.push(child_element)
    return result


def find_elements_by_query( *args, **query):
    all_node = Stack()
    all_node.push(args[0])
    result = []

    while all_node.is_not_empty():
        element = all_node.pop()

        elements_list = element.get_acc_children_elements()

        rst = __find_ui_element(element, **query)

        if rst:
            element.set_last_ele(all_node.pop())
            element.set_next_ele(last_element)
            result.append(element)

        last_element = element
        if len(elements_list) > 0:
            for child_element in elements_list:
                all_node.push(child_element)
    return result

def find_element_by_image(path, distance, algorithms_name):
    x, y = kmeans_run(path, distance, algorithms_name)
    if x is not None:
        return ImageObject(x, y)
    else:
        return None