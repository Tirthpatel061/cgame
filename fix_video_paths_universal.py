import os
import re

# Files to update with their corresponding level numbers
files_to_update = {
    'kings-and-pigs-main/index - Copy.html': 1,
    'kings-and-pigs-main/index3.html': 3,
    'kings-and-pigs-main/index4.html': 4,
    'kings-and-pigs-main/index5.html': 5,
    'kings-and-pigs-main/index6.html': 6,
    'kings-and-pigs-main/index7.html': 7,
    'kings-and-pigs-main/index8.html': 8,
    'kings-and-pigs-main/indexgame2.html': 2,
    'kings-and-pigs-main/indexgame3.html': 3,
    'kings-and-pigs-main/indexgame4.html': 4,
    'kings-and-pigs-main/indexgame5.html': 5,
    'kings-and-pigs-main/indexgame6.html': 6,
    'kings-and-pigs-main/indexgame7.html': 7,
    'kings-and-pigs-main/indexgame8.html': 8,
}

def fix_video_source_tag(content, level_number):
    """Add id to video source tag and set default relative path"""
    # Pattern to match video source tag (with or without id)
    patterns = [
        f'<source src="/tutorial/level{level_number}_tutorial.mp4" type="video/mp4">',
        f'<source src="../level{level_number}_tutorial.mp4" type="video/mp4">',
        f'<source id="videoSource" src="/tutorial/level{level_number}_tutorial.mp4" type="video/mp4">',
        f'<source id="videoSource" src="../level{level_number}_tutorial.mp4" type="video/mp4">',
    ]
    
    new_tag = f'<source id="videoSource" src="../level{level_number}_tutorial.mp4" type="video/mp4">'
    
    for pattern in patterns:
        if pattern in content:
            content = content.replace(pattern, new_tag)
            return content, True
    
    return content, False

def add_dynamic_path_detection(content, level_number):
    """Add dynamic path detection to showTutorialVideo function"""
    
    # Find the showTutorialVideo function
    function_pattern = r'function showTutorialVideo\(\) \{[^}]*videoModal\.classList\.add\(\'show\'\);'
    
    match = re.search(function_pattern, content, re.DOTALL)
    if not match:
        return content, False
    
    # Check if already has dynamic path detection
    if 'isServerMode' in content and 'videoSource.src' in content:
        return content, False  # Already fixed
    
    # New function with dynamic path detection
    new_function = f'''function showTutorialVideo() {{
            // Detect if running through server or directly
            const isServerMode = window.location.protocol === 'http:' && 
                                 (window.location.hostname === 'localhost' || 
                                  window.location.hostname === '127.0.0.1');
            
            // Set the correct video path based on mode
            const videoSource = document.getElementById('videoSource');
            if (isServerMode) {{
                // Running through server - use server endpoint
                videoSource.src = '/tutorial/level{level_number}_tutorial.mp4';
            }} else {{
                // Opening file directly - use relative path
                videoSource.src = '../level{level_number}_tutorial.mp4';
            }}
            
            // Show modal first
            videoModal.classList.add('show');'''
    
    # Replace the beginning of the function
    old_function_start = match.group(0)
    content = content.replace(old_function_start, new_function)
    
    return content, True

def fix_video_path(file_path, level_number):
    """Fix video path in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Step 1: Fix video source tag
        content, changed = fix_video_source_tag(content, level_number)
        if changed:
            modified = True
            print(f"  ✓ Updated video source tag")
        
        # Step 2: Add dynamic path detection
        content, changed = add_dynamic_path_detection(content, level_number)
        if changed:
            modified = True
            print(f"  ✓ Added dynamic path detection")
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"ℹ️  Already fixed: {file_path}")
            return True
                
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    print("🔧 Fixing video paths for UNIVERSAL compatibility...")
    print("   (Works both WITH and WITHOUT server)")
    print("=" * 60)
    
    fixed_count = 0
    total_count = len(files_to_update)
    
    for file_path, level_number in files_to_update.items():
        if os.path.exists(file_path):
            print(f"\n📝 Processing: {file_path}")
            if fix_video_path(file_path, level_number):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n" + "=" * 60)
    print(f"✨ Complete! Processed {fixed_count}/{total_count} files")
    print("\n📝 How it works:")
    print("   - Default path: ../levelX_tutorial.mp4 (relative)")
    print("   - JavaScript detects if running through server")
    print("   - If server detected: switches to /tutorial/levelX_tutorial.mp4")
    print("   - If file opened directly: uses ../levelX_tutorial.mp4")
    print("\n✅ Videos now work in BOTH scenarios:")
    print("   1. Opening HTML file directly from folder")
    print("   2. Running through server (python start_all_servers.py)")
    print("\n🚀 Test both ways:")
    print("   • Direct: Double-click indexgame1.html")
    print("   • Server: python start_all_servers.py")

if __name__ == '__main__':
    main()
