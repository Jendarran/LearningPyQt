import sys, requests, collections
import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style

style.use('ggplot')


class Exchange(QtWidgets.QWidget):
    """Creates a window that displays the exchange rate for a single currency pair at a time in addition to a graph of
    the rate over the past 30 days.  The default view is EUR/USD.

    Note: 30 days takes 6-8 seconds to load per graph.  The line below to change the day range is commented below in
    case you want less data in exchange for a quicker response.
    """

    def __init__(self):
        """Inits Exchange with selection boxes and accompanying graph, calling init_ui() to finalize."""
        super().__init__()

        self.combo1 = QtWidgets.QComboBox()
        self.combo2 = QtWidgets.QComboBox()

        self.exrt1 = QtWidgets.QLabel('1')
        self.exrt2 = QtWidgets.QLabel('1')

        self.graph = PlotCanvas(self)

        self.init_ui()

    def init_ui(self):
        """Finalizes initialization for code clarity."""
        h_box1 = QtWidgets.QHBoxLayout()
        h_box2 = QtWidgets.QHBoxLayout()

        v_box1 = QtWidgets.QVBoxLayout()
        v_box2 = QtWidgets.QVBoxLayout()
        v_box3 = QtWidgets.QVBoxLayout()

        currency_list = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK',
                         'DKK', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'EUR',
                         'ILS', 'INR', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK',
                         'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD',
                         'THB', 'TRY', 'USD', 'ZAR']

        self.combo1.addItems(currency_list)
        self.combo1.setCurrentIndex(13)
        self.combo2.addItems(currency_list)
        self.combo2.setCurrentIndex(30)

        self.exrt1.setAlignment(Qt.AlignRight)
        self.exrt2.setAlignment(Qt.AlignRight)

        submit = QtWidgets.QPushButton('Get Rate')

        h_box1.addWidget(self.exrt1)
        h_box1.addWidget(self.combo1)

        h_box2.addWidget(self.exrt2)
        h_box2.addWidget(self.combo2)

        v_box1.addLayout(h_box1)
        v_box1.addLayout(h_box2)
        v_box1.addWidget(submit)
        v_box1.setContentsMargins(200, 10, 200, 10)

        v_box2.addWidget(self.graph)

        v_box3.addLayout(v_box1)
        v_box3.addLayout(v_box2)
        self.setLayout(v_box3)

        self.get_rates()
        submit.clicked.connect(self.get_rates)

        self.setWindowTitle('Exchange Rates')
        self.setGeometry(400, 200, 625, 535)
        self.show()

    def get_rates(self):
        """Requests current exchange rate data from Fixer.io."""
        first_currency = self.combo1.currentText()
        second_currency = self.combo2.currentText()

        if first_currency == second_currency:
            self.exrt1.setText('1')
            self.exrt2.setText('1')
        else:
            data = requests.get('http://api.fixer.io/latest?base={}'.format(first_currency))
            rates_dict = data.json()['rates']

            self.exrt1.setText('1')
            self.exrt2.setText(str(rates_dict[second_currency]))

        self.display_graph()

    def display_graph(self):
        """Requests past 30 day exchange rate data and displays on a graph."""
        first_currency = self.combo1.currentText()
        second_currency = self.combo2.currentText()

        if first_currency != second_currency:
            graph_pairs = collections.OrderedDict()
            date = datetime.date.today()

            for i in range(30):  # You can change the date range here.
                url = 'http://api.fixer.io/{}?base={}'.format(str(date), first_currency)
                response = requests.get(url)
                rates_dict = response.json()['rates']
                graph_pairs[date] = rates_dict[second_currency]
                date -= datetime.timedelta(days=1)

            dates = []
            values = []
            for d, v in graph_pairs.items():
                dates.append(d)
                values.append(v)
            graph_title = '{} vs {}'.format(first_currency, second_currency)

            self.graph.plot(dates, values, graph_title)


class PlotCanvas(FigureCanvas):
    """Creates a matplotlib Figure object that can then be passed exchange rate data."""

    def __init__(self, parent=None, width=3, height=2, dpi=100):
        """Initializes PlotCanvas with a single plot and allows it to adjust with window size."""
        self.f = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.f.add_subplot(111)

        FigureCanvas.__init__(self, self.f)
        self.setParent(parent)

        self.f.set_tight_layout(True)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, dates, values, title):
        """Clears current plot and populates graph with new data."""
        self.ax.cla()

        for label in self.ax.xaxis.get_ticklabels():
            label.set_rotation(20)

        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)

        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')
        self.ax.plot_date(dates, values, '-')
        self.ax.set_title(title)
        self.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    getRates = Exchange()
    sys.exit(app.exec_())
