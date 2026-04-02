import os
import json
import random

def remove_pill_borders(themes_dir):
    all_json_files = [f for f in os.listdir(themes_dir) if f.endswith('.json')]
    
    theme_files = []
    for f_name in all_json_files:
        if f_name not in ['package.json', 'default-theme.json', 'README.md', 'generate_new_themes.py', 'adjust_borders.py', 'generate_previews.py', 'template.html', 'theme_previews.html']:
             if f_name.endswith('-theme.json'):
                theme_files.append(f_name)

    pill_themes = []
    for f_name in theme_files:
        file_path = os.path.join(themes_dir, f_name)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Check for "999px" for both border-radius and pill-radius
                if data.get("border-radius") == "999px" and data.get("pill-radius") == "999px":
                    pill_themes.append(f_name)
        except Exception as e:
            print(f"Error reading {f_name}: {e}")

    random.shuffle(pill_themes)
    num_to_modify = len(pill_themes) // 3

    modified_themes = pill_themes[:num_to_modify]
    
    print(f"Total pill themes found: {len(pill_themes)}")
    print(f"Themes to modify (no border): {len(modified_themes)}")

    changes_made = 0
    for f_name in modified_themes:
        file_path = os.path.join(themes_dir, f_name)
        try:
            with open(file_path, 'r+') as f:
                data = json.load(f)
                
                # Set border and btn-border to background color to make them invisible
                bg_color = data.get("bg", "#000000") # Get background color, default to black
                data["btn-border"] = bg_color
                data["border"] = bg_color
                
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            changes_made += 1
        except Exception as e:
            print(f"Error processing {f_name}: {e}")
            
    print(f"Finished adjusting borders. {changes_made} theme files modified to have no borders.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    remove_pill_borders(script_dir)
