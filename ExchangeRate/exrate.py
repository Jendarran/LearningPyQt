import sys, requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtCore import Qt

class Exchange(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.exrt1 = QLabel('1')
        self.exrt1.setAlignment(Qt.AlignRight)
        self.exrt2 = QLabel('1')
        self.exrt2.setAlignment(Qt.AlignRight)

        self.currencyList = ['AUD' ,'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK',
                             'DKK', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS',
                             'INR', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD',
                             'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB',
                             'TRY', 'USD', 'ZAR']

        self.combo1 = QComboBox()
        self.combo1.addItems(self.currencyList)
        self.combo2 = QComboBox()
        self.combo2.addItems(self.currencyList)
        self.submit = QPushButton('Get Rate')

        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()
        v_box = QVBoxLayout()

        h_box1.addWidget(self.exrt1)
        h_box1.addWidget(self.combo1)
        h_box2.addWidget(self.exrt2)
        h_box2.addWidget(self.combo2)
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addWidget(self.submit)
        self.setLayout(v_box)

        self.submit.clicked.connect(self.get_rates)
        self.setWindowTitle('Rates')
        self.setGeometry(500, 300, 200, 150)
        self.show()



    def get_rates(self):
        data = requests.get('http://api.fixer.io/latest?base=' + self.combo1.currentText())
        rates_list = data.json()['rates']

        if self.combo1.currentText() == self.combo2.currentText():
            self.exrt1.setText('1')
            self.exrt2.setText('1')
        else:
            self.exrt1.setText('1')
            self.exrt2.setText(str(rates_list[self.combo2.currentText()]))

app = QApplication(sys.argv)
getRates = Exchange()
sys.exit(app.exec_())
