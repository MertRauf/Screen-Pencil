import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QSpinBox, QLabel, QFileDialog, QSlider, QToolButton, 
    QMessageBox, QFrame, QButtonGroup, QSizePolicy
)
from PyQt5.QtGui import (
    QPainter, QPen, QPixmap, QColor, QIcon, QFont, QFontMetrics, 
    QLinearGradient, QPainterPath, QBrush
)
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty

class CompactButton(QPushButton):
    """Compact icon button class"""
    def __init__(self, icon, tooltip_text, color="#3498db", parent=None):
        super().__init__(parent)
        self.setText(icon)
        self.setToolTip(tooltip_text)
        self.base_color = color
        self.setFixedSize(50, 50)  # Increased button size
        self.setFont(QFont("Segoe UI Emoji", 16))
        self.setup_style()
        
    def setup_style(self):
        """Sets up button style"""
        style = f"""
            CompactButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.base_color}, stop:1 {self.darken_color(self.base_color)});
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                margin: 5px;  /* Increased margin */
            }}
            CompactButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.lighten_color(self.base_color)}, 
                    stop:1 {self.base_color});
                transform: scale(1.1);
            }}
            CompactButton:pressed {{
                background: {self.darken_color(self.base_color)};
                transform: scale(0.95);
            }}
            CompactButton:checked {{
                background: {self.lighten_color(self.base_color)};
                border: 2px solid white;
            }}
            QToolTip {{
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                border-radius: 8px;
                padding: 5px;
                font: 11px 'Segoe UI';
            }}
        """
        self.setStyleSheet(style)
    
    def darken_color(self, color):
        """Darkens the color"""
        c = QColor(color)
        return f"rgb({max(0, c.red()-30)}, {max(0, c.green()-30)}, {max(0, c.blue()-30)})"
    
    def lighten_color(self, color):
        """Lightens the color"""
        c = QColor(color)
        return f"rgb({min(255, c.red()+30)}, {min(255, c.green()+30)}, {min(255, c.blue()+30)})"

class ColorButton(QToolButton):
    """Compact button for color selection"""
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(32, 32)  # Increased color button size
        self.setToolTip(f"Color: {color.name()}")
        self.setup_style()
        
    def setup_style(self):
        color_str = f"rgb({self.color.red()}, {self.color.green()}, {self.color.blue()})"
        style = f"""
            ColorButton {{
                background-color: {color_str};
                border: 2px solid #34495e;
                border-radius: 16px;
                margin: 4px;  /* Increased margin */
            }}
            ColorButton:hover {{
                border: 3px solid #3498db;
                transform: scale(1.15);
            }}
            ColorButton:pressed {{
                border: 3px solid #2980b9;
            }}
            QToolTip {{
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                border-radius: 8px;
                padding: 5px;
                font: 11px 'Segoe UI';
            }}
        """
        self.setStyleSheet(style)

class CompactSlider(QSlider):
    """Compact slider"""
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setFixedWidth(120)
        self.setup_style()
    
    def setup_style(self):
        style = """
            QSlider::groove:horizontal {
                background: #34495e;
                height: 6px;
                border-radius: 3px;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #5dade2;
                transform: scale(1.2);
            }
        """
        self.setStyleSheet(style)

