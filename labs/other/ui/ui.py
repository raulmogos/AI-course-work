from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit


class UI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.__controller = controller
        self._problem_ea_params = {}
        #
        self.setGeometry(650, 150, 400, 400)
        self.setWindowTitle('lab3')
        self.__layout = QVBoxLayout(self)
        #
        label_title = QLabel('EVOLUTIONARY ALGORITHMS (EA)')
        label_title.setAlignment(Qt.AlignCenter)
        self.__layout.addWidget(label_title)
        self.__layout.addWidget(QLabel('probability of mutation:'))
        self.__text_probability_of_mutation = QLineEdit(self)
        self.__layout.addWidget(self.__text_probability_of_mutation)
        #
        self.__layout.addWidget(QLabel('probability of crossover:'))
        self.__text_probability_of_crossover = QLineEdit(self)
        self.__layout.addWidget(self.__text_probability_of_crossover)
        #
        self.__layout.addWidget(QLabel('individual size:'))
        self.__text_individual_size = QLineEdit(self)
        self.__layout.addWidget(self.__text_individual_size)
        #
        self.__layout.addWidget(QLabel('population size:'))
        self.__text_population_size = QLineEdit(self)
        self.__layout.addWidget(self.__text_population_size)
        #
        self.__layout.addWidget(QLabel('number of iterations:'))
        self.__text_iterations_number = QLineEdit(self)
        self.__layout.addWidget(self.__text_iterations_number)
        #
        self._button_run_ea_problem = QPushButton('Run EA Problem')
        self._button_run_ea_problem.clicked.connect(self.__run_ea)
        self.__layout.addWidget(self._button_run_ea_problem)
        #
        label_title_2 = QLabel('HILL CLIMBING (HC)')
        label_title_2.setAlignment(Qt.AlignCenter)
        self.__layout.addWidget(label_title_2)
        #
        self.__layout.addWidget(QLabel('matrix size:'))
        self.__text_point_size = QLineEdit(self)
        self.__layout.addWidget(self.__text_point_size)
        #
        self._button_run_hc_problem = QPushButton('Run HC Problem')
        self._button_run_hc_problem.clicked.connect(self.__run_hc)
        self.__layout.addWidget(self._button_run_hc_problem)

    def __run_problem_ea_thread(self, iterations_no):
        output = self.__controller.run_problem_ea(no_iterations=iterations_no)
        for key in output:
            print(f'{key}   ->    {output[key]}')
        if output['solution_found']:
            y = Thread(
                target=output['solution'].show,
                args=('solution global',),
                daemon=True
            )
            y.start()
        else:
            y = Thread(
                target=output['best_individual_so_far'].show,
                args=('best so far',),
                daemon=True
            )
            y.start()
        self._button_run_ea_problem.setEnabled(True)

    def __run_ea(self):
        p_mutation = self.__text_probability_of_mutation.text()
        p_crossover = self.__text_probability_of_crossover.text()
        individual_size = self.__text_individual_size.text()
        population_size = self.__text_population_size.text()
        iterations_no = self.__text_iterations_number.text()
        if not (p_mutation and p_crossover and individual_size and population_size and iterations_no):
            return
        self.__controller.set_problem_ea_params({
            'probability_of_mutation': float(p_mutation),
            'probability_of_crossover': float(p_crossover),
            'individual_size': int(individual_size),
            'population_size': int(population_size)
        })
        x = Thread(target=self.__run_problem_ea_thread, args=(int(iterations_no),), daemon=True)
        x.start()
        self._button_run_ea_problem.setEnabled(False)

    def __run_problem_hc_thread(self):
        output = self.__controller.run_problem_hc()
        for key in output:
            print(f'{key}   ->    {output[key]}')
        y = Thread(
            target=output['solution'].show,
            args=('best so far',),
            daemon=True
        )
        y.start()
        self._button_run_hc_problem.setEnabled(True)

    def __run_hc(self):
        point_size = self.__text_point_size.text()
        if not point_size:
            return
        self.__controller.set_problem_hc_params({
            'point_size': int(point_size),
        })
        x = Thread(target=self.__run_problem_hc_thread, daemon=True)
        x.start()
        self._button_run_hc_problem.setEnabled(False)
