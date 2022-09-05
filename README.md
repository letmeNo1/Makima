Aki - Automated Testing on desktop
=================================
-   [English](#Background)
-   [中文版](#背景)

Background
==========

This is a desktop automated testing framework based on accessibility api. At the same time, with the help of the open source framework of Ctype, the purpose of calling the Mac and Windows system-level API is achieved.

install 
===============
pip install makima

Getting started
===============

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


Usage
==========

### launch app and initialize an UIElementRef by identifier(Mac) or window name(Windows)
 
 ***For Mac：*** pass


 ***For Windows：***  Caculator = initialize_app_ref_for_win("Caculator")

 ***Mouse event：***

UIElementRef object support click, double click, long click, hover，drag

e.g.  `Caculator.find_element_by_wait(acc_name = "Input phone number",0).click()` or `Caculator.find_element_by_wait(acc_name = "Input phone number",0).doubleClick()`

 ***Input Event：***

UIElementRef object support type and clear

e.g. `Caculator.find_element_by_wait(acc_name = "Input phone number",0).type("188888")` or `Caculator.find_element_by_wait(acc_name = "Input phone number",0).clear()`


### find elements
   
 ***For Mac：*** 
  pass
     
 ***For Windows：***
 
     '''
       support query:
            automation_id=automation id
            acc_description = acc description
            acc_name=acc name
            acc_role_name=role name
            acc_value=acc value
            class_name=class name
            control_type=control type
            full_description=full description

        '''

     Caculator.find_element_by_wait(self, timeout=5000, use_re=False, **query)
     
     timeout is not required,The default value is 5000
     
     use_re is not required,The default value is False, If the value is true, a regular expression match can be used
     e.g  Caculator.find_element_by_wait(acc_name=".*Start.*")
   
     query is required,You can use multiple query
     e.g Caculator.find_element_by_wait(acc_name="auto", class_name="UIItemsView")

    
### Operation

 Support Mouse events, Combination keyboard events
 
      //Simulate opening the Windows interface to search and press enter to start the program
      win_keyboard.send(win_keyboard.codes.LEFT_WIN)
      win_keyboard.copy_text(app_name)
      time.sleep(1)
      win_keyboard.send(win_keyboard.codes.CONTROL.modify(win_keyboard.codes.KEY_V), delay=1)
      time.sleep(1)
      win_keyboard.send(win_keyboard.codes.RETURN)



背景
==========

Makima是一个基于Accessibility Api实现的跨平台(Mac(pending)/Windows）桌面端自动化测试框架，借助开源框架Ctype实现了对系统底层Api的访问。

安装
===============
pip install makima


**对于 Mac**

pass

元素定位工具
===============
**对于 Mac**

Accessibility Inspector：Xcode -> 打开 Developer Tools

使用“Accessibility Inspector”可以查找到App对应的元素属性

**对于 Windows**

下载 [inspect.exe](https://github.com/letmeNo1/Aki-Tools/blob/main/inspect.exe)

使用“inspect.exe”可以查找到App对应的元素属性


使用
==========

### 启动应用程序并通过窗口名称获取到UI对象
 
 ***对于 Mac：*** pass


 ***对于 Windows：***  Caculator = initialize_app_ref_for_win("Caculator")

App 窗口本身就是一个 UIElementRef 对象，而每个元素也都是一个 UIElementRef 对象。你可以通过UIElementRef来调用各种查找或者是点击的方法

 ***鼠标事件：***

UIElementRef 对象支持单击、双击、长按、悬停

例如: `Caculator.find_element_by_wait(acc_name = "Input phone number",0).click()` or `Caculator.find_element_by_wait(acc_name = "Input phone number",0).doubleClick()`

 ***输入事件：***

UIElementRef 对象支持输入和清除

例如:  `Caculator.find_element_by_wait(acc_name = "Input phone number",0).type("188888")` 或 `Caculator.find_element_by_wait(acc_name = "Input phone number",0).clear()`

### 查找元素

 ***对于 Mac：*** 
  
    pass
     
 ***对于 Windows：***
     
     '''
       支持的查找方式:
            automation_id=automation id
            acc_description = acc description
            acc_name=acc name
            acc_role_name=role name
            acc_value=acc value
            class_name=class name
            control_type=control type
            full_description=full description
     '''

     Caculator.find_element_by_wait(self, timeout=5000, use_re=False, **query)
     
     timeout 是一个可选参数，默认值为5000，即5秒
     
     use_re 是一个可选参数，默认值为False，若传True则表示开启正则表达式匹配
     例如 Caculator.find_element_by_wait(acc_name=".*Start.*")
   
     query 是一个必备参数，可以同事使用多个query来进行查找
     
     例如 Caculator.find_element_by_wait(acc_name="auto", class_name="UIItemsView")

      `
    
### 通用操作

 支持鼠标事件、组合键盘事件
 
  //模拟打开Windows界面进行搜索并按回车键启动程序
  win_keyboard.send(win_keyboard.codes.LEFT_WIN)
  win_keyboard.copy_text(app_name)
  time.sleep(1)
  win_keyboard.send(win_keyboard.codes.CONTROL.modify(win_keyboard.codes.KEY_V), delay=1)
  time.sleep(1)
  win_keyboard.send(win_keyboard.codes.RETURN)













