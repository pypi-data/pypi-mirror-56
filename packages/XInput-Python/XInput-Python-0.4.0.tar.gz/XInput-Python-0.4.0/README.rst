
##############
XInput\-Python
##############

********************************************************
A simple to use interface to the XInput API for Python\.
********************************************************
| **XInput\-Python** provides a few simple methods that can be used to query controller information\.
| 

Tiny Documentation
==================
| *XInput is Windows only*

Installation
------------
| XInput\-Python is available from the `PyPI <https://pypi.org>`_ using


::

    pip install XInput-Python

 
| It can be inmported like this\:


::

    import XInput

 

Using XInput\-Python
--------------------
| XInput\-Python provides a few functions\:
| :code:`get_connected() -> (bool, bool, bool, bool)` Query which controllers are connected \(note\: don\'t query each frame\)
| 
| :code:`get_state(user_index) -> State` Gets the State of the controller :code:`user_index`
| 
| :code:`get_button_values(state) -> dict` Returns a dictionary\, showing which buttons are currently being pressed\.
| 
| :code:`get_trigger_values(state) -> (LT, RT)` Returns a tuple with the values of the left and right triggers in range :code:`0.0` to :code:`1.0`
| 
| :code:`get_thumb_values(state) -> ((LX, LY), (RX, RY))` Returns the values of the thumb sticks\, expressed in X and Y ranging from :code:`0.0` to :code:`1.0`
| 
| :code:`set_vibration(user_index, left_speed, right_speed) -> bool (Success)` Sets the vibration of the left and right motors of :code:`user_index` to values between :code:`0` and :code:`65535` or in range :code:`0.0` to :code:`1.0` respectively\.
| 
| :code:`get_battery_information(user_index) -> (<type>, <level>)` Returns the battery information for :code:`user_index`
| 
| :code:`set_deadzone(deadzone, value) -> None` Sets the deadzone values for left\/right thumb stick and triggers\.
| 
| The following deadzones exist\:
| :code:`XInput.DEADZONE_LEFT_THUMB` \- \(range 0 to 32767\) Left thumb stick deadzone \(default is 7849\)
| 
| :code:`XInput.DEADZONE_RIGHT_THUMB` \- \(range 0 to 32767\) Right thumb stick deadzone \(default is 8689\)
| 
| :code:`XInput.DEADZONE_TRIGGER` \- \(range 0 to 255\) Trigger deadzone \(default is 30\)
| 

Using Events
^^^^^^^^^^^^
| You can also use the Event\-system\:


::

    events = get_events()

 
| 
| :code:`get_events` will return a generator that yields instances of the :code:`Event` class\.
| 
| The :code:`Event` class always has the following members\:
| :code:`Event.user_index` \(range 0 to 3\) \- the id of the controller that issued this event
| :code:`Event.type` \- which type of event was issued
| 
| The following events exist\:
| :code:`XInput.EVENT_CONNECTED == 1` \- a controller with this :code:`user_index` was connected \(this event will even occur if the controller was connected before the script was started\)
| 
| :code:`XInput.EVENT_DISCONNECTED == 2` \- a controller with this :code:`user_index` was disconnected
| 
| :code:`XInput.EVENT_BUTTON_PRESSED == 3` \- a button was pressed on the controller :code:`user_index`
| 
| :code:`XInput.EVENT_BUTTON_RELEASED == 4` \- a button was released on the controller :code:`user_index`
| 
| :code:`XInput.EVENT_TRIGGER_MOVED == 5` \- a trigger was moved on the controller :code:`user_index`
| 
| :code:`XInput.EVENT_STICK_MOVED == 6` \- a thumb stick was moved on the controller :code:`user_index`
| 
| **Button Events**
| All button related Events have the following additional members\:
| :code:`Event.button_id` \- the XInput numerical representation of the button
| :code:`Event.button` \- a literal representation of the button
| 
| The following buttons exist\:


::

    "DPAD_UP" == 1
    "DPAD_DOWN" == 2
    "DPAD_LEFT" == 4
    "DPAD_RIGHT" == 8
    "START" == 16
    "BACK" == 32
    "LEFT_THUMB" == 64
    "RIGHT_THUMB" == 128
    "LEFT_SHOULDER" == 256
    "RIGHT_SHOULDER" == 512
    "A" == 4096
    "B" == 8192
    "X" == 16384
    "Y" == 32768
    

 
| 
| **Trigger Events**
| All trigger related Events have the following additional members\:
| :code:`Event.trigger` \(either :code:`XInput.LEFT == 0` or :code:`XInput.RIGHT == 1`\) \- which trigger was moved
| :code:`Event.value` \(range 0\.0 to 1\.0\) \- by how much the trigger is currently pressed
| 
| **Stick Events**
| All thumb stick related Events have the following additional members\:
| :code:`Event.stick` \(either :code:`XInput.LEFT == 0` or :code:`XInput.RIGHT == 1`\) \- which stick was moved
| :code:`Event.x` \(range \-1\.0 to 1\.0\) \- the position of the stick on the X axis
| :code:`Event.y` \(range \-1\.0 to 1\.0\) \- the position of the stick on the Y axis
| :code:`Event.value` \(range 0\.0 to 1\.0\) \- the distance of the stick from it\'s center position
| :code:`Event.dir` \(tuple of X and Y\) \- the direction the stick is currently pointing
| 

Callback events and threading
-----------------------------
| With the :code:`GamepadThread` class it is possible to handle asynchronous events\.
| To use this feature\, extend the :code:`EventHandler` to create one or multiple handlers and add them to the thread\.
| The library will automatically check the status of the gamepad and use the appropriate callback for the triggering event\.
| It is also possible to filter the inputs for every single handler\.
| In case of multiple handlers it is possible to use a list of handlers as argument\, as well as the :code:`add_handler()` method and the :code:`remove_handler()` method to remove them\.
| Filters can be applied to select events of only certain buttons\, trigger or stick\. Also a \"pressed\-only\" and \"released\-only\" filter is available for buttons\.
| The available filters are\:


::

    
    BUTTON_DPAD_UP       
    BUTTON_DPAD_DOWN     
    BUTTON_DPAD_LEFT     
    BUTTON_DPAD_RIGHT    
    BUTTON_START         
    BUTTON_BACK          
    BUTTON_LEFT_THUMB    
    BUTTON_RIGHT_THUMB   
    BUTTON_LEFT_SHOULDER 
    BUTTON_RIGHT_SHOULDER
    BUTTON_A             
    BUTTON_B             
    BUTTON_X             
    BUTTON_Y             
    
    STICK_LEFT           
    STICK_RIGHT          
    TRIGGER_LEFT         
    TRIGGER_RIGHT        
    
    FILTER_PRESSED_ONLY     
    FILTER_RELEASED_ONLY
    

      
| 
| The filters can be combined by adding them together\:
| 


::

    filter1 = STICK_LEFT + STICK_RIGHT + BUTTON_DPAD_DOWN + BUTTON_DPAD_UP
    filter2 = BUTTON_Y + BUTTON_X + FILTER_PRESSED_ONLY

 
| 
| The filter can be applied using add\_filter\:
| 


::

    handler.add_filter(filter)

 
| 
| **Example**


::

    class MyHandler(EventHandler):
        def process_button_event(self, event):
            # put here the code to parse every event related only to the buttons
    
        def process_trigger_event(self, event):
            # event reserved for the two triggers
    
        def process_stick_event(self, event):
            # event reserved for the two sticks
    
        def process_connection_event(self, event):
            # event related to the gamepad status
    
    filter = STICK_LEFT + STICK_RIGHT
    my_handler = MyHandler()
    my_handler.add_filter(filter)
    my_gamepad_thread = GamepadThread(my_handler)

 
| 
| The thread will start automatically upon creation\. It is possible to stop and start it again if necessary with the two methods :code:`start()` and :code:`stop()`
| 

Demo
----
| Run :code:`XInputTest.py` to see a visual representation of the controller input\.
| Run :code:`XInputThreadTest.py` to test the visual representation using the asynchronous callbacks\.