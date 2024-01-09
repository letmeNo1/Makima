Makima - Automated Testing on desktop
=================================
-   [English](#Background)
-   [中文版](#背景)

Background
==========

This is a desktop automated testing framework based on accessibility api. At the same time, with the help of the open source framework of Ctype, the purpose of calling the Mac and Windows system-level API is achieved.

Install 
===============

pip install Makima

Getting started
===============

**For Mac**

pass

**For Windows**

Requires system version >= Windows 7

Application element locate tool
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
from makima.helper.operation_mac import Init_App_Ref_For_Mac

makima = Init_App_Ref_For_Mac()    
teams_ins = makima(name="Microsoft Teams")
```

 ***For Windows：***
 ```
from makima.helper.operation_win import Init_App_Ref_For_Win

makima = Init_App_Ref_For_Win()   
teams_ins = makima(name = "Microsoft Teams")
```

***support query：***

Both mac and windows support,  `name =` is used as the search criterion by default when the query type is not specified,

`name =` full matching 
```
name = "Calendar | Microsoft Teams"
```
`name_contains=` partial matching 
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
Return Current window state, e.g. 0: "standard", 1: "maximum", 2: "minimize"


* `get_last_ele -> WinUIElement`: 
Return last element


* `get_next_ele -> WinUIElement`: 
Return next element


**Attribute@non-property:**

* `get_clickable_point() -> tuple(x,y)`:  
Return tuple (x, y) if a clickable point was retrieved, or None otherwise


* `get_acc_children_elements() -> list[WinUIElement]`:
Return children elements


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


* `get_selected -> bool `: 
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


* `get_element_at_position(x,y) ->MacUIElement`:
Gets the UIElement object at the specified coordinates


* `get_acc_children_elements()`:
Return children elements


* `get_position()`:
Gets the current element coordinates


* `get_size()`:
Gets the current element width, height


* `get_parent() -> MacUIElement`:  
Return parent element

* `get_center_coordinates()`
Return center coordinates of UIElement object

## Action For Windows and Mac

**Method:**

Find method

For all find method, `**query` can use all attribute from `attribute@property`, and support `contains` and `matches`
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

For all action method  
`x_coordinate`, `y_coordinate` 
are optional and defaults to None, which means use the coordinate of the current element.  
`x_offset`, `y_offset` are optional. The offset xy is offset based on the current xy axis

* `click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse click events


* `hover(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse hover events


* `double_click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulate a double mouse click


* `right_click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
Simulates mouse right click events


* `drag_to(self,to_x, to_y, duration, x_coordinate, y_coordinate, x_offset, y_offset)`:
Simulates dragging an element to the specified coordinates

* `input_text(text)`: 
Simulates input event

* `clear(text)`: 
Clear input field


# Keyboard event

## Windows only
Supports single or multiple key combinations
```
from makima.windows.utils.keyboard import WinKeyboard

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
from makima.mac.utils.keyboard import MacKeyboard

makima_kb = MacKeyboard()

# Simulate the Enter key
makima_kb.send_keys(makima_kb.codes.RETURN)

# Simulating copy and paste
makima_kb.send_keys(makima_kb.codes.KEY_V, makima_kb.mask_codes.COMMAND)


# Simulating ctrl + command + A
makima_kb.send_keys(makima_kb.codes.KEY_A, makima_kb.codes.Ctrl, makima_kb.mask_codes.COMMAND)

```

Notice!
When there are two or more keys, the Mac and Windows parameters are not the same, and when the operating system is Mac, the Mac key combination needs to be matched with the keycode of the mask type. The order in which arguments are passed also affects the actual performance of keypresses.

       
# Mouse event
Most mouse events are contained within the element object operations, so we won't cover them here

## Windows only

```
from makima.windows.utils.keyboard import WinMouse

makima_mouse = WinMouse()

# The wheel moves up 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,-100)

# The wheel moves down 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,100)
```

## Mac only
```
from makima.mac.utils.keyboard import MacMouse

makima_mouse = MacMouse()

# The wheel moves up 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,-100)

# The wheel moves down 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,100)

```

# Common

## Windows only

```
from makima.windows.utils.keyboard import WinCommon

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
from makima.mac.utils.common import MacCommon

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



背景
==========

这是一个基于无障碍api的桌面自动化测试框架。同时，借助开源的Ctype框架，实现了对Mac和Windows系统级API的调用。

安装 
===============

pip install Makima

版本要求 
===============
**对于 Mac**

无

**对于 Windows**

需要系统版本>= Windows 7

应用程序元素定位工具
===============
**对于 Mac**

Accessibility Inspector：Xcode -> 打开 Developer Tools

使用`Accessibility Inspector`可以提供一种快速查找这些属性的方法。

**对于 Windows**

下载  [inspect.exe](https://github.com/letmeNo1/Aki-Tools/blob/main/inspect.exe)

使用`inspect.exe`可以提供一种快速查找这些属性的方法。

初始化
==========

### 通过应用名称/窗口名称初始化UIElementRef
 
 ***对于 Mac：***      
```
from makima.helper.operation_mac import Init_App_Ref_For_Mac

makima = Init_App_Ref_For_Mac()    
teams_ins = makima(name="Microsoft Teams")
```

 ***对于 Windows：***
 ```
from makima.helper.operation_win import Init_App_Ref_For_Win

makima = Init_App_Ref_For_Win()   
teams_ins = makima(name = "Microsoft Teams")
```

***支持的查找方式：***

Windows 和Mac 通用，当不指定查询类型时，默认使用' name = '作为搜索条件。

`name =` 完全匹配
```
name = "Calendar | Microsoft Teams"
```
`name_contains=` 模糊匹配
```
name_contains = "Calendar | Microsoft Teams"
```
`name_matches` 正则表达式匹配
```
name_matches = "^Automation.*Teams$"
```

*对于 Windows*

额外支持`class_name`作为额外的查询条件

e.g. `teams_ins = makima(name_contains="| Microsoft Teams",class_name="")`

or pass a handle object directly
e.g. 
```
teams_hwnd = makima_common.find_windos(name="Microsoft Teams")[0]
teams_ins = makima(hwnd=teams_hwnd)
```

*对于 Mac*

额外支持`pid`作为查询条件

e.g. `self.makima(pid="1234")`


# UIElementRef

UIElement通过`Init_App_Ref_For_Win`/`Init_App_Ref_For_Mac`返回

## Windows支持的属性:

**Attribute@property:**

* `get_current_hwnd -> str`:  
返回当前元素的相关窗口的句柄


* `get_toggle_state -> str`:  
返回当前元素的开关状态(前提是元素是开关类型的元素)。.


* `get_acc_value -> str`:   
返回当前元素的 Value, 对应 LegacyIAccessible.Value


* `get_acc_keyboardshortcut -> str`:  
返回当前元素的 keyboardshortcut, 对应 LegacyIAccessible.KeyboardShortcutProperty


* `get_automation_id -> str`: 返回当前元素的 automationid,


* `get_class_name -> str`:  返回当前元素的 class name


* `get_control_type_name -> str`: 返回当前元素的 control type name


* `get_is_enabled -> bool`: 返回当前元素的 enabled status


* `get_acc_name -> str`: 返回当前元素的 accessible name


* `get_default_action -> str`:  
返回当前元素的 default_action


* `get_description -> str`:   
返回当前元素的 accessible description, 对应 LegacyIAccessibleDescriptionProperty


* `get_acc_role -> str`:  
返回当前元素的 accessible role, 对应 LegacyIAccessibleRoleProperty


* `get_state -> str`:   
返回当前元素的 state text, 对应 LegacyIAccessibleStateProperty


* `get_window_state -> str`:  
返回当前窗口状态，例如 0:"standard"， 1: " maximuim "， 2: "minimize"


* `get_last_ele -> WinUIElement`: 
返回上一个元素

* `get_next_ele -> WinUIElement`: 
返回下一个元素


**Attribute@non-property:**

* `get_clickable_point() -> tuple(x,y)`:  
如果检索到了可单击的坐标，则返回元组(x, y)，否则不返回


* `get_acc_children_elements() -> list[WinUIElement]`:
返回子级元素


* `get_acc_location() -> tuple (left, top, right, bottom)`: 
返回完全包围UIElement的矩形的坐标。返回元组(left, top, right, bottom)


* `get_parent() -> WinUIElement`:返回父级元素

## Attribute Mac only:

**Attribute@property:**

* `get_role -> str`:
返回当前元素的 role value


* `get_identifier: -> str`:
返回当前元素的 identifier


* `get_title: -> str`:
返回当前元素的 title



* `get_value -> str`: 
返回当前元素的 value


* `get_label -> str`: 
返回当前元素的 label


* `get_role_description -> str`: 
返回当前元素的 role description


* `get_help -> str`: 
返回当前元素的 help


* `get_sub_role -> str `: 
返回当前元素的 sub role


* `get_selected -> bool`: 
返回当前元素是否被选中

**Attribute@non-property:**

* `get_attributes() -> str`:
返回当前元素的所有属性


* `get_actions() -> list`:
返回当前元素上可用的操作列表


* `get_pid()`:
返回当前元素的pid


* `perform_action(action)`:
在UIElement对象上执行指定的操作


* `get_element_at_position(x,y) ->MacUIElement`:
获取指定坐标处的UIElement对象


* `get_acc_children_elements()`:
返回子元素


* `get_position()`:
获取当前元素坐标


* `get_size()`:
获取当前元素的宽度、高度


* `get_parent() -> MacUIElement`:  
返回父元素


* `get_center_coordinates()`
返回UIElement对象的中心坐标


## 适用于Windows和Mac操作系统

**方法:**

查找方法

对于所有find方法，` query`可以使用`attribute@property`中的所有属性，并支持`contains`和`matches`
如
  ```
  ele(acc_name = "Microsoft Teams")
  ele(acc_name = "Microsoft Teams",acc_role = "input")
  ele(acc_name_contains = "teams",acc_role = "input")
  ele(acc_name_matches = "*.teams*.")
  ```

* `ele(timeout =5, **query) -> WinUIElement`: 
查找元素，搜索元素的默认超时时间是5秒, timeout将抛出错误。返回一个单元素对象


* `eles(timeout =5, **query) -> List[WinUIElement]`:  
查找元素，搜索元素的默认超时时间是5秒, timeout将抛出错误。返回多个元素对象


* `check_element_exist(timeout =5, **query) -> bool`: 
检查元素是否存在，搜索元素的默认超时时间是5秒, timeout将抛出错误。返回`True`或`False`


* `scroll_to_find_element(scroll_time=15, timeout =5, **query) -> WinUIElement`:  
通过滚动查找元素，搜索元素的默认超时时间是5秒, timeout将抛出错误。


操作方法

对于所有操作方法
`x_coordinate`、`y_coordinate`
是可选的，默认值为None，这表示使用当前元素的坐标。
`x_offset`、`y_offset`是可选的。偏移量xy是基于当前xy轴的偏移量

* `click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
模拟鼠标点击事件


* `hover(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
模拟鼠标悬停事件


* `double_click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
模拟鼠标双击


* `right_click(x_coordinate=None, y_coordinate=None, x_offset: float = None, y_offset: float = None)`: 
模拟鼠标右键事件


* `drag_to(self,to_x, to_y, duration, x_coordinate, y_coordinate, x_offset, y_offset)`:
模拟拖动一个元素到指定的坐标

* `input_text(text)`: 
模拟输入事件

* `clear(text)`: 
清空输入字段


# 键盘事件

## 仅限Windows
Supports single or multiple key combinations
```
from makima.windows.utils.keyboard import WinKeyboard

makima_kb = WinKeyboard()

# Simulate the Enter key
makima_kb.send_keys(makima_kb.codes.RETURN)

# Simulating copy and paste
makima_kb.send_keys(makima_kb.codes.KEY_C,makima_kb.codes.KEY_V)

# Simulating ctrl + alt + A
makima_kb.send_keys(self.makima_kb.codes.ALT,self.makima_kb.codes.CONTROL,self.makima_kb.codes.KEY_A)
```

## 仅限Mac
支持单键或多键组合
```
from makima.mac.utils.keyboard import MacKeyboard

makima_kb = MacKeyboard()

# Simulate the Enter key
makima_kb.send_keys(makima_kb.codes.RETURN)

# Simulating copy and paste
makima_kb.send_keys(makima_kb.codes.KEY_V, makima_kb.mask_codes.COMMAND)


# Simulating ctrl + command + A
makima_kb.send_keys(makima_kb.codes.KEY_A, makima_kb.codes.Ctrl, makima_kb.mask_codes.COMMAND)

```

注意!
当有两个或两个以上的键时，Mac和Windows参数不相同，当操作系统为Mac时，需要将Mac键组合与mask类型的keycode进行匹配。传递参数的顺序也会影响按键的实际表现。

       
# 鼠标事件
大多数鼠标事件都包含在元素对象操作中，因此这里不做介绍

## 仅限Windows

```
from makima.windows.utils.keyboard import WinMouse

makima_mouse = WinMouse()

# The wheel moves up 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,-100)

# The wheel moves down 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,100)
```

## 仅限Mac
```
from makima.mac.utils.keyboard import MacMouse

makima_mouse = MacMouse()

# The wheel moves up 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,-100)

# The wheel moves down 100, x,y means start position 
makima_mouse.scroll_wheel(x,y,100)

```

# 通常接口

## 仅限 Windows

```
from makima.windows.utils.keyboard import WinCommon

makima_common = WinCommon()

# Waiting for the window to appear,The default timeout is 5 seconds, The rules for passing parameters are the same as
`Init_App_Ref_For_Mac`
makima_common.find_window_by_wait(name=None, timeout=5, **kwargs)

# Finds the window and returns a list of `HWND_OBJ`
makima_common.find_windows(name=None, **query)

# Open the application from the start menu
makima_common.open_app_by_name(name)

```
Windows额外支持`HWND OBJ`

```
teams_obj = makima_common.find_windows(name="Teams", **query)

# 获取窗口标题
teams_obj.get_window_title

# 获取窗口类名
teams_obj.get_window_class_name

# 强制窗口显示在前面
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


## 仅限Mac
```
from makima.mac.utils.common import MacCommon

makima_common = MacCommon()

# 激活窗口，让它出现在前面
makima_common.active_window(name)

# 隐藏窗口
makima_common.hide_window(name)

# 打开窗口
makima_common.unhide_window(name)

# 确定应用程序是否已经启动
makima_common.is_finished_launching(name)
```
