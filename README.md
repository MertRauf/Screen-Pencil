Modern Sketch Drawing Tool
Overview
The Modern Sketch Drawing Tool is a lightweight, frameless, and transparent desktop application built using PyQt5. It allows users to draw directly on their screen with various tools, colors, and settings. The application captures the screen as a background and provides an intuitive interface for free drawing, shapes, highlighting, erasing, and saving drawings as PNG files. It is designed with a modern, compact control panel that can be toggled on or off.
Features

Drawing Modes: Supports multiple drawing modes including free drawing, highlighter, straight lines, rectangles, circles, and an eraser.
Color Palette: Offers a selection of 10 vibrant colors for drawing.
Pen Thickness: Adjustable pen size (1 to 25 pixels) via a slider.
Zoom Control: Adjustable zoom level (0.5x to 3.0x) for precise drawing.
Undo Functionality: Revert the last drawing action (lines or shapes).
Save as PNG: Save the current drawing as a PNG file, with the control panel hidden during the save process.
Transparent Window: The application runs in a frameless, translucent window that stays on top of other applications.
Compact Control Panel: A sleek, customizable panel with buttons for tools, colors, and settings, which can be hidden or shown.
Keyboard Shortcuts: Extensive shortcut support for quick access to tools and actions.
Error Handling: Includes basic error handling for drawing, saving, and undoing actions.

Requirements

Python 3.6 or higher
PyQt5 (pip install PyQt5)
Operating System: Windows, macOS, or Linux (with a compatible desktop environment)

Installation

Ensure Python is installed on your system.
Install PyQt5 using pip:pip install PyQt5


Save the provided Python script (e.g., screen_draw.py) to a directory.
Run the script:python screen_draw.py



Usage

Starting the Application:

Run the script, and the application will open in a full-screen, transparent window.
The control panel appears on the left side of the screen with buttons for tools, colors, and settings.


Drawing:

Click the "Start Drawing" button (🎨) or press Ctrl+D to enter drawing mode.
The screen is captured as the background, and you can start drawing.
Use the mouse to draw in free mode, create shapes, or erase content.
Press Ctrl+D again to exit drawing mode and clear the canvas.


Control Panel:

The panel contains buttons for main controls, drawing tools, color selection, and settings (pen thickness and zoom).
Toggle the panel visibility with H or the "Hide/Show Panel" button (👁️).


Saving Drawings:

Click the "Save as PNG" button (💾) or press Ctrl+S to save the current drawing.
A file dialog will prompt you to choose a location and filename for the PNG file.
The control panel is automatically hidden during the save process to avoid capturing it in the output.


Exiting:

Click the "Exit" button (❌) or press Esc to close the application.



Keyboard Shortcuts
The application supports the following keyboard shortcuts for quick access to features:

Ctrl+D: Start or stop drawing mode.
H: Show or hide the control panel.
Ctrl+C: Clear the entire canvas.
Ctrl+Z: Undo the last drawing action.
Ctrl+S: Save the drawing as a PNG file.
Esc: Exit the application.
F: Switch to Free Drawing mode.
L: Switch to Highlighter mode.
N: Switch to Straight Line mode.
R: Switch to Rectangle mode.
C: Switch to Circle mode.
E: Switch to Eraser mode.

Drawing Tools
The application provides the following drawing tools, accessible via buttons or shortcuts:

Free Drawing (✏️, F): Draw freehand lines with the selected color and thickness.
Highlighter (🖍️, L): Draw semi-transparent lines for highlighting (opacity set to 100/255).
Straight Line (📏, N): Draw straight lines between two points.
Rectangle (⬜, R): Draw rectangles by clicking and dragging.
Circle (⭕, C): Draw circles or ellipses by clicking and dragging.
Eraser (🧽, E): Erase lines or shapes within a radius (twice the pen size) around the mouse cursor.

Color Palette
The color palette includes 10 predefined colors, arranged in two columns:

Red (#e74c3c)
Blue (#3498db)
Green (#2ecc71)
Orange (#f39c12)
Purple (#9b59b6)
Cyan (#1abc9c)
Dark Blue (#34495e)
White (#ffffff)
Yellow (#f1c40f)
Pink (#e91e63)

Click a color button to select it. In Highlighter mode, the selected color is semi-transparent.
Settings

Pen Thickness:
Adjusted via a slider (📏) ranging from 1 to 25 pixels.
The tooltip displays the current thickness value.


Zoom:
Adjusted via a slider (🔍) ranging from 0.5x to 3.0x.
The tooltip displays the current zoom level (e.g., "Zoom: 1.0x").
Zoom affects the entire canvas, scaling both the background and drawings.



Technical Details

Framework: Built with PyQt5 for cross-platform compatibility.
UI Design: Uses a custom CompactButton class for stylized buttons, ColorButton for color selection, CompactSlider for sliders, and CompactPanel for the control panel.
Drawing Mechanism:
Lines and shapes are stored in separate lists (self.lines and self.shapes) for efficient rendering and undo functionality.
The paintEvent method handles rendering with antialiasing for smooth lines.
Mouse events (mousePressEvent, mouseMoveEvent, mouseReleaseEvent) manage drawing interactions.


Styling: Uses QSS (Qt Style Sheets) with gradients, hover effects, and transformations for a modern look.
Error Handling: Displays error messages via QMessageBox for issues during drawing mode changes, saving, or undoing.

Limitations

The application captures the entire screen, which may be resource-intensive on high-resolution displays.
No support for text annotations or advanced shape editing.
The eraser removes entire lines or shapes if they intersect with the erase radius, rather than partially erasing them.
Zooming may affect performance on low-end systems due to real-time scaling.

Future Improvements

Add support for text annotations.
Implement partial erasing for more precise edits.
Add a redo function to complement undo.
Support additional file formats for saving (e.g., JPEG).
Optimize performance for high-resolution screens.

License
This project is provided as-is for educational and personal use. No specific license is applied, but please credit the original author if redistributing or modifying the code.
Contributing
Contributions are welcome! Please submit pull requests or issues to the repository (if available) or contact the author for suggestions and bug reports.

--

by MertRauf
