from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QStackedWidget
from PySide6.QtCore import Qt, QTimer, QEvent, QObject, Signal, QSize
from PySide6.QtGui import QCursor, QIcon, QMovie
from functools import partial
from basiclingua import BasicLingua

    
    
class TextTranslationPage(QWidget):
    back_to_main = Signal()  

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        top_row_layout = QHBoxLayout()
        layout.addLayout(top_row_layout)
        
        back_button = QPushButton(self)
        back_button.setIcon(QIcon("back-button.png")) 
        back_button.setStyleSheet("background-color: #333; border: none; color: whitesmoke;")  
        back_button.setFixedSize(70, 70)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: none;
                color: white;
                font-size: 20px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #45a049; /* Change color on hover */
            }
        """)
        back_button.clicked.connect(self.go_to_main_window)
        top_row_layout.addWidget(back_button)
        
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.addSpacing(50)
        
        title_label = QLabel("Text Translation", self)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px; color: whitesmoke;")
        input_layout.addWidget(title_label)
        
        self.api_input = QLineEdit(self)
        self.api_input.setPlaceholderText("Enter API Key")
        self.api_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.api_input.setFixedSize(300, 40)
        self.api_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.api_input.installEventFilter(self)
        input_layout.addWidget(self.api_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("User Input")
        self.user_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.user_input.setFixedSize(300, 40)
        self.user_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.user_input.installEventFilter(self)
        input_layout.addWidget(self.user_input)


        self.target_language_input = QLineEdit(self)
        self.target_language_input.setPlaceholderText("Target Language")
        self.target_language_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.target_language_input.setFixedSize(300, 40)
        self.target_language_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.target_language_input.installEventFilter(self)
        input_layout.addWidget(self.target_language_input)
        
       

        layout.addLayout(input_layout)
        
        button_layout = QHBoxLayout()
        input_layout.addLayout(button_layout)

        translate_button = QPushButton("Translate", self)
        translate_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        translate_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        translate_button.setFixedSize(100, 50)
        translate_button.clicked.connect(self.translate_text)
        button_layout.addWidget(translate_button)
        
        self.loader_movie = QMovie("Rocket.gif")
        self.loader_label = QLabel(self)
        self.loader_label.setMovie(self.loader_movie)
        self.loader_label.hide()
        button_layout.addWidget(self.loader_label)
        
        
        self.result_label = QLabel("", self)
        self.result_label.setStyleSheet("font-size: 18px; color: whitesmoke; margin-top: 20px;")
        input_layout.addWidget(self.result_label)
        
        refresh_button = QPushButton("Refresh", self)
        refresh_button.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        refresh_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_button.setFixedSize(100, 50)
        refresh_button.clicked.connect(self.refresh_fields)
        button_layout.addWidget(refresh_button)
        
        
        
    def go_to_main_window(self):
        self.back_to_main.emit()
        
    def eventFilter(self, obj, event):
            if event.type() == QEvent.FocusIn:
                obj.setStyleSheet("border: 2px solid #160202; border-radius: 5px; color: whitesmoke; font-size: 15px;")
            elif event.type() == QEvent.FocusOut:
                obj.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px;")
            return super().eventFilter(obj, event)

    def translate_text(self):
        api_key = self.api_input.text()
        user_input = self.user_input.text()
        target_lang= self.target_language_input.text()
        
        try:
            
            self.loader_label.show()
            self.loader_movie.start()
            
            client = BasicLingua(api_key)
            translated_text = client.text_translate(user_input, target_lang)
            self.result_label.setText(f"Translated Text: {translated_text}")
            
        except ValueError:
            self.result_label.setText("Invalid Input: Please enter valid numbers.")
            
        finally:
            self.loader_label.hide()
            self.loader_movie.stop()

            
    def refresh_fields(self):
        self.user_input.clear()
        self.target_language_input.clear()
        self.result_label.clear()
    
        
class ExtractPatternPage(QWidget):
    back_to_main = Signal() 
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        top_row_layout = QHBoxLayout()
        layout.addLayout(top_row_layout)
        
        back_button = QPushButton(self)
        back_button.setIcon(QIcon("back-button.png")) 
        back_button.setStyleSheet("background-color: #333; border: none; color: whitesmoke;")  
        back_button.setFixedSize(70, 70)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: none;
                color: white;
                font-size: 20px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #45a049; /* Change color on hover */
            }
        """)
        back_button.clicked.connect(self.go_to_main_window)
        top_row_layout.addWidget(back_button)
        
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.addSpacing(50)
        
        title_label = QLabel("Extract Pattern", self)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px; color: whitesmoke;")
        input_layout.addWidget(title_label)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Enter text to extract patterns")
        self.user_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.user_input.setFixedSize(300, 40)
        self.user_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.user_input.installEventFilter(self)
        input_layout.addWidget(self.user_input)


        self.patterns_input = QLineEdit(self)
        self.patterns_input.setPlaceholderText("email, number, name...")
        self.patterns_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.patterns_input.setFixedSize(300, 40)
        self.patterns_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.patterns_input.installEventFilter(self)
        input_layout.addWidget(self.patterns_input)

        layout.addLayout(input_layout)
        
        button_layout = QHBoxLayout()
        input_layout.addLayout(button_layout)

        extract_button = QPushButton("Extract", self)
        extract_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        extract_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        extract_button.setFixedSize(100, 50)
        button_layout.addWidget(extract_button)
        
        refresh_button = QPushButton("Refresh", self)
        refresh_button.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        refresh_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_button.setFixedSize(100, 50)
        button_layout.addWidget(refresh_button)
        
        
    def go_to_main_window(self):
        self.back_to_main.emit()
        
    def eventFilter(self, obj, event):
            if event.type() == QEvent.FocusIn:
                obj.setStyleSheet("border: 2px solid #160202; border-radius: 5px; color: whitesmoke; font-size: 15px;")
            elif event.type() == QEvent.FocusOut:
                obj.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px;")
            return super().eventFilter(obj, event)
        
    
        
