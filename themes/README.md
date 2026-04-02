# HTTree Theme Library

A collection of themes for the HTTree standalone HTML text editor.

## How to Use

1. Press `%` while in TREE mode (not editing)
1. Select any `.json` theme file from this collection
1. Theme applies immediately
1. Save your HTML file - theme persists

## Available Themes

### Dark Themes
- **default-theme.json** - Original HTTree dark theme
- **hacker-theme.json** - Classic green terminal hacker aesthetic
- **one-dark-theme.json** - Popular Atom/VSCode One Dark theme
- **solarized-dark-theme.json** - Eye-friendly Solarized dark
- **nord-theme.json** - Cool arctic Nord color palette
- **rose-pine-theme.json** - Soft, muted rose pine colors
- **vscode-dark-theme.json** - Visual Studio Code dark theme
- **github-dark-theme.json** - GitHub's dark interface theme
- **gruvbox-theme.json** - Retro groove color scheme
- **macchiato-theme.json** - Catppuccin Macchiato theme
- **monokai-theme.json** - Classic Monokai dark theme
- **tomorrow-night-theme.json** - Tomorrow Night theme

### Light Themes
- **light-theme.json** - Clean, minimal light theme
- **solarized-light-theme.json** - Eye-friendly Solarized light
- **github-light-theme.json** - GitHub's light interface theme
- **nord-light-theme.json** - Light variant of Nord theme

## Theme Structure

Each theme is a simple JSON file with CSS color variables:

```json
{
  "bg": "#000000",        // Background color
  "fg": "#f5f5f5",       // Main text color
  "muted": "#555",        // Muted/subtle text
  "accent": "#00d1b2",    // Accent/highlight color
  "danger": "#ff5577",    // Error/danger color
  "sel-bg": "#111827",    // Selection background
  "btn-border": "#555",    // Button borders
  "border": "#222"        // General borders
}
```

## Creating Custom Themes

Create your own theme by copying any existing theme file and modifying the color values. Use any standard CSS color format (hex, rgb, etc.).

## Installation

Simply place these `.json` files anywhere accessible and use the `%` key import feature in HTTree to apply them.
