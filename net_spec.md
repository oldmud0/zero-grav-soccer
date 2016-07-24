## Network specification
**C** is client, **S** is server.

TODO: Unicode support.

Names are 16 characters padded with spaces.
Positions, velocities, and angles are little-endian floats.

### Process
 - Handshake
 - Game info
 - Join team
 - Send player data regularly

### Handshake
**Client**

C: `08 80` - magic number

C: Name

Server has choice to accept client or cut him off now.
If accepted, send Game info.

### Game info
**ID**: 1

**Server**

 - Blue team points (1 byte)
 - Red team points (1 byte)

### Player info
**ID**: 2

**Server**

 - Name (16 bytes)
 - Player ID (1 byte)
 - Team (1 byte)
 - Position X (4 bytes)
 - Position Y (4)
 - Velocity X (4)
 - Velocity Y (4)
 - Rotation (4)
 - Angular velocity (4)
 
### Player data (send)
**ID**: 3

**Client**

 - Position X (4 bytes)
 - Position Y (4)
 - Velocity X (4)
 - Velocity Y (4)
 - Rotation (4)
 - Angular velocity (4)
 - Input (1, low to high bits):
	Left
	Right
	Up
	Grab
	
### Player data (recv)
**ID**: 3

**Server**

 - Player ID (1 byte)
 - Position X (4 bytes)
 - Position Y (4)
 - Velocity X (4)
 - Velocity Y (4)
 - Rotation (4)
 - Angular velocity (4)
 - Input (1, low to high bits):
	Left
	Right
	Up
	Grab
	(If this is player, then ignore input)
	
### Join team
**ID**: 4

**Client/server**

Client sends packet to request team. Server will respond back with actual team.

 - Team (1 byte)

### Chat (send)
**ID**: 5

**Client**

 - Message (UTF-8, 256 characters, no padding)

### Chat (recv)
**ID**: 5

**Server**

 - Name
 - Message (UTF-8)

### Entity data
**ID**: 6

**Server** (has final say in game physics)

 - Position X (4 bytes)
 - Position Y (4)
 - Velocity X (4)
 - Velocity Y (4)
 - Rotation (4)
 - Angular velocity (4)