class TextReplacePage(QWidget):
    back_to_main = Signal() 
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        top_row_layout = QHBoxLayout()
        layout.addLayout(top_row_layout)
        
        back_button = QPushButton(self)
        back_button.setIcon(QIcon("back-button.png")) 
        back_button.setStyleSheet("background-color: #333; border: none; color: whitesmoke;")  
        back_button.setFixedSize(70, 70)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: none;
                color: white;
                font-size: 20px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #45a049; /* Change color on hover */
            }
        """)
        back_button.clicked.connect(self.go_to_main_window)
        top_row_layout.addWidget(back_button)
        
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.addSpacing(50)
        
        title_label = QLabel("Text Replace", self)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px; color: whitesmoke;")
        input_layout.addWidget(title_label)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("User Input")
        self.user_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.user_input.setFixedSize(300, 40)
        self.user_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.user_input.installEventFilter(self)
        input_layout.addWidget(self.user_input)


        self.replacement_input = QLineEdit(self)
        self.replacement_input.setPlaceholderText("Type detiales prompts specifying replacement rules")
        self.replacement_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.replacement_input.setFixedSize(300, 40)
        self.replacement_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.replacement_input.installEventFilter(self)
        input_layout.addWidget(self.replacement_input)
        layout.addLayout(input_layout)
        
        button_layout = QHBoxLayout()
        input_layout.addLayout(button_layout)

        process_button = QPushButton("Process", self)
        process_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        process_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        process_button.setFixedSize(100, 50)
        button_layout.addWidget(process_button)
        
        refresh_button = QPushButton("Refresh", self)
        refresh_button.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        refresh_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_button.setFixedSize(100, 50)
        button_layout.addWidget(refresh_button)
        
        
    def go_to_main_window(self):
        self.back_to_main.emit()
        
        
     

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Button Cluster")
        self.setStyleSheet("background-color: #333;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        
        self.setup_main_window()
        self.setup_text_translation_page()
        self.setup_extract_pattern_page() 

    def setup_main_window(self):
        main_window_widget = QWidget()
        layout = QVBoxLayout(main_window_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        
        main_title_label = QLabel("BasicLingua", self)
        main_title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: whitesmoke;")
        layout.addWidget(main_title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(60)
       
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        button_1 = QPushButton("Text Translation", self)
        button_1.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
        button_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button_1.clicked.connect(self.show_text_translation_page)
        grid_layout.addWidget(button_1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        button_2 = QPushButton("Extract Patterns", self)
        button_2.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
        button_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button_2.clicked.connect(self.show_extract_patterns_page)
        grid_layout.addWidget(button_2, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # button_3 = QPushButton("Extract Patterns", self)
        # button_3.setStyleSheet(
        #     "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
        # button_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # button_3.clicked.connect(self.show_modern_page)
        # grid_layout.addWidget(button_3, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # button_4 = QPushButton("Detect NER", self)
        # button_4.setStyleSheet(
        #     "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
        # button_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # button_4.clicked.connect(self.show_modern_page)
        # grid_layout.addWidget(button_4, 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # button_5 = QPushButton("Button 5", self)
        # button_5.setStyleSheet(
        #     "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
        # button_5.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # button_5.clicked.connect(self.show_modern_page)
        # grid_layout.addWidget(button_5, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.central_widget.addWidget(main_window_widget)


    def setup_text_translation_page(self):
        text_translation_page = TextTranslationPage()
        text_translation_page.back_to_main.connect(self.show_main_window)
        self.central_widget.addWidget(text_translation_page)
        
    def setup_extract_pattern_page(self): 
        extract_pattern_page = ExtractPatternPage()
        extract_pattern_page.back_to_main.connect(self.show_main_window)
        self.central_widget.addWidget(extract_pattern_page)

    def show_text_translation_page(self):
        self.central_widget.setCurrentIndex(1)
        
    def show_extract_patterns_page(self):
        self.central_widget.setCurrentIndex(2)
        
    
    def show_main_window(self):
        self.central_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
