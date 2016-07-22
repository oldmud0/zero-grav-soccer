# Soccer in space!

Playing the game
----------------

To run the game, execute main.py with Python 3. This will require Pygame to be installed.

Use the directional arrow keys (up, left, and right) or W, A, and D to turn and propel the ship.

Press Escape to close the game.

Press R to restart.

Overview
========

The main premise of zero gravity soccer, like ordinary soccer, is 
bringing the objective (the ball) to the goal on the other team's side. 
However, because it is in zero gravity, the laws of physics apply at a 
far greater scale than normal. There are no free kicks; opposing ships 
can ram each other for a strategic advantage; and a federation-approved 
field is surrounded with guardrails to allow ships to bounce off the 
edges with minimal loss of kinetic energy.

The blue and red teams, each consisting of 3 players, take opposite 
sides of the field. A player can grab the ball for up to three seconds, 
after which the player must throw it (with a minor recoil based on the 
ball's mass) or simply lose control of it. If the player collides 
against another from the opposing team, the player automatically loses 
exclusive control of the ball.

Once a team brings the ball to the goal, all players respawn at their 
initial positions at the middle of the field to begin another round. The 
game ends when a team has two points more than the other team.

Features
========

This project will never truly be “finished.” Game creation is an 
extensive process that entails substantial work, at least dozens of 
man-hours, and, often times, a team. However, for the sake of deadlines 
and grades, this final project includes the bare minimum number of 
features that allow the game to be playable.

Physics engine
--------------

The game includes a rudimentary physics engine that handles 
entity-entity elastic collisions based on mass and velocity. All 
collisions are calculated pixel-by-pixel rather than by hitbox (the 
rectangle representing the boundaries of an entity).

TODO: Modify angular velocity based on collision point's distance from 
the center of mass (assume at center of sprite).

Entity-wall collisions are handled with a simple collision detector 
which checks which sides of the wall are filled (up, down, left, or 
right) about 15 pixels from the point of the collision, and determines 
the angle of the wall in 45-degree increments based on this information. 
The change in velocity as a result of the collision can be calculated 
very easily simply by negating one or both components of the velocity 
vector, since there are only eight scenarios the algorithm can detect.

Camera
------

To track the entity being controlled (i.e. the player’s ship), a 
camera applies an offset to all entities while respecting the boundaries 
of the map in order to keep this controlled entity in the center while 
preventing anything beyond the boundaries of the level to be shown (as 
this is undefined behavior, although in the future a sort of parallax 
effect could be added in the background, which would actually provide an 
incentive to include one).

Heads-up display
----------------

A heads-up display assists the player in understanding what is happening 
in the game. It includes an arrow at the edge of the screen to point at 
the objective (the ball) when it is off screen, as well as a subtle 
indicator to identify teammates.

Future/to-do
============

As explained previously, making games is serious business, so obviously 
it would take a substantial amount of additional time to make the game 
not just playable, but also enjoyable.

Artificial intelligence
-----------------------

An AI is ideal for playing alone or when there are not enough players 
for balanced teams. A simple AI could maneuver itself toward the ball 
and try to bunt it towards the enemy goal.

Networking
----------

Although originally in my list of planned features to complete before 
the project deadline, it simply cannot be realized within that 
timeframe. Networking requires tightly synchronized communication 
between a server and its clients, and a simple peer-to-peer model can be 
difficult to tweak. Even then, if every player was trusted with their 
own ship’s position information, it would be extremely easy to cheat 
in the game. Motion prediction/extrapolation code might also be required 
if latency is too high.

Art, sprites, and music
-----------------------

Digital art is not my forte. 

3-second invincibility
----------------------

Upon (re)spawning, ships should be invincible for three seconds to 
prevent any unfair advantage gained from teleportation or from 
obstructing the flow of the game.

Local multiplayer
-----------------

Just a simple splitscreen functionality could be made by dividing a 
window into two surfaces. However, this would have to be a tradeoff 
between network multiplayer and splitscreen. It's not certain whether 
both could be done simultaneously (the answer leans to "yes").
