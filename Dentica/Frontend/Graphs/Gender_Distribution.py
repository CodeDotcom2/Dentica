from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class GenderDistributionPie(QWidget):
    def __init__(self, data_labels, data_values, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(2, 2))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.figure.subplots_adjust(right=0.8)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(data_labels, data_values)

    def draw_chart(self, labels, values):
        ax = self.figure.add_subplot(111)
        ax.clear()
        colors = ['#1d1f27', '#5e93bf', '#99c4e7']
        wedges, _, autotexts = ax.pie(
            values,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
            x, y = autotext.get_position()
            autotext.set_position((x * 1.2, y * 1.2))

        ax.legend(
            wedges,
            labels,
            loc='upper left',
            bbox_to_anchor=(-0.15, 1.15),
            fontsize=6,
            frameon=False
        )

        ax.axis('equal')
        self.canvas.draw()



