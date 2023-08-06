<h1 id="lucia">lucia</h1>

The main Lucia module

The functions here are responsible for initializing and quitting lucia, showing the game window, handle global events and so on.
In addition, this part of lucia also contains most keyboard functions.

<h2 id="lucia.AudioBackend">AudioBackend</h2>

```python
AudioBackend(self, /, *args, **kwargs)
```

<h3 id="lucia.AudioBackend.BASS">BASS</h3>

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
<h3 id="lucia.AudioBackend.FMOD">FMOD</h3>

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
<h3 id="lucia.AudioBackend.OPENAL">OPENAL</h3>

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
<h2 id="lucia.initialize">initialize</h2>

```python
initialize(audiobackend=1)
```
Initialize lucia and the underlying graphic, audio, keyboard, interface engines
<h2 id="lucia.quit">quit</h2>

```python
quit()
```
Shutdown lucia and close underlying engines freeing up system resources
<h2 id="lucia.show_window">show_window</h2>

```python
show_window(title='LuciaGame', size=(640, 480))
```
Shows the main game window on the screen, this is most likely called at the start of a game
<h2 id="lucia.process_events">process_events</h2>

```python
process_events()
```
This processes events for the window
This should be called in any loop, to insure that the window and application stays responsive
<h2 id="lucia.key_pressed">key_pressed</h2>

```python
key_pressed(key_code)
```
Checks if a key was pressed down this frame (single key press)
* key_code: A pygame.K_ key code

returns: True if the specified key kode was pressed, False otherwise.

<h2 id="lucia.key_released">key_released</h2>

```python
key_released(key_code)
```
Checks if a key was released down this frame (single key release)
* key_code: A pygame.K_ key code

returns: True if the specified key kode was released, False otherwise.

<h2 id="lucia.key_down">key_down</h2>

```python
key_down(key_code)
```
Checks if a key is beeing held down.
* key_code: A pygame.K_ key code

returns: True if the specified key kode is beeing held down, False otherwise.

<h2 id="lucia.key_up">key_up</h2>

```python
key_up(key_code)
```
Check if a key isn't beeing held down (ie if it's not pressed and held)
* key_code : A pygame.K_ key code

returns: True if key is not held down, False otherwise

<h1 id="lucia.data">lucia.data</h1>

Provides functions for easily manipulating textual or binary data.
Currently includes encryption and compression.

<h2 id="lucia.data.unsupportedAlgorithm">unsupportedAlgorithm</h2>

```python
unsupportedAlgorithm(self, /, *args, **kwargs)
```
raised when the user tries supplying an algorithm not specified in constants
<h1 id="lucia.output">output</h1>

An output which automatically selects the first available output on the system
<h2 id="lucia.output.outputs">outputs</h2>

Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
<h1 id="lucia.packfile">lucia.packfile</h1>

Lucia's resource pack module

This module will aid in the interaction with and creation of data files for storing game assets.
A lucia resource file is a binary file format with the ability to have encryption and/or compression instituted on a per-file basis at creation time. Using the get method one may retrieve the contents of any file added to the pack, for example to be used in a memory load function of a sound system.

<h2 id="lucia.packfile.InvalidPackHeader">InvalidPackHeader</h2>

```python
InvalidPackHeader(self, /, *args, **kwargs)
```
raised when the packs header is invalid
<h2 id="lucia.packfile.ResourceFileVersion">ResourceFileVersion</h2>

```python
ResourceFileVersion(self, /, *args, **kwargs)
```
The version should only change if changes are introduced that breaks backwards compatibility
<h3 id="lucia.packfile.ResourceFileVersion.v1">v1</h3>

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
<h2 id="lucia.packfile.LoadPolicy">LoadPolicy</h2>

```python
LoadPolicy(self, /, *args, **kwargs)
```
The load policy used when loading in data from a resource file

LOAD_ALL loads everything into ram.
LOAD_INDEX only load in the filenames and where they are located on disk.

<h3 id="lucia.packfile.LoadPolicy.LOAD_ALL">LOAD_ALL</h3>

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
<h3 id="lucia.packfile.LoadPolicy.LOAD_INDEX">LOAD_INDEX</h3>

int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
<h2 id="lucia.packfile.ResourceFileItem">ResourceFileItem</h2>

```python
ResourceFileItem(self, name, content, compress, encrypt)
```
Internal object representing an item in the pack.
<h2 id="lucia.packfile.ResourceFile">ResourceFile</h2>

```python
ResourceFile(self, key, header=b'LURF', version=1)
```
The resource file object

You will interact with resource files through methods provided by this object. This object may have any number of instances, however only one instance should interact with a given file on the file system at a time.

<h3 id="lucia.packfile.ResourceFile.load">load</h3>

```python
ResourceFile.load(self, filename, policy=1)
```
Opens a resource file to be read.

This file will be checked for validity based on matching header, version, and a non-0 number of files. If one of these conditions fails, InvalidPackHeader will be raised. Otherwise this object will be loaded with the contents.
    :param filename: The file name to be read from the file system.
    :param policy (optional): The load policy to use, defaults to LoadPolicy.LOAD_ALL

<h3 id="lucia.packfile.ResourceFile.save">save</h3>

```python
ResourceFile.save(self, filename)
```
Saves data added to this object to a resource file.

When creating a resource file, this is the final method you would call.
args:
    :param filename: The file name on disk to write to. Will be overwritten if already exists.

<h3 id="lucia.packfile.ResourceFile.add_file">add_file</h3>

```python
ResourceFile.add_file(self, name, compress=True, encrypt=True, internalname=None)
```
Adds a file on disk to the pack, optionally compressing and/or encrypting it.

args:
    :param name: The file name to read from.
    :param compress (boolean, optional): Whether compression should be applied to this file. Defaults to True.
    :param encrypt (boolean, optional): Whether encryption should be applied to this file. Defaults to True.
    :param internalname (optional): Internal file name to be used inside the pack. If None, the default, internal name will be same as name on disk.

<h3 id="lucia.packfile.ResourceFile.get">get</h3>

```python
ResourceFile.get(self, name)
```
[summary]

Args:
 name ([str]): The key to lookup in the data file

Returns:
 bytes or none: Returns the found result, or none if nothing with the specified key was found.

