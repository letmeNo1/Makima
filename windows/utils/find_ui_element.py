from .stack import Stack


def find_element_by_text(root_element, automation_id):
    all_node = Stack()
    all_node.push(root_element)
    while all_node.is_not_empty():
        element = all_node.pop()
        if element.get_automation_id == automation_id:
            return element
        if len(element.get_acc_children_elements) != 0 :
            for child_element in element.get_acc_children_elements():
                print(child_element.get_automation_id)
                all_node.push(child_element)

