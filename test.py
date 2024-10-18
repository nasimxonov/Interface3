import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QPushButton, QRadioButton, QButtonGroup, 
    QMessageBox, QLineEdit
)

class Savol:
    def __init__(self, savol_matni, javoblar, togri_javob):
        self.savol_matni = savol_matni
        self.javoblar = javoblar
        self.togri_javob = togri_javob

class TestApp(QWidget):
    def __init__(self, savollar, ismi):
        super().__init__()
        self.savollar = savollar
        self.savol_indeks = 0
        self.togri_javoblar_soni = 0
        self.ismi = ismi

        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()

        self.savol_label = QLabel(self)
        self.layout.addWidget(self.savol_label)

        self.javoblar_group = QButtonGroup(self)
        self.javob_radiolar = []
        for i in range(3):
            rb = QRadioButton(self)
            self.javoblar_group.addButton(rb)
            self.layout.addWidget(rb)
            self.javob_radiolar.append(rb)

        self.keyingisi_btn = QPushButton('Keyingisi', self)
        self.keyingisi_btn.clicked.connect(self.keyingi_savol)
        self.layout.addWidget(self.keyingisi_btn)

        self.setLayout(self.layout)
        self.savolni_korsat()

    def savolni_korsat(self):
        savol = self.savollar[self.savol_indeks]
        self.savol_label.setText(savol.savol_matni)

        for i, rb in enumerate(self.javob_radiolar):
            rb.setText(savol.javoblar[i])
            rb.setChecked(False)

    def keyingi_savol(self):
        tanlangan_javob_button = self.javoblar_group.checkedButton()
        if tanlangan_javob_button is None:
            QMessageBox.warning(self, 'Ogohlantirish', 'Javobni tanlang!')
            return

        tanlangan_javob = tanlangan_javob_button.text()

        togri_javob = self.savollar[self.savol_indeks].togri_javob
        if tanlangan_javob == togri_javob:
            self.togri_javoblar_soni += 1

        self.savol_indeks += 1

        if self.savol_indeks >= len(self.savollar):
            self.natijani_korsat()
        else:
            self.savolni_korsat()

    def natijani_korsat(self):
        ball = self.togri_javoblar_soni * 5  
        natija = f"{self.ismi}, siz {self.togri_javoblar_soni}/{len(self.savollar)} ta savolga to'g'ri javob berdingiz! Sizning ballaringiz: {ball}"
        QMessageBox.information(self, 'Test natijasi', natija)
        self.close()

def savollarni_oqish(fayl_nomi):
    with open(fayl_nomi, 'r') as fayl:
        data = json.load(fayl)
        return [Savol(item['savol'], item['javoblar'], item['togri']) for item in data['savollar']]

class IsmInput(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.label = QLabel("Ismingizni kiriting:")
        self.layout.addWidget(self.label)

        self.ismi_input = QLineEdit(self)
        self.layout.addWidget(self.ismi_input)

        self.submit_btn = QPushButton("Davom etish", self)
        self.submit_btn.clicked.connect(self.davom_etish)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def davom_etish(self):
        ismi = self.ismi_input.text()
        if not ismi:
            QMessageBox.warning(self, 'Ogohlantirish', 'Ism kiriting!')
            return

        self.close()
        self.start_test(ismi)

    def start_test(self, ismi):
        savollar = savollarni_oqish('savollar.json')
        self.test_app = TestApp(savollar, ismi)
        self.test_app.setWindowTitle('Test Dasturi')
        self.test_app.resize(400, 300)
        self.test_app.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ism_input = IsmInput()
    ism_input.setWindowTitle('Ism Kiritish')
    ism_input.resize(300, 150)
    ism_input.show()

    sys.exit(app.exec_())
