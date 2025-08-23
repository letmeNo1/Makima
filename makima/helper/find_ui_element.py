import platform
import re
from collections import deque

# Import the ImageObject class based on the operating system
if platform.system() == "Windows":
    from makima.windows.image_object import ImageObject
elif platform.system() == "Darwin":
    from makima.mac.image_object import ImageObject
from makima.openCV.kmeans_run import kmeans_run

# Helper function to determine if a UI element meets the given query conditions
def __assert_ui_element(element, **query):
    rst = []
    # Iterate through the query conditions
    for query_method, query_string in query.items():
        if "contains" in query_method:
            # Get the element's attribute
            element_attr: str = getattr(element, 'get_' + query_method.replace("_contains", ""))
            # Check if the element's attribute contains the specified string
            rst.append(str(element_attr).find(query_string) != -1)
        elif "matches" in query_method:
            # Get the element's attribute
            element_attr: str = getattr(element, 'get_' + query_method.replace("_matches", ""))
            # Check if the element's attribute matches the regular expression
            rst.append(re.search(query_string, str(element_attr)) is not None)
        else:
            # Get the element's attribute
            element_attr: str = getattr(element, 'get_' + query_method)
            # Check if the element's attribute is equal to the specified string
            rst.append(element_attr == query_string)
    # Return the logical AND result of all query condition judgments
    return all(rst)

# Continuously call the func function within the specified timeout until an element that meets the conditions is found or the timeout occurs
def wait_function(timeout, func, root, **query):
    # Record the start time
    time_started_sec = time.time()
    # Get the query string
    query_string = list(query.values())[0]
    # Get the query method
    query_method = list(query.keys())[0]
    # Calculate the end time
    end_time = time_started_sec + timeout
    while time.time() < end_time:
        # Call the func function
        result = func(root, **query)
        if isinstance(result, list):
            if len(result) > 0:
                return result
        else:
            if result is not None:
                # Record the completion time
                finish_time = time.time() - time_started_sec
                return result
    if func.__name__ == "find_elements_by_query":
        return []
    else:
        # Throw a timeout exception
        error = "Can't find element in %s s by %s = %s" % (timeout, query_method, query_string)
        raise TimeoutError(error)

# Within the specified timeout, sequentially try to call the func function with each query condition in the querylist until an element that meets the conditions is found or the timeout occurs
def wait_any(timeout, func, root, querylist):
    # Record the start time
    time_started_sec = time.time()
    # Calculate the end time
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        for query in querylist:
            # Call the func function
            result = func(root, **query)
            if result is not None:
                return result
    # Throw a timeout exception
    error = "Can't find element/elements"
    raise TimeoutError(error)

# Continuously call the func function within the specified timeout to determine if an element that meets the conditions can be found
def wait_exist(timeout, func, root, **query):
    rst = False
    # Record the start time
    time_started_sec = time.time()
    # Calculate the end time
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        # Call the func function
        result = func(root, **query)
        if result is not None:
            return True
    return rst

# Continuously call the func function within the specified timeout to determine if the element that meets the conditions has disappeared
def wait_disappear(timeout, func, root, **query):
    rst = False
    # Record the start time
    time_started_sec = time.time()
    # Calculate the end time
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        # Call the func function
        result = func(root, **query)
        if result is None:
            return True
    return rst

# Continuously call the func function within the specified timeout to find an element by image
def wait_function_by_image(timeout, func, path, distance, algorithms_name):
    # Record the start time
    time_started_sec = time.time()
    # Calculate the end time
    end_time = time_started_sec + timeout

    while time.time() < end_time:
        # Call the func function
        result = func(path, distance, algorithms_name)
        if result is not None:
            return result
    # Throw a timeout exception
    error = "Can't find element/elements in %s s by image" % timeout
    raise TimeoutError(error)

import time

# Use breadth-first search (BFS) to traverse the node tree to find UI elements that meet the conditions
def __traversal_node(root, is_muti, **query):
    # Used to store elements that meet the conditions
    rst_elements = []
    # Used to record the IDs of elements that have been visited
    history_element_id = []
    # Use a deque to implement BFS. Initially, add the root node and level 1 to the queue
    queue = deque([(root, 1)])
    # Record the initial level
    init_level = 1
    # Record the previous element
    prev_element = None
    # Record the next element
    next_element = None
    # Continue traversing while the queue is not empty
    while queue:
        # Remove an element and its level from the queue
        element, level = queue.popleft()
        # If it is a Windows system, get the RuntimeId property of the element
        if platform.system() == "Windows":
            element_id = element.get_RuntimeIdProperty
        else:
            element_id = str(element)
        # If the current level is greater than the initial level, update the initial level
        if level > init_level:
            init_level += 1
        # Determine if the current element meets the query conditions
        rst = __assert_ui_element(element, **query)
        if rst:
            # If the queue is not empty, get the next element in the queue
            if queue:
                next_element, _ = queue[0]
            # Set the previous element of the current element
            element._set_last_ele(prev_element)
            # Set the next element of the current element
            element._set_next_ele(next_element)
            # If only one element needs to be found, return the current element directly
            if not is_muti:
                return element
            # Add the element that meets the conditions to the result list
            rst_elements.append(element)
        # If the element's ID has not been visited
        if element_id not in history_element_id:
            # Update the previous element to the current element
            prev_element = element
            if element_id is not None:
                # Record the element's ID
                history_element_id.append(element_id)
            # Get the child elements of the current element
            children = element.get_acc_children_elements()
            if children:
                # Add the child elements and their levels to the queue
                for child in children:
                    queue.append((child, level + 1))
    # If only one element needs to be found, return None
    if not is_muti:
        return None
    else:
        # Return all elements that meet the conditions
        return rst_elements

# Find the first element that meets the conditions
def find_element_by_query(root, **query):
    result = __traversal_node(root, False, **query)
    return result

# Find all elements that meet the conditions
def find_elements_by_query(root, **query):
    result = __traversal_node(root, True, **query)
    return result

# Find an element by image
def find_element_by_image(path, distance, algorithms_name):
    # Call the kmeans_run function to perform image search
    x, y = kmeans_run(path, distance, algorithms_name)
    if x is not None:
        # Create and return an ImageObject instance
        return ImageObject(x, y)
    else:
        # Throw an exception
        raise Exception("Unable to find image")