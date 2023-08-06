<h1 id="lucia.utils">lucia.utils</h1>


<h1 id="lucia.utils.instance_checker">lucia.utils.instance_checker</h1>


<h2 id="lucia.utils.instance_checker.InstanceChecker">InstanceChecker</h2>

```python
InstanceChecker(self, f)
```
An instance checker

This is similar to bgt's instance object, to make sure a game can be running only once.

args:
    f (str): The name to be registered as a mutex.

<h3 id="lucia.utils.instance_checker.InstanceChecker.is_running">is_running</h3>

```python
InstanceChecker.is_running(self)
```
check if another instance is already running

returns:
    True if this instance is already registered, false otherwise.

<h1 id="lucia.utils.network">lucia.utils.network</h1>


<h1 id="lucia.utils.number_to_words">number_to_words</h1>

```python
number_to_words(number, include_and=False)
```
returns a string representation for the given number
<h1 id="lucia.utils.rotation">lucia.utils.rotation</h1>

Rotation class

This is modeled on the bgt rotation class from Sam Tupy. Input and output are in degrees.

<h2 id="lucia.utils.rotation.Vector">Vector</h2>

```python
Vector(self, x=0.0, y=0.0, z=0.0)
```
an object representing what bgt calls a vector

This represents a point in 3-space, where positive x is right, positive y is forward, and positive z is up.
The property coords can be used to get and set a tuple of the coordinates represented by this vector with no rounding applied.

args:
    x (float, optional): The starting x coordinate of this vector
    y (float, optional): The starting y coordinate of this vector
    z (float, optional): The starting z coordinate of this vector.

<h2 id="lucia.utils.rotation.move">move</h2>

```python
move(coords, deg, pitch=0.0, factor=1.0)
```
moves a vector in a given direction by a scale factor of factor

Takes a vector as input, applies the translation, and returns a vector as output. Probably best done as player.coords=move(player.coords,player.facing) or something similar.
The scale factor is used if you wish to move more than 1 coordinate, otherwise you simply apply the unit circle.

args:
  coords (tuple or list): The current point in 3-space you wish to move.
  deg (float): The current facing of an object
  pitch (float, optional): The vertical degrees you wish to move. Defaults to 0, no vertical movement.
  factor (float, optional): The scale factor you wish to move by. Passing 1 is equivalent to one unit move in any direction, but for warping in a particular direction you can pass a higher factor. Defaults to 1.

returns:
  a transformed vector

<h2 id="lucia.utils.rotation.calculate_angle">calculate_angle</h2>

```python
calculate_angle(x1, y1, x2, y2, deg)
```
given two points, returns the angle of the second one relative to the first.

This function is useful for reporting a direction of an object to a player, for example.
In this example the 'origin' point would be the player and the 'distant' point would be the object the player is tracking.

args:
  x1 (float): The x coordinate of the origin point.
  y1 (float): The y coordinate of the origin point.
  x2 (float): The x coordinate of the distant point
  y2 (float): The y coordinate of the distant point
  deg (float): The absolute direction the origin point is facing, for offsets.

returns:
  an angle (in degrees) of the distant point relative to the origin point, shifted by the orientation of the origin.

<h2 id="lucia.utils.rotation.get_1d_distance">get_1d_distance</h2>

```python
get_1d_distance(x1, x2)
```
returns the distance on a 1-dimensional plane from x1 to x2
<h2 id="lucia.utils.rotation.get_2d_distance">get_2d_distance</h2>

```python
get_2d_distance(x1, y1, x2, y2)
```
returns the pythagorean distance between two points on an x-y plane.
<h2 id="lucia.utils.rotation.get_3d_distance">get_3d_distance</h2>

```python
get_3d_distance(x1, y1, z1, x2, y2, z2)
```
returns the pythagorean distance between two points in 3-space.
<h1 id="lucia.utils.timer">lucia.utils.timer</h1>


<h2 id="lucia.utils.timer.Timer">Timer</h2>

```python
Timer(self)
```
A timer class, to track time mesured in millis

<h3 id="lucia.utils.timer.Timer.elapsed">elapsed</h3>

Returns the exact elapsed time since this timer was created or last restarted.

<h3 id="lucia.utils.timer.Timer.restart">restart</h3>

```python
Timer.restart(self)
```
Restarts the timer, and set it's elapsed time to 0.

<h3 id="lucia.utils.timer.Timer.pause">pause</h3>

```python
Timer.pause(self)
```
Pauses the timer at a certain position.
<h3 id="lucia.utils.timer.Timer.resume">resume</h3>

```python
Timer.resume(self)
```
Resumes the timer after being paused.
