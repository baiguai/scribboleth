import os
import json

def create_theme_preview_grid(themes_dir, output_file):
    """
    Generates an HTML file with a grid of theme previews.
    """
    theme_files = [f for f in os.listdir(themes_dir) if f.endswith('.json')]
    
    previews_html = ""
    for theme_file in sorted(theme_files):
        theme_name = os.path.splitext(theme_file)[0]
        try:
            with open(os.path.join(themes_dir, theme_file), 'r') as f:
                theme_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print("Skipping " + theme_file + ": " + str(e))
            continue

        css_variables = ""
        for key, value in theme_data.items():
            css_variables += "    --{key}: {value};\n".format(key=key, value=value)

        previews_html += '''
        <div class="theme-preview-container">
            <h3>{theme_name}</h3>
            <div class="theme-preview" style="--bg: {bg}; --fg: {fg};">
                <div class="preview-content" style="{css_variables}">
                    <div class="app">
                        <header>
                            <span class="dot green"></span>
                            <span class="dot red"></span>
                            <span class="kbd-hint">/</span>
                        </header>
                        <aside class="tree">
                            <ul>
                                <li>
                                    <div class="node selected">
                                        <span class="twisty">▼</span>
                                        <span class="icon">📁</span>
                                        <span class="title">notes</span>
                                    </div>
                                    <ul>
                                        <li>
                                            <div class="node">
                                                <span class="twisty">●</span>
                                                <span class="icon">📄</span>
                                                <span class="title">design-ideas.txt</span>
                                            </div>
                                        </li>
                                        <li>
                                            <div class="node">
                                                <span class="twisty">●</span>
                                                <span class="icon">📄</span>
                                                <span class="title">meeting-minutes.md</span>
                                            </div>
                                        </li>
                                    </ul>
                                </li>
                                 <li>
                                    <div class="node">
                                        <span class="twisty">▶</span>
                                        <span class="icon">📁</span>
                                        <span class="title">archive</span>
                                    </div>
                                </li>
                            </ul>
                        </aside>
                        <section class="editor">
                            <div class="status">
                                <span class="pill">NOTE</span>
                                <span class="dim">/notes/design-ideas.txt</span>
                            </div>
                            <div class="textarea-mock">
This is a sample note.<br>
It shows how the text looks.<br>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </div>
        '''.format( 
            theme_name=theme_name,
            bg=theme_data.get('bg', '#fff'),
            fg=theme_data.get('fg', '#000'),
            css_variables=css_variables
        )

    with open(os.path.join(themes_dir, 'template.html'), 'r') as f:
        main_html = f.read()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(main_html.replace('{previews_html}', previews_html))

    print("Successfully generated '" + output_file + "' with " + str(len(theme_files)) + " theme previews.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'theme_previews.html')
    create_theme_preview_grid(script_dir, output_path)
