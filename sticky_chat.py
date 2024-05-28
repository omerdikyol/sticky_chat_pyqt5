import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
    QFileDialog, QMenuBar, QMenu, QAction, QInputDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class StickyNoteChat(QWidget):
    def __init__(self):
        super().__init__()

        self.users = ["User 1", "User 2"]
        self.current_user_index = 0
        self.user_colors = ["#ADD8E6", "#FFD700"]
        self.always_on_top = True

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sticky Chat Made By Ömer Dikyol")
        self.setGeometry(100, 100, 400, 500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()

        # Create a menu bar
        self.menu_bar = QMenuBar(self)
        self.layout.setMenuBar(self.menu_bar)

        # Add "Options" menu
        options_menu = QMenu("Options", self)
        self.menu_bar.addMenu(options_menu)

        # Add "Always On Top" option
        self.always_on_top_action = QAction("Disable Always On Top", self)
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        options_menu.addAction(self.always_on_top_action)

        # Add "Change User Names" option
        change_user_names_action = QAction("Change User Names", self)
        change_user_names_action.triggered.connect(self.change_user_names)
        options_menu.addAction(change_user_names_action)

        self.user_label = QLabel(f"Current User: {self.users[self.current_user_index]}")
        self.user_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.user_label.setStyleSheet(f"color: {self.user_colors[self.current_user_index]}; background-color: black;")
        self.layout.addWidget(self.user_label)

        self.chat_history = QTextEdit()
        self.chat_history.setFont(QFont("Arial", 12))
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)

        self.message_entry = QTextEdit()
        self.message_entry.setFont(QFont("Arial", 12))
        self.message_entry.setMaximumHeight(50)
        self.layout.addWidget(self.message_entry)

        self.button_layout = QHBoxLayout()
        
        self.send_button = QPushButton("Send [ENTER]")
        self.send_button.clicked.connect(self.add_message)
        self.button_layout.addWidget(self.send_button)

        self.change_turn_button = QPushButton(f"Change Turn [TAB]")
        self.change_turn_button.clicked.connect(self.change_turn)
        self.button_layout.addWidget(self.change_turn_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_messages)
        self.button_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_messages)
        self.button_layout.addWidget(self.export_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.message_entry.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.add_message()
                return True
            elif event.key() == Qt.Key_Tab:
                self.change_turn()
                return True
        return super().eventFilter(source, event)

    def add_message(self):
        message = self.message_entry.toPlainText().strip()
        if message != "":
            user_message = f"<div style='background-color:{self.user_colors[self.current_user_index]}; padding: 5px; margin: 5px 0;'>{self.users[self.current_user_index]}: {message}</div>"
            self.chat_history.append(user_message)
            self.message_entry.clear()

    def change_turn(self):
        self.current_user_index = 1 - self.current_user_index
        self.user_label.setText(f"Current User: {self.users[self.current_user_index]}")
        self.user_label.setStyleSheet(f"color: {self.user_colors[self.current_user_index]}; background-color: black;")
        self.change_turn_button.setText(f"Change Turn [TAB] (Current: {self.users[self.current_user_index]})")

    def clear_messages(self):
        self.chat_history.clear()

    def export_messages(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save chat log", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.chat_history.toPlainText())

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.always_on_top_action.setText("Disable Always On Top")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.always_on_top_action.setText("Enable Always On Top")
        self.show()

    def change_user_names(self):
        for i in range(len(self.users)):
            new_name, ok = QInputDialog.getText(self, "Change User Name", f"Enter new name for {self.users[i]}:")
            if ok and new_name.strip() != "":
                self.users[i] = new_name
        self.user_label.setText(f"Current User: {self.users[self.current_user_index]}")
        self.change_turn_button.setText(f"Change Turn [TAB] (Current: {self.users[self.current_user_index]})")

def main():
    app = QApplication(sys.argv)
    window = StickyNoteChat()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
