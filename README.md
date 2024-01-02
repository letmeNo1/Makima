Makima - Automated Testing on desktop
=================================
-   [English](#Background)
-   [中文版](#背景)

Background
==========

This is a desktop automated testing framework based on accessibility api. At the same time, with the help of the open source framework of Ctype, the purpose of calling the Mac and Windows system-level API is achieved.

Install 
===============

pip install ApolloMakima

Getting started

**For Mac**

pass

**For Windows**
Requires system version >= Windows 7

Applicaion element locate tool
===============
**For Mac**

Accessibility Inspector：Xcode -> Open Developer Tools

Using `Accessibility Inspector` can provide a quick way to find these attributes.

**For Windows**

download  [inspect.exe](https://github.com/letmeNo1/Aki-Tools/blob/main/inspect.exe)

Using `inspect.exe` can provide a quick way to find these attributes.


Init
==========

### initialize an UIElementRef by app name/window name
 
 ***For Mac：***      
```
from apollo_makima.helper.operation_mac import Init_App_Ref_For_Mac

makima = Init_App_Ref_For_Mac()    
teams_ins = makima(name="Microsoft Teams")

or

from apollo_base.makima_base import MakimaBase

class YourClass(MakimaBase)
    super().__init__()

def your_function
    self.makima(name= Microsoft Teams")
```

***For Windows：***
 ```
from apollo_makima.helper.operation_win import Init_App_Ref_For_Win

makima = Init_App_Ref_For_Win()   
teams_ins = makima(name = "Microsoft Teams")

from apollo_base.makima_base import MakimaBase

class YourClass(MakimaBase)
    super().__init__()

def your_function
    self.makima(name_contains="| Microsoft Teams")
 ```

***support query：***

Both mac and windows support,  `name =` is used as the search criterion by default when the query type is not specified,

`name =` full matching 
```
name = "Calendar | Microsoft Teams"
```
`name_contains=` partial matching and   
```
name_contains = "Calendar | Microsoft Teams"
```
`name_matches`regular expression matching
```
name_matches = "^Automation.*Teams$"
```

for *Windows*
Additional support for `class_name` as an additional lookup condition
e.g. `teams_ins = makima(name_contains="| Microsoft Teams",class_name="")`

or pass a handle object directly
e.g. 
```
teams_hwnd = makima_common.find_windos(name="Microsoft Teams")[0]
teams_ins = makima(hwnd=teams_hwnd)
```

for *Mac*
Additional support for `pid` as an lookup condition
e.g. `self.makima(pid="1234")`


# UIElementRef

UIElement is return by `Init_App_Ref_For_Win`/`Init_App_Ref_For_Mac`
   
## Attribute Windows only:

**Attribute@property:**

* `get_current_hwnd -> str`:  
Return a handle of current UIElement related Window


* `get_toggle_state -> str`:  
Return the toggle status of the current element (provided the element is a toggle element).


* `get_acc_value -> str`:   
Return UIElement's value, corresponding to LegacyIAccessible.Value


* `get_acc_keyboardshortcut -> str`:  
Return UIElement's keyboardshortcut, corresponding to LegacyIAccessible.KeyboardShortcutProperty


* `get_automation_id -> str`: Return UIElement's automationid,


* `get_class_name -> str`:  Return UIElement's class name


* `get_control_type_name -> str`: Return UIElement's control type name


* `get_is_enabled -> bool`: Return UIElement's enabled status


* `get_acc_name -> str`: Return UIElement's accessible name


* `get_default_action -> str`:  
Return UIElement's default_action


* `get_description -> str`:   
Return UIElement's accessible description, corresponding to LegacyIAccessibleDescriptionProperty


* `get_acc_role -> str`:  
Return UIElement's accessible role, corresponding to LegacyIAccessibleRoleProperty


* `get_state -> str`:   
Return UIElement's state text, corresponding to LegacyIAccessibleStateProperty


* `get_window_state -> str`:  
Return Current window state, e.g. 0: "standard", 1: "maxiuim", 2: "minimize"


* `get_last_ele -> WinUIElement`: 
Return last element


* `get_next_ele -> WinUIElement`: 
Return next element


**Attribute@non-property:**

* `get_clickable_point() -> tuple(x,y)`:  
Return tuple (x, y) if a clickable point was retrieved, or None otherwise


* `get_acc_children_elements() -> list[WinUIElement]`:
Return chilren elements


* `get_acc_location() -> tuple (left, top, right, bottom)`:  
Return the coordinates of the rectangle that completely encloses the UIElement.Return tuple (left, top, right, bottom)


* `get_parent() -> WinUIElement`:  
Return parent element

## Attribute Mac only:

**Attribute@property:**

* `get_role -> str`:
Return UIElement's role value


* `get_identifier: -> str`:
Return UIElement's identifier


* `get_title: -> str`:
Return UIElement's title



* `get_value -> str`: 
Return UIElement's value


* `get_label -> str`: 
Return UIElement's label


* `get_role_description -> str`: 
Return UIElement's role description


* `get_help -> str`: 
Return UIElement's help


* `get_sub_role -> str `: 
Return UIElement's sub role


* `get_selected -> boo `: 
Return UIElement if selected

**Attribute@non-property:**

* `get_attributes() -> str`:
Return all attribute ofr UIElement


* `get_actions() -> list`:
Return a list of the actions available on the UIElement


* `get_pid()`:
Return the PID of the AXUIElement


* `perform_action(action)`:
Perform the specified action on the UIElement object


* `get_element_at_position(x,y)`:
Gets the UIElement object at the specified coordinates


* `get_acc_children_elements()`:
Return chilren elements


* `get_position()`:
Gets the current element coordinates


* `get_size()`:
Gets the current element width, hight


* `get_parent() -> MacUIElement`:  
Return parent element

* `get_center_coordinates()`
Return center coordinates of UIElement object

## Action For Windows and Mac

**Method:**

Find method

For all find metod, `**query` can use all attribute from `attribute@property`, and support `contains` and `matches`
e.g
  ```
  ele(acc_name = "Microsoft Teams")
  ele(acc_name = "Microsoft Teams",acc_role = "input")
  ele(acc_name_contains = "teams",acc_role = "input")
  ele(acc_name_matches = "*.teams*.")
  ```

* `ele(timeout =5, **query) -> WinUIElement`: 
Find element, The default timeout period for searching elements is 5s，Timeout will throw an error. Return a single-element object


* `eles(timeout =5, **query) -> List[WinUIElement]`:  
Find elements, The default timeout period for searching elements is 5s，Timeout will throw an error. Return multiple element objects


* `check_element_exist(timeout =5, **query) -> bool`: 
Check whether the element exists, The default timeout period for searching elements is 5s，Timeout will throw an error. Return `True` or `False`


* `scroll_to_find_element(scroll_time=15, timeout =5, **query) -> WinUIElement`:  
Find element by scroll, The default timeout period for searching elements is 5s，Timeout will throw an error.


Action Method

For all action metod  
`x_coordinate`, `y_coordinate` 
are optional and defaults to None, which means use the coordinate of the current element.  
`x_offset`, `y_offset` are optional. The offset xy is offset based on the current xy axis

* `click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse click events


* `hover(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse hover events


* `double_click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse hover events


* `right_click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse right click events


* `drag_to(self,to_x, to_y, duration, x_coordinate, y_coordinate, x_offset, y_offset)`:
Offset Click. The offset xy is offset based on the current xy axis

* `input_text(text)`: 
Simulates input event

* `clear(text)`: 
Clear input field


# Keybord event

## Windows only
Supports single or multiple key combinations
```
from apollo_makima.windows.utils.keyboard import WinKeyboard

makima_kb = WinKeyboard()

# Simulate the Enter key
makima_kb.send_keys(makima_kb.codes.RETURN)

# Simulating copy and paste
makima_kb.send_keys(makima_kb.codes.KEY_C,makima_kb.codes.KEY_V)

# Simulating ctrl + alt + A
makima_kb.send_keys(self.makima_kb.codes.ALT,self.makima_kb.codes.CONTROL,self.makima_kb.codes.KEY_A)
```

## Mac only
Supports single or multiple key combinations
```
from apollo_makima.mac.utils.keyboard import MacKeyboard

makima_kb = MacKeyboard()

# Simulate the Enter key
makima_kb.send_keys(makima_kb.codes.RETURN)

# Simulating copy and paste
makima_kb.send_keys(makima_kb.codes.KEY_V, makima_kb.mask_codes.COMMAND)


# Simulating ctrl + command + A
makima_kb.send_keys(makima_kb.codes.KEY_A, makima_kb.codes.Ctrl, makima_kb.mask_codes.COMMAND)

```

Notice!
When there are two or more keys, the mac and window parameters are not the same, so you need to match the mac key combination with the keycode of the mask type. The order in which arguments are passed also affects the actual performance of keypresses

       
# Mouse event
Most mouse events are contained within the element object operations, so we won't cover them here

## Windows only

```
from apollo_makima.windows.utils.keyboard import WinMouse

makima_mouse = WinMouse()

# The wheel moves up 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,-100)

# The wheel moves down 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,100)
```

## Mac only
```
from apollo_makima.mac.utils.keyboard import MacMouse

makima_mouse = MacMouse()

# The wheel moves up 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,-100)

# The wheel moves down 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,100)

```

# Common

## Windows only

```
from apollo_makima.windows.utils.keyboard import WinCommon

makima_common = WinCommon()

# Waiting for the window to appear,The default timeout is 5 seconds, The rules for passing parameters are the same as
`Init_App_Ref_For_Mac`
makima_common.find_window_by_wait(name=None, timeout=5, **kwargs)

# Finds the window and returns a list of `HWND_OBJ`
makima_common.find_windows(name=None, **query)

# Open the application from the start menu
makima_common.open_app_by_name(name)

```
Additional Windows Support `HWND_OBJ`

```
teams_obj = makima_common.find_windows(name="Teams", **query)

#get window title
teams_obj.get_window_title

#get window class name
teams_obj.get_window_class_name

#Force the window to appear at the front
teams_obj.focus_window()

""" 
Maxinum or Mininum windows
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
""" 
teams_obj.show_window(number)


```


## Mac only
```
from apollo_makima.mac.utils.common import MacCommon

makima_common = MacCommon()

# Activate the window so that it appears at the front
makima_common.active_window(name)

# Hide the window
makima_common.hide_window(name)

# Unhide the window
makima_common.unhide_window(name)

# Determine if the application has started
makima_common.is_finished_launching(name)
```
