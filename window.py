from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import random
import time
import os
import matplotlib.pyplot as plt
import numpy as np
import winsound


# klasa służąca do czekania na wyświetlenie koloru/ zagranie dźwięku
# wykonuje to w osobnym wątku aby nie mrozić GUI przez ten czas
class Worker(QObject):
    finished = pyqtSignal()
    interrupted = pyqtSignal()
    _isRunning = True

    def run(self):
        rand_time = random.randint(200, 800) / 100
        time.sleep(rand_time)
        if self._isRunning is True:
            self.finished.emit()
        else:
            self.interrupted.emit()

    def stop(self):
        self._isRunning = False


# klasa głównego okna
class Ui_MainWindow(object):

    def __init__(self):
        self.is_start_button_first_click = True
        self.green_color_appearance_time = 0
        self.sound_appearance_time = 0
        self.is_test = False
        self.is_visual = False
        self.is_acoustic = False
        self.thread_was_interrupted = False
        self.kind_of_test = -1
        self.results = []
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setUi(self, MainWindow):

        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(6, 270, 781, 21))
        self.result_label.setObjectName("result_label")
        self.result_label.setText("")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)

        self.test_end_button = QtWidgets.QPushButton(self.centralwidget)
        self.test_end_button.setGeometry(QtCore.QRect(350, 440, 111, 25))
        self.test_end_button.setObjectName("test_end_button")
        self.test_end_button.setText("Statystyki")
        self.test_end_button.clicked.connect(self.statystyki)

        self.plot_results_button = QtWidgets.QPushButton(self.centralwidget)
        self.plot_results_button.setGeometry(QtCore.QRect(340, 480, 131, 25))
        self.plot_results_button.setObjectName("plot_results_button")
        self.plot_results_button.setText("Rysuj wykres")
        self.plot_results_button.clicked.connect(self.show_results)

        self.instruction_button = QtWidgets.QPushButton(self.centralwidget)
        self.instruction_button.setGeometry(QtCore.QRect(360, 400, 89, 25))
        self.instruction_button.setObjectName("instruction_button")
        self.instruction_button.setText("Instrukcja")
        self.instruction_button.clicked.connect(self.instrukcja)

        self.trying_radiobutton = QtWidgets.QRadioButton(self.centralwidget)
        self.trying_radiobutton.setGeometry(QtCore.QRect(270, 350, 112, 23))
        self.trying_radiobutton.setObjectName("trying_radiobutton")
        self.trying_radiobutton.setText("Wypróbuj")
        self.trying_radiobutton.setChecked(True)
        self.trying_radiobutton.clicked.connect(self.test_clicked)

        self.test_radiobutton = QtWidgets.QRadioButton(self.centralwidget)
        self.test_radiobutton.setGeometry(QtCore.QRect(450, 350, 112, 23))
        self.test_radiobutton.setObjectName("test_radiobutton")
        self.test_radiobutton.setText("Test")
        self.test_radiobutton.clicked.connect(self.test_clicked)

        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(8, 4, 781, 261))
        self.start_button.setObjectName("start_button")
        self.start_button.setText("Rozpocznij")
        self.start_button.clicked.connect(self.start_test)

        self.visual_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.visual_checkbox.setGeometry(QtCore.QRect(270, 310, 92, 23))
        self.visual_checkbox.setObjectName("visual_checkbox")
        self.visual_checkbox.setText("Wizualny")
        self.visual_checkbox.clicked.connect(self.visual_clicked)

        self.acoustic_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.acoustic_checkbox.setGeometry(QtCore.QRect(450, 310, 101, 23))
        self.acoustic_checkbox.setObjectName("acoustic_checkbox")
        self.acoustic_checkbox.setText("Dźwiękowy")
        self.acoustic_checkbox.clicked.connect(self.acoustic_clicked)

        MainWindow.setCentralWidget(self.centralwidget)

    def instrukcja(self):
        msg = QMessageBox(MainWindow)
        msg.setWindowTitle("Instrukcja")
        msg.setText("Instrukcja przeprowadzenia testu")
        msg.setInformativeText("Witaj w teście sprawdzenia Twojej sprawności psychomotorycznej!\n\n"
                               "Aby wykonywać test należy zaznaczyć 'Test', a jeżeli potrzebujesz"
                               " rozgrzewki wybierz opcję 'Wypróbuj'\n"
                               "Opcja 'Wypróbuj' nie będzie zliczała Twojego średniego wyniku,\n"
                               " ale pokaże Twoje pojedyncze wyniki\n" 
                               "Aby rozpocząć test należy wciśnąć przycisk główny('Rozpocznij)."
                               "W zależności od zaznaczonych opcji:\n\n"
                               "Test wizualny polega na kliknięciu na główny przycisk('Pomiar'), "
                               "gdy jego kolor zmieni się na zielony\n\n"
                               "Test dźwiękowy polega na wciśnięciu przycisku głównego('Pomiar'), "
                               "gdy usłyszymy sygnał dzwiękowy\n\n"
                               "Gdy zaznaczymy obie opcje testu, to należy wcisnąć przycisk wtedy, "
                               "gdy kolor przycisku jest zielony lub słyszymy sygnał dźwiękowy,"
                               " rodzaj testu będzie losowany\n\n"
                               "Po wykonaniu kilku pomiarów możemy zobaczyć nasze statysktyki "
                               "danego testu po naciśnięciu przycisku 'Statystyki' lub zobaczyć nasze wyniki "
                               "przedstawione na wyskresie ('Rysuj wykres') (w trybie 'Test')\n\n"
                               "Zmiana trybu testu (wizualny, dźwiękowy), powoduje utratę poprzednich pomiarów!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    # badam wartości zmiennym is_test is_acoustic aby poprawnie wybrać dany rodzaj testu
    def start_test(self):
        if self.is_visual and self.is_acoustic:
            if self.is_start_button_first_click:
                self.kind_of_test = random.randint(0, 1)  # losuje jeden z dwóch testów
            if self.kind_of_test == 0:
                self.visual_test()
            else:
                self.acoustic_test()
        elif self.is_visual:
            self.visual_test()
        elif self.is_acoustic:
            self.acoustic_test()
        else:
            print("Musisz wybrać rodzaj testu aby go rozpocząć!")

# metody do odczytywania kliknięć wykonanych przez użytkownika na GUI
    def test_clicked(self):
        self.is_test = self.test_radiobutton.isChecked()
        self.results = []

    def visual_clicked(self):
        self.is_visual = self.visual_checkbox.isChecked()
        self.results = []

    def acoustic_clicked(self):
        self.is_acoustic = self.acoustic_checkbox.isChecked()
        self.results = []

    # metoda do wyświetlania liczbowej reprezentacji wyników użytkownika
    def statystyki(self):
        if self.is_test and len(self.results) != 0:
            msg = QMessageBox(MainWindow)
            msg.setWindowTitle("Statystyki")
            msg.setText("Twój najlepszy wynik: " + f"{min(self.results):0.3f} s\n"
                        "Twój najsłabszy wynik: " + f"{max(self.results):0.3f} s\n"
                        "Twój średni czas reakcji: " + f"{sum(self.results)/len(self.results):0.3f} s\n")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        elif len(self.results) == 0:
            msg = QMessageBox(MainWindow)
            msg.setWindowTitle("Statystyki")
            msg.setText("Nie dokonano żadnego pomiaru!")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()
        else:
            msg = QMessageBox(MainWindow)
            msg.setWindowTitle("Statystyki")
            msg.setText("Jesteś w trybie 'Wypróbuj', aby korzystać ze statystyk musisz być w trybie test")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    # metoda do wyświetlania graficznej reprezentacji wyniku użytkownika
    def show_results(self):
        if self.is_test and len(self.results) > 1:
            x = np.arange(1, len(self.results)+1, 1)
            y_mean = sum(self.results)/len(self.results)
            y = []
            for i in range(0, len(self.results)):
                y.append(y_mean)
            plt.plot(x, self.results, x, y)
            plt.xlabel('Kolejne pomiary')
            plt.ylabel('Opóźnienie [ms]')
            plt.legend(['Wyniki pomiarów', 'Wartość średnia'])
            plt.show()
        elif not self.is_test:
            msg = QMessageBox(MainWindow)
            msg.setWindowTitle("Statystyki")
            msg.setText("Jesteś w trybie 'Wypróbuj', aby korzystać ze statystyk musisz być w trybie test")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else:
            msg = QMessageBox(MainWindow)
            msg.setWindowTitle("Rysowanie wykresu")
            if len(self.results) == 0:
                msg.setText("Nie dokonano żadnego pomiaru!")
            else:
                msg.setText("Dokonano tylko jednego pomiaru!")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    # metody do przeprowadzenia test wizualnego i akustycznego
    # dzielą się na dwie fazy:
    # pierwsze kliknięcie (is_start_button_first_click==True)
    # drugie kliknięcie (is_start_button_first_click==False)

    # po pierwszym kliknięciu przygotowujemy zmienne na drugie kliknięcie (set_env_after_first_click)
    # oraz losujemy przedział czasu z zakresu 2s - 8s, po których zostanie wykonana zmiana koloru / zagrany dźwięk

    # po drugim kliknięciu musimy się upewnić że użytkownik nie kliknął za szybko
    # gdy tak się stało to wykonujemy metodą clicked_too_fast, która resetuje program do stanu przed pierwszym
    # kliknięciem, więcej szczegółow w komentarzu do metody clicked_too_fast

    # gdy nie było falstartu to po drugim kliknięciu odczytujemy czas pomiędzy nadaniem sygnału a reakcją użytkownika
    # i resetujemy środowisko do stanu przed pierwszym kliknięciem
    def visual_test(self):
        if self.is_start_button_first_click:
            self.set_env_after_first_click('zielone światło')
            self.get_random_pause()
        elif not self.is_start_button_first_click and self.clicked_too_fast():
            self.set_env_after_second_click()
        else:
            self.get_reaction_time(self.green_color_appearance_time)
            self.set_env_after_second_click()

    def acoustic_test(self):
        if self.is_start_button_first_click:
            self.set_env_after_first_click('dźwięk')
            self.get_random_pause()
        elif not self.is_start_button_first_click and self.clicked_too_fast():
            self.set_env_after_second_click()
        else:
            self.get_reaction_time(self.sound_appearance_time)
            self.set_env_after_second_click()

# metody do zmiany właściwości przyciku/labela z automatyczną aktualizacją obiektu
    def change_button_color(self, button, color):
        button.setStyleSheet('background-color:' + color)
        button.repaint()

    def change_button_text(self, button, text):
        button.setText(text)
        button.repaint()

    # metoda dla odpowiedniego rodzaju testu wyświetla odpowiednie komunikaty
    def set_env_after_first_click(self, text):
        if self.is_visual and self.is_acoustic:
            self.change_button_text(self.start_button, 'Czekaj na ...!')
        else:
            self.change_button_text(self.start_button, 'Czekaj na ' + text + '!')
        self.change_button_color(self.start_button, 'red')
        self.is_start_button_first_click = False
        self.change_button_text(self.result_label, '')

    # metoda resetuje zmienne do stanu przed pierwszym kliknięciem, zeruje zmienne
    def set_env_after_second_click(self):
        self.change_button_color(self.start_button, 'white')
        self.change_button_text(self.start_button, 'Rozpocznij')
        self.kind_of_test = -1
        self.green_color_appearance_time = 0
        self.sound_appearance_time = 0
        self.is_start_button_first_click = True

    # metda wyliczająca czas reakcji użytkownika i dodająca wynik do listy wyników z danego testu
    def get_reaction_time(self, timestamp):
        reaction_time = time.perf_counter() - timestamp
        self.result_label.setText(str(reaction_time * 1000) + str(' ms'))
        self.results.append(reaction_time)

    # metoda służąca do wykonywania oczekiwania na nadanie sygnału (wizualnego/dźwiękowego) w osobnym wątku, przez co
    # w międzyczasie zapewnia użytkownikowi możliwość korzystania z GUI
    def get_random_pause(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        # w zależności od sygnału dostarczonego z obiektu klasy Worker() musimy odpowiednio:
        # dla przerwania wykonywania (poprzez falstart przy pomiarze czasu reakcji) musimy poinformować użytkownika o
        # tym że dokonał pomiaru przed sygnałem oraz zabić proces, który miał w określonym czasie ten sygnał nadać,
        # gdy proces skończył się naturalnie (nie został przerwany), to w zależności od rodzaju testu musimy albo nadać
        # sygnał dźwiękowy, albo akustyczny, albo losowy spośród nich oraz odpowiednio zaktualizować wygląd GUI

        self.worker.finished.connect(self.thread.quit)
        self.worker.interrupted.connect(
            lambda: self.change_button_color(self.start_button, 'white')
        )
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.worker.finished.connect(
            lambda: self.start_counter()
        )
        if self.is_visual and self.is_acoustic:
            rand_test = random.randint(0, 1)
            if rand_test == 0:
                self.worker.finished.connect(
                    lambda: self.change_button_color(self.start_button, 'green')
                )
            else:
                self.worker.finished.connect(
                    lambda: self.start_sound()
                )
        elif self.is_visual:
            self.worker.finished.connect(
                lambda: self.change_button_color(self.start_button, 'green')
            )
        elif self.is_acoustic:
            self.worker.finished.connect(
                lambda: self.start_sound()
            )

    # metoda zatrzymująca wątek, gdy użytkownik kliknie przycisk przed nadaniem sygnału
    # niestety powoduje zamrożenie GUI na czas zabicia wątku
    def stop_thread(self):
        self.change_button_text(self.start_button, 'Przycisk wciśnięty za szybko!')
        self.change_button_text(self.result_label, 'Daj mi chwilę, muszę zabić wątek')
        self.change_button_color(self.start_button, 'yellow')
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

    # metoda sprawdzajaca, czy użytkownik nie dokonuje pomiaru przed nadaniem sygnału
    # jeżeli tak, to zabija wątek, który ten sygnał miał nadać
    def clicked_too_fast(self):
        if not self.is_start_button_first_click and (self.sound_appearance_time == 0 or
                                                     self.green_color_appearance_time == 0):
            self.stop_thread()
            return True
        return False

    # zaczyna zliczać czas, gdy w osobnym wątku zostanie nadany sygnał
    def start_counter(self):
        self.green_color_appearance_time = time.perf_counter()
        self.sound_appearance_time = self.green_color_appearance_time

    # metoda nadająca sygnał dźwiękowy ( w tej wersji działa dla windowsa)
    def start_sound(self):
        winsound.Beep(500, 100)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    StatsWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
