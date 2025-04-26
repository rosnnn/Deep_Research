from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtGui import QPalette, QColor, QMovie
from PyQt5.QtCore import Qt

from langgraph_flow.graph_orchestrator import build_graph

class DeepResearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep Research AI Agent")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.movie = QMovie("lofi.gif")  
        self.movie.setSpeed(100) 

        self.background_label = QLabel(self)
        self.background_label.setMovie(self.movie)
        self.movie.start()

        self.question_label = QLabel("What do you want to know?")
        self.layout.addWidget(self.question_label)

        self.question_input = QLineEdit(self)
        self.layout.addWidget(self.question_input)

        self.ask_button = QPushButton("Ask", self)
        self.ask_button.clicked.connect(self.on_ask)
        self.layout.addWidget(self.ask_button)

        self.answer_label = QLabel("Answer:")
        self.layout.addWidget(self.answer_label)

        self.answer_output = QTextEdit(self)
        self.answer_output.setReadOnly(True)
        self.layout.addWidget(self.answer_output)

        self.setLayout(self.layout)

        self.set_styles()

        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.movie.setScaledSize(self.size())  
        super().resizeEvent(event)

    def set_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                color: white;
            }
            QLabel {
                font-weight: bold;
                color: white;
            }
            QLineEdit {
                color: white;
                background-color: rgba(0, 0, 0, 100);
                border: 1px solid white;
                font-weight: bold;
            }
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                font-weight: bold;
                border: 1px solid white;
            }
            QTextEdit {
                color: white;
                background-color: rgba(0, 0, 0, 100);
                border: 1px solid white;
                font-weight: bold;
            }
        """)

    def on_ask(self):
        question = self.question_input.text()

        if question:
            try:
                graph = build_graph(question)
                final_output = graph.invoke({"question": question})

                answer = final_output.get("answer", "No answer available.")
                self.answer_output.setText(answer)
            except Exception as e:
                self.answer_output.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = DeepResearchApp()
    window.show()
    app.exec_()
