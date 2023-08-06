<h1 id="lucia.ui">lucia.ui</h1>


<h1 id="lucia.ui.menu">lucia.ui.menu</h1>


<h2 id="lucia.ui.menu.Menu">Menu</h2>

```python
Menu(self, scroll_sound='', enter_sound='', open_sound='', border_sound='', music='')
```
audiogame virtual menu

This object functions as an audiogame menu, where up/down/enter can be used to interact and choose an option.
Sounds such as the movement sound, selection sound, etc may be specified.
This is an almost direct conversion of bgt's dynamic_menu class, though it contains some enhancements found in other extensions such as m_pro.

args:
    scroll_sound (str, optional): File name of the sound that will be played when the cursor moves within the menu because an arrow key was pressed.
    enter_sound (str, optional): File name of the sound that will be played when enter is pressed to choose an option.
    open_sound (str, optional): File name of the sound that will be played when the menu is presented to the user.
    border_sound (str, optional): File name of the sound played when you hit the edge of the menu when trying to move.
    music (str, optional): File name of the background music that will be played while this menu is running.

<h3 id="lucia.ui.menu.Menu.set_callback">set_callback</h3>

```python
Menu.set_callback(self, callback)
```
Sets the menus callback. The callback will be called every iteration of the loop.

args:
    callback (obj): The method to use as callback. This method should be either a module or a class and provide the necessary output functions, see lucia.output for an example.
raises:
    ValueError if callback is not callable

<h3 id="lucia.ui.menu.Menu.add_speech_method">add_speech_method</h3>

```python
Menu.add_speech_method(self, method, shouldInterrupt=True)
```
selects the speech method and interrupt flag

args:
    method (obj): The method to use. This method should be either a module or a class and provide the necessary output functions, see lucia.output for an example.
    shouldInterrupt (bool, optional): determines if this speech method should interrupt already existing speech when speaking something new. Default is True.

<h3 id="lucia.ui.menu.Menu.add_item_tts">add_item_tts</h3>

```python
Menu.add_item_tts(self, item, internal_name='')
```
adds a spoken item to the menu.

args:
    item (str): The text of the item to be added. This is the text you will here when you come across it in the menu.
    internal_name (str, optional): The internal name of this item. when you retrieve the selected item by name this will be returned. Defaults to the spoken text of the item.

<h3 id="lucia.ui.menu.Menu.run">run</h3>

```python
Menu.run(self, intro='select an option', interrupt=True)
```
presents this menu to the user.

This function blocks until the menu is closed, either by selecting an item or pressing escape.
Available controls are up/down arrows, enter, and escape. Wrapping is not supported.

args:
    intro (str, optional): The text that will be spoken when the menu is presented, this will occur at the same time as the open sound. Default is 'select an option'
    interrupt (bool, optional): Determines if speech is interrupted when it is queued to be spoken. For your sanity, this should always be True. Defaults to True.

returns:
    str if an option was selected, containing the option's internal name. -1 if escape was pressed.

<h2 id="lucia.ui.menu.YesNoMenu">YesNoMenu</h2>

```python
YesNoMenu(*args)
```
A yes/no menu

This simply takes a menu and initializes it with options of Yes and No, you would then have to call run and get the return.
The internal names of the items are lower case.

args:
args (tuple): Set of arguments to pass to Menu.__init__

<h1 id="lucia.ui.menu2">lucia.ui.menu2</h1>

advanced menu for advanced use

this menu module provides highly flexible menu items with different events and an advanced menu handling
<h2 id="lucia.ui.menu2.Menu">Menu</h2>

```python
Menu(self, items, clicksound='', edgesound='', wrapsound='', entersound='', opensound='', itempos=0, title='menu', fpscap=120, on_index_change=None, callback_function=None)
```

<h3 id="lucia.ui.menu2.Menu.run">run</h3>

```python
Menu.run(self)
```
when this function is called, menu loop starts. If the user make the menu return such as pressing enter on an item that has can_return attribute set to true the loop ends and it usually returns results as a list of dictionaries
<h1 id="lucia.ui.virtualinput">lucia.ui.virtualinput</h1>


