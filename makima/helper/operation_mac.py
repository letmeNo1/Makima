import os
from makima.mac.call_mac_api.call_app_kit import CallAppKit
from makima.mac.ui_element import MacUIElement
import ApplicationServices as AppServ
from makima.mac.utils.common import MacCommon
import multiprocessing


class MacUIElementProxy:
    def __init__(self, request_queue, response_queue):
        self.request_queue = request_queue
        self.response_queue = response_queue
        self._current_id = None

    def __getattr__(self, name):
        def method_proxy(*args, **kwargs):
            if self._current_id is None:
                # First call, no element identifier
                self.request_queue.put((name, args, kwargs, None))
            else:
                # Chained call, include the element identifier
                self.request_queue.put((name, args, kwargs, self._current_id))
            result = self.response_queue.get()
            if isinstance(result, tuple) and result[0] == 'element_id':
                # The returned value is an element identifier, record it
                self._current_id = result[1]
                return self
            return result
        return method_proxy


def worker(request_queue, response_queue, window, window_type, timeout, query):
    mac_common = MacCommon()
    if window is not None:
        if "TopApplication" == window:
            call_app_kit = CallAppKit()
            pid = call_app_kit.get_frontmost_pid()
        else:
            window_obj = mac_common.find_window_by_wait(window_type, timeout, name=window)
            pid = window_obj.get_owner_pid
    else:
        window_obj = mac_common.find_window_by_wait(window_type, timeout, **query)
        pid = window_obj.get_owner_pid
    app_window = AppServ.AXUIElementCreateApplication(int(pid))
    root_instance = MacUIElement(ref=app_window)
    element_instances = {None: root_instance}  # Store element instances, the root instance identifier is None
    element_id_counter = 1  # Element identifier counter

    while True:
        command = request_queue.get()
        if command == 'exit':
            break
        method_name, args, kwargs, element_id = command
        instance = element_instances.get(element_id)
        if instance is None:
            continue
        method = getattr(instance, method_name)
        result = method(*args, **kwargs)
        if isinstance(result, MacUIElement):
            # If the returned value is a MacUIElement instance, assign an identifier and store it
            new_id = element_id_counter
            element_id_counter += 1
            element_instances[new_id] = result
            response_queue.put(('element_id', new_id))
        else:
            response_queue.put(result)


class Init_App_Ref_For_Mac(CallAppKit):
    def __call__(self, window=None, window_type=1, timeout=10, new_process=False, **query):
        if new_process:
            print(f"Main process ID: {os.getpid()}")
            request_queue = multiprocessing.Queue()
            response_queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=worker, args=(request_queue, response_queue, window, window_type, timeout, query))
            p.start()
            print("main process")
            return MacUIElementProxy(request_queue, response_queue)
        else:
            mac_common = MacCommon()
            if window is not None:
                if "TopApplication" == window:
                    pid = self.get_frontmost_pid()
                else:
                    window_obj = mac_common.find_window_by_wait(window_type, timeout, name=window)
                    pid = window_obj.get_owner_pid
            else:
                window_obj = mac_common.find_window_by_wait(window_type, timeout, **query)
                pid = window_obj.get_owner_pid
            app_window = AppServ.AXUIElementCreateApplication(int(pid))
            return MacUIElement(ref=app_window)