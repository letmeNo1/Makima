import time

from makima.pywinauto import WindowSpecification, timings

from makima.Intelligent_search.IntelligentSearch import intelligent_search
from makima.pywinauto.findwindows import ElementAmbiguousError, ElementNotFoundError
from loguru import logger
from makima.pywinauto.keyboard import send_keys


def _convert_criteria(criteria):
    """
    Convert specific keys in the criteria dictionary to the required keys.

    :param criteria: The original criteria dictionary.
    :return: The modified criteria dictionary with converted keys.
    """
    if 'acc_name' in criteria:
        criteria['title'] = criteria.pop('acc_name')
    elif 'acc_name_contains' in criteria:
        criteria['title_re'] = f".*{criteria.pop('acc_name_contains')}.*"
    elif 'acc_name_matches' in criteria:
        criteria['title_re'] = criteria.pop('acc_name_matches')
    if 'acc_role' in criteria:
        criteria['loc_control_type'] = criteria.pop('acc_role')
    else:
        return criteria

    return criteria


class WinElement:
    def __init__(self, root: WindowSpecification):
        self.root = root

    def get_children(self):
        return self.root.find_all('')

    def ele(self, query: str = None, timeout=10, **criteria) -> 'WinUIElementExt':
        timings.Timings.window_find_timeout = timeout

        """
        Search for a single element based on a query or criteria.

        :param query: A string query for intelligent search.
        :param criteria: Additional criteria for searching child windows.
        :return: A WinUIElementExt object representing the found element.
        """
        criteria = _convert_criteria(criteria)
        if query:
            rst = intelligent_search(self.element, query)
            return WinUIElementExt(rst)
        element = self.root.child_window(**criteria)
        try:
            element.find_all()
        except ElementAmbiguousError as e:
            logger.debug("ElementAmbiguousError: Multiple elements found matching the criteria.")
            # Re-find all elements matching the criteria
            elements = self.root.descendants(**criteria)
            for elem in elements:
                logger.debug(f"{elem.element_info.name}, {elem.element_info.loc_control_type}")
            raise e
        except AttributeError:
            pass
        return WinUIElementExt(element, self.root)

    def eles(self, query: str = None, timeout=10, **criteria) -> list:
        timings.Timings.window_find_timeout = timeout

        """
        Search for multiple elements based on criteria and return a list of WinUIElementExt objects.

        :param query: (Not used in this method)
        :param criteria: Additional criteria for searching descendant elements.
        :return: A list of WinUIElementExt objects matching the criteria.
        """
        criteria = self._convert_criteria(criteria)

        elements = self.root.descendants(**criteria)
        return [WinUIElementExt(element, self.root) for element in elements]

    def is_scrollable(self, element):
        try:
            # 尝试获取滚动条
            scrollbars = element.descendants(control_type="ScrollBar")
            return len(scrollbars) > 0
        except Exception as e:
            logger.debug(f"Error checking scrollability: {e}")
            return False

    def scroll_to_find_element(self, query: str = None, timeout=5, direction='down', max_scrolls=15, amount=1,
                               **criteria) -> 'WinUIElementExt':
        """
        Scroll through the window to find a single element based on a query or criteria.

        :param query: A string query for intelligent search.
        :param timeout: Timeout for finding the element.
        :param direction: Direction to scroll, default is 'down'.
        :param max_scrolls: Maximum number of scrolls, default is 5.
        :param amount: Amount to scroll each time, default is 1.
        :param criteria: Additional criteria for searching child windows.
        :return: A WinUIElementExt object representing the found element.
        """

        # Try to find the element without scrolling first
        for i in range(max_scrolls):
            try:
                ele = self.ele(query, 1, **criteria)
                if ele.element_info.visible:
                    send_keys('{DOWN}')
                    send_keys('{DOWN}')
                    return self.ele(query, 1, **criteria)

            except (ElementAmbiguousError, AttributeError, ElementNotFoundError):
                send_keys('{DOWN}')
                send_keys('{DOWN}')



class WinUIElementExt:
    def __init__(self, element, root=None):
        self.element = element
        self.root = root

    def click(self):
        self.element.click_input()

    def invoke(self):
        self.element.click()

    def get_acc_name(self):
        if self.element.element_info.help_text:
            return self.element.element_info.help_text
        return self.element.element_info.rich_text()

    @property
    def acc_name(self):
        if self.element.element_info.help_text:
            return self.element.element_info.help_text
        return self.element.element_info.rich_text()

    @property
    def element_info(self):
        return self.element.element_info

    def find_after(self, **query):
        query = _convert_criteria(query)

        stack = [self.root]
        current_runtime_id = self.element.element_info.runtime_id
        found_current_element = False

        while stack:
            current_element = stack.pop(0)

            # 检查是否找到了当前元素
            if current_element.element_info.runtime_id == current_runtime_id:
                found_current_element = True
                continue

            # 只有在找到当前元素之后才开始查找符合条件的元素
            if found_current_element:
                # 检查当前元素是否符合查询条件
                match = True
                for key, value in query.items():
                    if not hasattr(current_element.element_info, key) or getattr(current_element.element_info,
                                                                                 key) != value:
                        match = False
                        break
                if match:
                    return WinUIElementExt(current_element)  # 找到第一个符合条件的元素后立即返回

            try:
                children = current_element.children()
                stack.extend(children)
            except Exception as e:
                print(f"Error accessing children: {e}")

        # 如果没有找到符合条件的元素，抛出自定义异常
        raise RuntimeError("No matching element found")