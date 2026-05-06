import os
import re

# Files to update with their corresponding level numbers
files_to_update = {
    'kings-and-pigs-main/index.html': 2,
    'kings-and-pigs-main/index - Copy.html': 2,
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

def fix_video_path(file_path, level_number):
    """Fix video path in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the video source tag with relative path
        old_pattern = f'<source src="../level{level_number}_tutorial.mp4" type="video/mp4">'
        new_pattern = f'<source src="/tutorial/level{level_number}_tutorial.mp4" type="video/mp4">'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed: {file_path} -> /tutorial/level{level_number}_tutorial.mp4")
            return True
        else:
            # Check if already using server path
            if new_pattern in content:
                print(f"ℹ️  Already fixed: {file_path}")
                return True
            else:
                print(f"⚠️  Pattern not found in: {file_path}")
                return False
                
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    print("🔧 Fixing video paths to use server endpoint...")
    print("=" * 60)
    
    fixed_count = 0
    total_count = len(files_to_update)
    
    for file_path, level_number in files_to_update.items():
        if os.path.exists(file_path):
            if fix_video_path(file_path, level_number):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("=" * 60)
    print(f"✨ Complete! Fixed {fixed_count}/{total_count} files")
    print("\n📝 Summary:")
    print("   - All video paths now use: /tutorial/levelX_tutorial.mp4")
    print("   - Videos will be served through the Flask backend")
    print("   - This works when server is running at http://localhost:5000")
    print("\n🚀 Next steps:")
    print("   1. Run: python start_all_servers.py")
    print("   2. Open game in browser")
    print("   3. Click Tutorial button in any level")
    print("   4. Video should now play correctly!")

if __name__ == '__main__':
    main()