class CompactPanel(QFrame):
    """Compact left panel"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setFixedWidth(80)  # Increased panel width
        self.setup_style()
        
    def setup_style(self):
        """Sets up panel style"""
        style = """
            CompactPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(44, 62, 80, 0.95), 
                    stop:1 rgba(52, 73, 94, 0.85));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px 8px;  /* Increased padding */
            }
        """
        self.setStyleSheet(style)

class ScreenDrawApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Sketch Drawing Tool")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setup_screen_geometry()
        self.initialize_drawing_state()
        self.setup_ui()

    def setup_screen_geometry(self):
        """Sets up screen dimensions"""
        self.screen = QApplication.primaryScreen()
        screen_size = self.screen.size()
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())

    def initialize_drawing_state(self):
        """Initializes drawing state"""
        self.drawing = False
        self.draw_mode = False
        self.last_point = None
        self.current_color = QColor("#e74c3c")
        self.pen_size = 5
        self.mode = "free"
        self.lines = []
        self.shapes = []
        self.history = []
        self.background = None
        self.start_point = None
        self.zoom_factor = 1.0
        self.panel_visible = True

    def setup_ui(self):
        """Sets up user interface"""
        # Left panel
        self.control_panel = CompactPanel(self)
        panel_height = min(650, self.height() - 100)  # Increased panel height
        self.control_panel.setFixedHeight(panel_height)
        
        # Position panel at left center
        panel_x = 20
        panel_y = (self.height() - panel_height) // 2
        self.control_panel.move(panel_x, panel_y)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)  # Increased spacing between buttons
        main_layout.setContentsMargins(8, 10, 8, 10)  # Increased inner margins
        
        # Main controls
        self.setup_main_controls(main_layout)
        
        # Separator line
        separator1 = self.create_separator()
        main_layout.addWidget(separator1)
        
        # Drawing tools
        self.setup_drawing_tools(main_layout)
        
        # Separator line
        separator2 = self.create_separator()
        main_layout.addWidget(separator2)
        
        # Colors
        self.setup_color_palette(main_layout)
        
        # Separator line
        separator3 = self.create_separator()
        main_layout.addWidget(separator3)
        
        # Settings
        self.setup_settings(main_layout)
        
        # Bottom spacer
        main_layout.addStretch()
        
        self.control_panel.setLayout(main_layout)
        self.setMouseTracking(True)

    def create_separator(self):
        """Creates separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFixedHeight(8)  # Increased separator height
        separator.setStyleSheet("""
            QFrame {
                color: rgba(255, 255, 255, 0.3);
                margin: 8px 12px;  /* Increased margin */
            }
        """)
        return separator

    def setup_main_controls(self, layout):
        """Sets up main control buttons"""
        # Start/Stop drawing button
        self.draw_button = CompactButton("🎨", "Start/Stop Drawing (Ctrl+D)", "#27ae60")
        self.draw_button.clicked.connect(self.toggle_draw_mode)
        self.draw_button.setShortcut("Ctrl+D")
        layout.addWidget(self.draw_button)
        
        # Hide/Show panel
        hide_button = CompactButton("👁️", "Hide/Show Panel (H)", "#95a5a6")
        hide_button.clicked.connect(self.toggle_panel)
        hide_button.setShortcut("H")
        layout.addWidget(hide_button)
        
        # Clear
        clear_button = CompactButton("🗑️", "Clear All (Ctrl+C)", "#e67e22")
        clear_button.clicked.connect(self.clear_canvas)
        clear_button.setShortcut("Ctrl+C")
        layout.addWidget(clear_button)
        
        # Undo
        undo_button = CompactButton("↩️", "Undo (Ctrl+Z)", "#9b59b6")
        undo_button.clicked.connect(self.undo)
        undo_button.setShortcut("Ctrl+Z")
        layout.addWidget(undo_button)
        
        # Save
        save_button = CompactButton("💾", "Save as PNG (Ctrl+S)", "#3498db")
        save_button.clicked.connect(self.save_png)
        save_button.setShortcut("Ctrl+S")
        layout.addWidget(save_button)
        
        # Exit
        exit_button = CompactButton("❌", "Exit Application (Esc)", "#e74c3c")
        exit_button.clicked.connect(self.close)
        exit_button.setShortcut("Esc")
        layout.addWidget(exit_button)

    def setup_drawing_tools(self, layout):
        """Sets up drawing tools"""
        # Tool buttons
        self.tool_group = QButtonGroup()
        tools = [
            ("✏️", "Free Drawing (F)", "free", "#3498db"),
            ("🖍️", "Highlighter (L)", "highlighter", "#f39c12"),
            ("📏", "Straight Line (N)", "line", "#2ecc71"),
            ("⬜", "Rectangle (R)", "rect", "#9b59b6"),
            ("⭕", "Circle (C)", "circle", "#e67e22"),
            ("🧽", "Eraser (E)", "eraser", "#e74c3c")
        ]
        
        for icon, tooltip, mode, color in tools:
            button = CompactButton(icon, tooltip, color)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, m=mode: self.set_mode(m))
            self.tool_group.addButton(button)
            layout.addWidget(button)
            
            if mode == "free":
                button.setChecked(True)

    def setup_color_palette(self, layout):
        """Sets up color palette"""
        # Color buttons - in two columns
        colors = [
            QColor("#e74c3c"), QColor("#3498db"), 
            QColor("#2ecc71"), QColor("#f39c12"), 
            QColor("#9b59b6"), QColor("#1abc9c"),
            QColor("#34495e"), QColor("#ffffff"), 
            QColor("#f1c40f"), QColor("#e91e63")
        ]
        
        for i in range(0, len(colors), 2):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10)  # Increased spacing between color buttons
            row_layout.setContentsMargins(2, 2, 2, 2)  # Added inner margins
            
            # Left color
            color_btn1 = ColorButton(colors[i])
            color_btn1.clicked.connect(lambda checked, c=colors[i]: self.change_color(c))
            row_layout.addWidget(color_btn1)
            
            # Right color (if available)
            if i + 1 < len(colors):
                color_btn2 = ColorButton(colors[i + 1])
                color_btn2.clicked.connect(lambda checked, c=colors[i + 1]: self.change_color(c))
                row_layout.addWidget(color_btn2)
            
            row_widget = QWidget()
            row_widget.setLayout(row_layout)
            layout.addWidget(row_widget)

    def setup_settings(self, layout):
        """Sets up settings"""
        # Thickness setting
        thickness_layout = QVBoxLayout()
        thickness_layout.setSpacing(5)  # Increased spacing
        thickness_layout.setContentsMargins(0, 5, 0, 10)  # Added bottom margin
        
        thickness_label = QLabel("📏")
        thickness_label.setStyleSheet("color: white; font: 16px 'Segoe UI Emoji'; text-align: center;")
        thickness_label.setAlignment(Qt.AlignCenter)
        thickness_label.setToolTip("Pen Thickness")
        
        self.thickness_slider = CompactSlider(Qt.Horizontal)
        self.thickness_slider.setRange(1, 25)
        self.thickness_slider.setValue(5)
        self.thickness_slider.valueChanged.connect(self.update_pen_size)
        self.thickness_slider.setToolTip("Pen Thickness: 5")
        
        thickness_layout.addWidget(thickness_label)
        thickness_layout.addWidget(self.thickness_slider)
        
        thickness_widget = QWidget()
        thickness_widget.setLayout(thickness_layout)
        layout.addWidget(thickness_widget)
        
        # Zoom setting
        zoom_layout = QVBoxLayout()
        zoom_layout.setSpacing(5)  # Increased spacing
        zoom_layout.setContentsMargins(0, 5, 0, 5)  # Added margins
        
        zoom_label = QLabel("🔍")
        zoom_label.setStyleSheet("color: white; font: 16px 'Segoe UI Emoji'; text-align: center;")
        zoom_label.setAlignment(Qt.AlignCenter)
        zoom_label.setToolTip("Zoom")
        
        self.zoom_slider = CompactSlider(Qt.Horizontal)
        self.zoom_slider.setRange(5, 30)
        self.zoom_slider.setValue(10)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        self.zoom_slider.setToolTip("Zoom: 1.0x")
        
        zoom_layout.addWidget(zoom_label)
        zoom_layout.addWidget(self.zoom_slider)
        
        zoom_widget = QWidget()
        zoom_widget.setLayout(zoom_layout)
        layout.addWidget(zoom_widget)

    def toggle_draw_mode(self):
        """Toggles drawing mode"""
        try:
            self.draw_mode = not self.draw_mode
            if self.draw_mode:
                screen_size = self.screen.size()
                self.background = self.screen.grabWindow(0, 0, 0, screen_size.width(), screen_size.height())
                self.draw_button.setText("⏸️")
                self.draw_button.setToolTip("Stop Drawing (Ctrl+D)")
                self.draw_button.base_color = "#e74c3c"
                self.draw_button.setup_style()
            else:
                self.reset_drawing_state()
                self.draw_button.setText("🎨")
                self.draw_button.setToolTip("Start Drawing (Ctrl+D)")
                self.draw_button.base_color = "#27ae60"
                self.draw_button.setup_style()
            self.update()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error changing drawing mode: {str(e)}")

    def toggle_panel(self):
        """Hides/shows the panel"""
        self.panel_visible = not self.panel_visible
        if self.panel_visible:
            self.control_panel.show()
        else:
            self.control_panel.hide()

    def set_mode(self, mode):
        """Sets drawing mode"""
        self.mode = mode
        if mode == "highlighter":
            self.current_color.setAlpha(100)
        else:
            self.current_color.setAlpha(255)

    def change_color(self, color):
        """Changes the color"""
        self.current_color = color
        if self.mode == "highlighter":
            self.current_color.setAlpha(100)

    def update_pen_size(self, size):
        """Updates pen thickness"""
        self.pen_size = size
        self.thickness_slider.setToolTip(f"Pen Thickness: {size}")

    def update_zoom(self, value):
        """Updates zoom level"""
        self.zoom_factor = value / 10.0
        self.zoom_slider.setToolTip(f"Zoom: {self.zoom_factor:.1f}x")
        self.update()

    def clear_canvas(self):
        """Clears the drawing canvas"""
        self.lines.clear()
        self.shapes.clear()
        self.history.clear()
        self.update()

    def reset_drawing_state(self):
        """Resets drawing state"""
        self.background = None
        self.lines.clear()
        self.shapes.clear()
        self.history.clear()
        self.zoom_factor = 1.0

    def undo(self):
        """Undoes the last action"""
        try:
            if self.history:
                action, index = self.history.pop()
                if action == "line" and index < len(self.lines):
                    self.lines.pop(index)
                elif action == "shape" and index < len(self.shapes):
                    self.shapes.pop(index)
                self.update()
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Undo error: {str(e)}")

    def save_png(self):
        """Saves as PNG"""
        try:
            if not self.draw_mode or not self.background:
                QMessageBox.warning(self, "Warning", "Start drawing mode first!")
                return
                
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Drawing", "", "PNG Files (*.png);;All Files (*)"
            )
            if file_name:
                # Temporarily hide panel
                panel_was_visible = self.panel_visible
                if panel_was_visible:
                    self.control_panel.hide()
                
                pixmap = QPixmap(self.size())
                pixmap.fill(Qt.transparent)
                self.render(pixmap)
                pixmap.save(file_name, "PNG")
                
                # Show panel again
                if panel_was_visible:
                    self.control_panel.show()
                    
                QMessageBox.information(self, "Success", "Drawing saved!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save error: {str(e)}")

    def paintEvent(self, event):
        """Drawing event"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            if self.draw_mode and self.background:
                painter.scale(self.zoom_factor, self.zoom_factor)
                painter.drawPixmap(0, 0, self.background)
                
                # Draw lines
                for points, color, size in self.lines:
                    pen = QPen(color, size / self.zoom_factor, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                    painter.setPen(pen)
                    painter.setOpacity(color.alpha() / 255.0)
                    
                    for i in range(len(points) - 1):
                        painter.drawLine(points[i], points[i + 1])
                
                # Draw shapes
                for shape_type, start, end, color, size in self.shapes:
                    pen = QPen(color, size / self.zoom_factor, Qt.SolidLine, Qt.RoundCap)
                    painter.setPen(pen)
                    painter.setOpacity(1.0)
                    
                    if shape_type == "line":
                        painter.drawLine(start, end)
                    elif shape_type == "rect":
                        painter.drawRect(QRect(start, end))
                    elif shape_type == "circle":
                        rect = QRect(start, end).normalized()
                        painter.drawEllipse(rect)
                
                painter.setOpacity(1.0)
        except Exception as e:
            pass  # Silently handle drawing errors

    def mousePressEvent(self, event):
        """Mouse press event"""
        if self.draw_mode and event.button() == Qt.LeftButton:
            adjusted_pos = QPoint(
                int(event.pos().x() / self.zoom_factor), 
                int(event.pos().y() / self.zoom_factor)
            )
            self.drawing = True
            self.last_point = adjusted_pos
            self.start_point = adjusted_pos
            
            if self.mode in ["free", "highlighter"]:
                self.lines.append(([self.last_point], self.current_color, self.pen_size))
                self.history.append(("line", len(self.lines) - 1))
            elif self.mode == "eraser":
                self.erase_at(adjusted_pos)
            
            self.update()

    def mouseMoveEvent(self, event):
        """Mouse move event"""
        if self.draw_mode and self.drawing and event.buttons() & Qt.LeftButton:
            adjusted_pos = QPoint(
                int(event.pos().x() / self.zoom_factor), 
                int(event.pos().y() / self.zoom_factor)
            )
            
            if self.mode in ["free", "highlighter"]:
                self.lines[-1][0].append(adjusted_pos)
                self.last_point = adjusted_pos
                self.update()
            elif self.mode == "eraser":
                self.erase_at(adjusted_pos)
                self.update()

    def mouseReleaseEvent(self, event):
        """Mouse release event"""
        if self.draw_mode and event.button() == Qt.LeftButton:
            adjusted_pos = QPoint(
                int(event.pos().x() / self.zoom_factor), 
                int(event.pos().y() / self.zoom_factor)
            )
            
            if self.mode in ["line", "rect", "circle"]:
                self.shapes.append((self.mode, self.start_point, adjusted_pos, self.current_color, self.pen_size))
                self.history.append(("shape", len(self.shapes) - 1))
            
            self.drawing = False
            self.start_point = None
            self.update()

    def erase_at(self, point):
        """Erases at the specified point"""
        erase_radius = self.pen_size * 2
        
        # Check lines
        self.lines = [
            (points, color, size) for points, color, size in self.lines
            if not any((p.x() - point.x()) ** 2 + (p.y() - point.y()) ** 2 < erase_radius ** 2 for p in points)
        ]
        
        # Check shapes
        new_shapes = []
        for shape_type, start, end, color, size in self.shapes:
            keep = True
            if shape_type == "line":
                if ((start.x() - point.x()) ** 2 + (start.y() - point.y()) ** 2 < erase_radius ** 2 or
                    (end.x() - point.x()) ** 2 + (end.y() - point.y()) ** 2 < erase_radius ** 2):
                    keep = False
            elif shape_type in ["rect", "circle"]:
                rect = QRect(start, end).normalized()
                if rect.contains(point):
                    keep = False
            
            if keep:
                new_shapes.append((shape_type, start, end, color, size))
        
        self.shapes = new_shapes

    def keyPressEvent(self, event):
        """Keyboard events"""
        shortcuts = {
            Qt.Key_H: self.toggle_panel,
            Qt.Key_F: lambda: self.set_mode("free"),
            Qt.Key_L: lambda: self.set_mode("highlighter"),
            Qt.Key_N: lambda: self.set_mode("line"),
            Qt.Key_R: lambda: self.set_mode("rect"),
            Qt.Key_C: lambda: self.set_mode("circle"),
            Qt.Key_E: lambda: self.set_mode("eraser"),
            Qt.Key_Escape: self.close
        }
        
        if event.key() in shortcuts:
            shortcuts[event.key()]()
        elif event.modifiers() & Qt.ControlModifier:
            ctrl_shortcuts = {
                Qt.Key_D: self.toggle_draw_mode,
                Qt.Key_C: self.clear_canvas,
                Qt.Key_Z: self.undo,
                Qt.Key_S: self.save_png
            }
            if event.key() in ctrl_shortcuts:
                ctrl_shortcuts[event.key()]()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # For modern appearance
    window = ScreenDrawApp()
    window.show()
    sys.exit(app.exec_())