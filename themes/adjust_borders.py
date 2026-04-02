import os
import json
import random

def adjust_theme_borders(themes_dir):
    """
    Adjusts border-radius and pill-radius for theme files based on proportions.
    """
    all_json_files = [f for f in os.listdir(themes_dir) if f.endswith('.json')]
    
    theme_files = []
    for f_name in all_json_files:
        # Exclude specific non-theme JSON files if they exist
        if f_name not in ['package.json', 'default-theme.json', 'README.md']: # default-theme.json is often a base, let's not mess with it
             if f_name.endswith('-theme.json'): # Heuristic for themes I generated
                theme_files.append(f_name)
    
    random.shuffle(theme_files)
    
    num_themes = len(theme_files)
    num_pill = num_themes // 4
    num_slightly_rounded = num_themes // 4
    
    pill_themes = theme_files[:num_pill]
    slightly_rounded_themes = theme_files[num_pill : num_pill + num_slightly_rounded]
    sharp_themes = theme_files[num_pill + num_slightly_rounded:]

    print(f"Total theme files to adjust: {num_themes}")
    print(f"  Pill borders: {len(pill_themes)} themes")
    print(f"  Slightly rounded borders: {len(slightly_rounded_themes)} themes")
    print(f"  Sharp borders: {len(sharp_themes)} themes")

    changes_made = 0

    # Apply pill borders
    for f_name in pill_themes:
        file_path = os.path.join(themes_dir, f_name)
        try:
            with open(file_path, 'r+') as f:
                data = json.load(f)
                data["border-radius"] = "999px" # Effectively a pill shape for most elements
                data["pill-radius"] = "999px"   # For specific "pill" elements
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            changes_made += 1
        except Exception as e:
            print(f"Error processing {f_name}: {e}")

    # Apply slightly rounded borders
    for f_name in slightly_rounded_themes:
        file_path = os.path.join(themes_dir, f_name)
        try:
            with open(file_path, 'r+') as f:
                data = json.load(f)
                data["border-radius"] = "4px"
                data["pill-radius"] = "4px"
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            changes_made += 1
        except Exception as e:
            print(f"Error processing {f_name}: {e}")

    # Apply sharp borders
    for f_name in sharp_themes:
        file_path = os.path.join(themes_dir, f_name)
        try:
            with open(file_path, 'r+') as f:
                data = json.load(f)
                data["border-radius"] = "0px"
                data["pill-radius"] = "0px"
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            changes_made += 1
        except Exception as e:
            print(f"Error processing {f_name}: {e}")
            
    print(f"Finished adjusting borders. {changes_made} theme files modified.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    adjust_theme_borders(script_dir)
