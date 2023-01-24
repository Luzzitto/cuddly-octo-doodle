# cuddly-octo-doodle

# Labeling

## Media
The SD Cards ("media") will contain the box letters, media location, and type.
### Box Letters
`Box Letters` contain the box name.
### Media Location
Media Location is simply coordinates of media into the box. For example, a box can contain **21 SD Card slots + 15 micro sd**. 
The 21 SD Card slots are *3 x 5*. The "3" represents the `x-coordiante` and "5" the `y-coordinate`. For example,
camera's sd card would fall in `A` section with number corresponding to the location (from top to bottom). Additionally,
a `+` (plus) or `-` (minus) would be added in between box letter and coordinate to determine the 3rd axis of location. `+` being the top section of the box and `-` the bottom.

### Example
* `MAIN-A2`
  * Corresponds to `MAIN` box with the location in section `A` and `2` column.
* `MAIN+D3`
  * At the top of `MAIN` box with section `D` and column `3`

## Hard Drive
Labeling Hard Drives are the easiests because they can be named with the owner name. For example, a main drive can be `Luzzitto` or a backup of main `Luzzitto-duplicate`. Until further notice, hard drives are addressed to the owner.

# Usage
## Register
### Media
Media/SD Card needs to be labeled before registering.

### Hard Drive

# Todo
* Label SD Card
* Register SD Card
* Upload Image Files
* Python files
  * `init.py` - Initialize folders and database information
  * `register.py` - Register media and add it to the list
  * `folder.py` - Get files information on certain folder
  * `verify.py` - Verify the copy to the original
