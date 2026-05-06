# Required JavaScript Files for Game

## Summary
This document lists all JavaScript files needed for the game to function properly.

## Files Currently Used in Game

### From `js/` Folder (Main Game Files)

#### Core Files (Required for all levels)
1. **`js/utils.js`** ✅ REQUIRED
   - Utility functions for game mechanics
   - Used by: All exploration levels (index.html, index3-8.html)

2. **`js/eventListeners.js`** ✅ REQUIRED
   - Handles keyboard input and door interactions
   - Manages tutorial video triggers
   - Used by: All exploration levels

#### Data Files
3. **`js/data/collisions.js`** ✅ REQUIRED
   - Contains collision map data for levels
   - Defines where player can/cannot walk
   - Used by: All exploration levels

#### Class Files (Game Objects)
4. **`js/classes/CollisionBlock.js`** ✅ REQUIRED
   - Defines collision blocks for walls/obstacles
   - Used by: All exploration levels

5. **`js/classes/Sprite.js`** ✅ REQUIRED
   - Base sprite class for animated objects
   - Used by: All exploration levels

6. **`js/classes/Player.js`** ✅ REQUIRED
   - Main player character class
   - Handles player movement and animations
   - Used by: All exploration levels

7. **`js/classes/player2.js`** ⚠️ POSSIBLY UNUSED
   - Secondary player class (may be for multiplayer)
   - Loaded but might not be actively used
   - Used by: All exploration levels (loaded but check if needed)

8. **`js/classes/classes.js`** ✅ REQUIRED
   - Additional game classes (doors, objects, etc.)
   - Used by: All exploration levels

### From `js2/` Folder (Alternative/Shooting Game)

1. **`js2/utils.js`** ⚠️ ONLY FOR SHOOTING GAME
   - Utility functions for shooting game variant
   - Used by: `indexshoot.html` only

2. **`js2/classes.js`** ⚠️ ONLY FOR SHOOTING GAME
   - Classes for shooting game mechanics
   - Used by: `indexshoot.html` only

3. **`js2/classses.js`** ❌ TYPO/UNUSED
   - Note the typo: "classses" instead of "classes"
   - Referenced in index files but file doesn't exist
   - This is likely a mistake and should be removed

## Files Loaded by Each Page Type

### Exploration Levels (index.html, index3-8.html)
```html
<script src="js/utils.js"></script>
<script src="js/data/collisions.js"></script>
<script src="js/classes/CollisionBlock.js"></script>
<script src="js/classes/Sprite.js"></script>
<script src="js/classes/Player.js"></script>
<script src="js/classes/player2.js"></script>
<script src="js/classes/classes.js"></script>
<script src="js/eventListeners.js"></script>
<script src="index.js"></script> <!-- or index3.js, index4.js, etc. -->
<script src="js2/classses.js"></script> <!-- ❌ TYPO - Should be removed -->
```

### Shooting Game (indexshoot.html)
```html
<script src="js2/utils.js"></script>
<script src="js2/classes.js"></script>
<script src="indexshoot.js"></script>
```

## Recommendations

### ✅ Keep These Files (Essential)
From `js/` folder:
- `js/utils.js`
- `js/eventListeners.js`
- `js/data/collisions.js`
- `js/classes/CollisionBlock.js`
- `js/classes/Sprite.js`
- `js/classes/Player.js`
- `js/classes/classes.js`

### ⚠️ Review These Files
- **`js/classes/player2.js`** - Check if actually used for multiplayer or can be removed
- **`js2/utils.js`** - Only needed if shooting game is used
- **`js2/classes.js`** - Only needed if shooting game is used

### ❌ Remove/Fix These
- **`js2/classses.js`** reference in HTML files - This is a typo and should be removed from all HTML files

## File Structure

```
kings-and-pigs-main/
├── js/                          # Main game files
│   ├── utils.js                 ✅ REQUIRED
│   ├── eventListeners.js        ✅ REQUIRED
│   ├── data/
│   │   └── collisions.js        ✅ REQUIRED
│   └── classes/
│       ├── CollisionBlock.js    ✅ REQUIRED
│       ├── Sprite.js            ✅ REQUIRED
│       ├── Player.js            ✅ REQUIRED
│       ├── player2.js           ⚠️ REVIEW
│       └── classes.js           ✅ REQUIRED
│
├── js2/                         # Shooting game variant
│   ├── utils.js                 ⚠️ ONLY IF USING SHOOTING GAME
│   └── classes.js               ⚠️ ONLY IF USING SHOOTING GAME
│
├── index.js                     ✅ Level 1 logic
├── index2.js                    ✅ Level 2 logic
├── index3.js                    ✅ Level 3 logic
├── index4.js                    ✅ Level 4 logic
├── index5.js                    ✅ Level 5 logic
├── index6.js                    ✅ Level 6 logic
├── index7.js                    ✅ Level 7 logic
├── index8.js                    ✅ Level 8 logic
└── indexshoot.js                ⚠️ ONLY IF USING SHOOTING GAME
```

## Action Items

1. **Remove typo reference** - Remove `<script src="js2/classses.js"></script>` from all HTML files
2. **Check player2.js usage** - Verify if this file is actually needed
3. **Clean up js2 folder** - If shooting game is not used, consider removing js2 folder entirely
4. **Document file purposes** - Add comments to each JS file explaining its purpose

## Minimal Required Files for Main Game

If you want to run just the main exploration/challenge game, you need:

**From js/ folder (8 files):**
1. `js/utils.js`
2. `js/eventListeners.js`
3. `js/data/collisions.js`
4. `js/classes/CollisionBlock.js`
5. `js/classes/Sprite.js`
6. `js/classes/Player.js`
7. `js/classes/classes.js`
8. `js/classes/player2.js` (if used)

**Root level (8 files):**
1. `index.js` (Level 1)
2. `index2.js` (Level 2)
3. `index3.js` (Level 3)
4. `index4.js` (Level 4)
5. `index5.js` (Level 5)
6. `index6.js` (Level 6)
7. `index7.js` (Level 7)
8. `index8.js` (Level 8)

**Total: 16 files minimum**

## js2 Folder Purpose

The `js2/` folder appears to be for a different game variant (shooting game) that uses:
- Different game mechanics
- Different class structure
- Only used by `indexshoot.html`

**Recommendation:** If you're not using the shooting game, you can safely ignore or remove the js2 folder.
