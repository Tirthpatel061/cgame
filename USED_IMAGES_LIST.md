# Actually Used Images in kings-and-pigs-main

Based on code analysis, here are the images that are actually referenced and used:

## img/ folder - REQUIRED IMAGES:

### King Character Sprites (img/king/)
- `img/king/idle.png` - King idle animation
- `img/king/idleLeft.png` - King idle left animation
- `img/king/runRight.png` - King running right
- `img/king/runLeft.png` - King running left (note: code uses runLeft.png but file is runleft.png)
- `img/king/enterDoor.png` - King entering door animation

### Background Images
- `img/backgroundLevel1.png` - Level 1 background
- `img/backgroundLevel2.png` - Level 2 background
- `img/backgroundLevel3.png` - Level 3 background

### Door Sprites
- `img/doorOpen.png` - Door opening animation (used in multiple levels)

### Character Images (for indexgame files)
- `img/Character_1.png` - Default standing character
- `img/Character_2.png` - Alternative character (if used)

### Animation Frames (for indexgame1-8.html)
**NOTE: These files appear to be MISSING but are referenced in code:**
- `img/frame_1_1.png` to `img/frame_1_5.png` - Frame 1 animations (5 images)
- `img/frame_2_1.png` to `img/frame_2_5.png` - Frame 2 animations (5 images)

**If these don't exist, the indexgame files may not work properly!**

### Other Referenced Images
- `img/box.png` - Box sprite (if used)
- `img/fire_1.png` - Fire animation frame 1 (if used)
- `img/fire_2.png` - Fire animation frame 2 (if used)

---

## img2/ folder - REQUIRED IMAGES:

### img2/samuraiMack/ - Samurai Character
- `img2/samuraiMack/background.png` - Background for samurai level
- `img2/samuraiMack/shop.png` - Shop sprite
- `img2/samuraiMack/Idle.png` - Idle animation
- `img2/samuraiMack/Run.png` - Running animation
- `img2/samuraiMack/Jump.png` - Jump animation
- `img2/samuraiMack/Fall.png` - Fall animation
- `img2/samuraiMack/Attack1.png` - Attack animation
- `img2/samuraiMack/Take Hit - white silhouette.png` - Take hit animation
- `img2/samuraiMack/Death.png` - Death animation

### img2/kenji/ - Kenji Character
- `img2/kenji/Idle.png` - Idle animation
- `img2/kenji/Run.png` - Running animation
- `img2/kenji/Jump.png` - Jump animation
- `img2/kenji/Fall.png` - Fall animation
- `img2/kenji/Attack1.png` - Attack animation
- `img2/kenji/Take hit.png` - Take hit animation
- `img2/kenji/Death.png` - Death animation

---

## img/ folder - OPTIONAL/UNUSED IMAGES (can be removed):

These files exist but are NOT referenced in the code:
- `img/Attack1 - Copy.png`
- `img/Attack1.png`
- `img/Attack2.png`
- `img/backgroundImage.png`
- `img/backgroundImage10.png`
- `img/backgroundLevel100.png`
- `img/backgroundLevel10000.png`
- `img/backgroundLevel13.png`
- `img/backgroundLevel3-original.png`
- `img/backgroundLevel30.png`
- `img/backgroundLevel3000.png`
- `img/backgroundLevel4.jpg`
- `img/backgroundLevel8.png`
- `img/d56he85-4941e7f4-9e06-4c99-83cd-715b33d854ae.png`
- `img/Death.png`
- `img/doorOpen (2).png`
- `img/doorOpen1.png`
- `img/doorOpen10.png`
- `img/Frame 4.png`
- `img/help-paper2d-pixel-art-blurred-after-packaging-for-windows-v0-gSQbs4FVP_ud0K8X9Qb1QmNkkU8TrByT-f4E6ok7cVs.webp`
- `img/king/runleft.png` (duplicate, lowercase)
- `img/king/runleft1.png`
- `img/king/runRight1.png`

---

## img2/ folder - OPTIONAL/UNUSED IMAGES (can be removed):

These files exist but are NOT referenced in the code:
- `img2/kenji/Attack2.png`
- `img2/samuraiMack/Attack2.png`
- `img2/samuraiMack/Take Hit.png` (code uses "Take Hit - white silhouette.png")

---

## login.html Video File:

- `img/among_us_background.mp4` - Background video for login page
  **NOTE: This file may be missing! Check if it exists.**

---

## MINIMAL IMAGE SET FOR DEPLOYMENT:

If you want to minimize file size, keep ONLY these:

### img/king/ (all 5 files)
- idle.png
- idleLeft.png
- runRight.png
- runLeft.png (rename runleft.png to runLeft.png if needed)
- enterDoor.png

### img/ (root level)
- backgroundLevel1.png
- backgroundLevel2.png
- backgroundLevel3.png
- doorOpen.png
- Character_1.png
- Character_2.png (if used)

### img/ (animation frames - CREATE THESE if missing)
- frame_1_1.png to frame_1_5.png
- frame_2_1.png to frame_2_5.png

### img2/samuraiMack/ (all 9 files)
- background.png
- shop.png
- Idle.png
- Run.png
- Jump.png
- Fall.png
- Attack1.png
- Take Hit - white silhouette.png
- Death.png

### img2/kenji/ (all 7 files)
- Idle.png
- Run.png
- Jump.png
- Fall.png
- Attack1.png
- Take hit.png
- Death.png

---

## IMPORTANT NOTES:

1. **Missing Files**: The frame_1_*.png and frame_2_*.png files are referenced but don't exist. You need to create or find these files, or the indexgame1-8.html files won't work.

2. **Case Sensitivity**: Some file names have case mismatches (runLeft.png vs runleft.png). Make sure file names match exactly.

3. **Video File**: Check if `img/among_us_background.mp4` exists for the login page.

4. **Total Required Images**: 
   - img/king/: 5 files
   - img/ root: 4-6 files + 10 frame files
   - img2/samuraiMack/: 9 files
   - img2/kenji/: 7 files
   - **Total: ~35-37 image files minimum**

5. **js/ and js2/ folders**: These contain JavaScript libraries, not images. Keep all JS files as they are likely dependencies.

6. **src/ folder**: This contains source code files, not images. Keep all files in this folder.
