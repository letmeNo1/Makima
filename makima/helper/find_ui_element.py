import re
import platform

import pkgutil


from makima.helper.stack import Stack
if pkgutil.find_loader('cv2') is not None:
    from makima.openCV.kmeans_run import kmeans_run
if platform.system() == "Darwin":
    from makima.mac.image_object import ImageObject
import time



def wait_function(timeout, use_re, func, *args, **query):
    time_started_sec = time.time()
    query_string = list(query.values())[0]
    query_method = list(query.keys())[0]
    while time.time() < time_started_sec + timeout / 1000.0:
        result = func(use_re, *args, **query)
        if result is not None:
            finish_time = time.time() - time_started_sec
            # print("Found element in {} s".format(finish_time))
            return result
    error = "Can't find element/elements in %s s by %s = %s" % (timeout / 1000.0, query_method, query_string)
    raise TimeoutError(error)


def wait_function_by_image(timeout, func, path, distance, algorithms_name):
    time_started_sec = time.time()
    while time.time() < time_started_sec + timeout / 1000.0:
        result = func(path, distance, algorithms_name)
        if result is not None:
            finish_time = time.time() - time_started_sec
            # print("Found element in {} s".format(finish_time))
            return result
    error = "Can't find element/elements in %s s by image" % (timeout / 1000.0)
    raise TimeoutError(error)


def find_element_by_image(path, distance, algorithms_name):
    x, y = kmeans_run(path, distance, algorithms_name)
    if x is not None:
        return ImageObject(x, y)
    else:
        return None


def find_element_by_query(use_re, *args, **query):
    all_node = Stack()
    all_node.push(args[0])
    result = None

    while all_node.is_not_empty():
        element = all_node.pop()
        elements_list = element.get_acc_children_elements()

        if use_re:
            result_list = [eval("element.get_{}".format(query_method), {}, {"element": element}) for
                           query_method, query_string in query.items() if
                           re.match(str(query_string), str(eval("element.get_{}".format(query_method), {}, {"element":element}))) is not None]
        else:
            result_list = [eval("element.get_{}".format(query_method), {}, {"element": element}) for
                           query_method, query_string in query.items() if
                           eval("element.get_{}".format(query_method), {}, {"element": element})
                           == query_string]
        if len(query) == len(result_list):
            if len(args) > 1 and "last" in args[1]:
                result = all_node.pop()
            elif len(args) > 1 and "next" in args[1]:
                result = last_element
            else:
                result = element
            break

        last_element = element
        if len(elements_list) > 0:
            for child_element in elements_list:
                all_node.push(child_element)
    return result


def find_elements_by_query(use_re, *args, **query):
    all_node = Stack()
    all_node.push(args[0])
    result = []

    while all_node.is_not_empty():
        element = all_node.pop()

        elements_list = element.get_acc_children_elements()

        if use_re:
            result_list = [eval("element.get_{}".format(query_method), {}, {"element": element}) for
                           query_method, query_string in query.items() if
                           re.match(str(query_string), str(eval("element.get_{}".format(query_method), {},
                                                                {"element": element}))) is not None]
        else:
            result_list = [eval("element.get_{}".format(query_method), {}, {"element": element}) for
                           query_method, query_string in query.items() if
                           eval("element.get_{}".format(query_method), {}, {"element": element})
                           == query_string]

        if len(query) == len(result_list):
            result.append(element)

        if len(elements_list) > 0:
            for child_element in elements_list:
                all_node.push(child_element)
    return result
