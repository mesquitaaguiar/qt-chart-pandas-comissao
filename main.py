import sys

from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

import pandas as pd
import numpy as np


class ChartComissaoQtPandas(QMainWindow):
    def __init__(self):
        super().__init__()
        
        df = pd.read_csv("vendas.csv", sep=";")
        df['ano_mes'] = df['data'].str[:7]
        df['comissao'] = pd.to_numeric((df['faturado']*(df['percentual']/100)).map('{:,.2f}'.format))

        df1 = df.groupby(["vendedor","ano_mes"])['comissao'].sum()

        it = 0
        var = ""   
        arr = []
        categories = []
        self.series = QBarSeries()  
        for index in df1.keys():
            if(it > 0 and index[0] !=  var):
                self.set_var = QBarSet(var)
                self.set_var.append(arr)
                self.series.append(self.set_var)
                arr = [] 
                arr.append(df1[1])
            else:
                arr.append(df1[it])
            if(index[1] not in categories):
                categories.append(index[1])    
            var = index[0]
            it = it + 1

        if(it > 0):
            self.set_var = QBarSet(var)
            self.set_var.append(arr)
            self.series.append(self.set_var)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Pagamento de Comissão")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.categories = categories
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(200000, 7500)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ChartComissaoQtPandas()
    window.resize(1200, 640)
    window.show()
    sys.exit(app.exec())