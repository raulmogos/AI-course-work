from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


DEFAULT_PARAMS_UI = {
    'swarm_size': 3,
    'particle_size': 40,
    'iterations_number': 100,
    'inertia_coefficient': 1,
    'cognitive_learning_coefficient': 1,
    'social_learning_coefficient': 1,
    'step_1': 0.6,
    'step_2': 0.9,
}


class UI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.__controller = controller

        self.setGeometry(650, 150, 400, 400)
        self.setWindowTitle('lab3')
        self.__layout = QVBoxLayout(self)
        #
        label_title = QLabel('PARTICLE SWARM OPTIMISATION')
        label_title.setAlignment(Qt.AlignCenter)
        self.__layout.addWidget(label_title)
        #
        self.__layout.addWidget(QLabel('particle size:'))
        self.__text_particle_size = QLineEdit(str(DEFAULT_PARAMS_UI['swarm_size']), self)
        self.__layout.addWidget(self.__text_particle_size)
        #
        self.__layout.addWidget(QLabel('swarm size:'))
        self.__text_swam_size = QLineEdit(str(DEFAULT_PARAMS_UI['particle_size']), self)
        self.__layout.addWidget(self.__text_swam_size)
        #
        self.__layout.addWidget(QLabel('iterations number:'))
        self.__text_iterations_number = QLineEdit(str(DEFAULT_PARAMS_UI['iterations_number']), self)
        self.__layout.addWidget(self.__text_iterations_number)
        #
        self.__layout.addWidget(QLabel('inertia coefficient:'))
        self.__text_inertia_coefficient = QLineEdit(str(DEFAULT_PARAMS_UI['inertia_coefficient']), self)
        self.__layout.addWidget(self.__text_inertia_coefficient)
        #
        self.__layout.addWidget(QLabel('cognitive learning coefficient:'))
        self.__text_cognitive_learning_coefficient = QLineEdit(
            str(DEFAULT_PARAMS_UI['cognitive_learning_coefficient']), self
        )
        self.__layout.addWidget(self.__text_cognitive_learning_coefficient)
        #
        self.__layout.addWidget(QLabel('social learning coefficient:'))
        self.__text_social_learning_coefficient = QLineEdit(str(DEFAULT_PARAMS_UI['social_learning_coefficient']), self)
        self.__layout.addWidget(self.__text_social_learning_coefficient)
        #
        self.__button_run_pso_problem = QPushButton('Run PSO Problem')
        self.__button_run_pso_problem.clicked.connect(self.__run_pso)
        self.__layout.addWidget(self.__button_run_pso_problem)

    def __run_pso(self):
        swarm_size = self.__text_swam_size.text()
        particle_size = self.__text_particle_size.text()
        inertia_coefficient = self.__text_inertia_coefficient.text()
        cognitive_learning_coefficient = self.__text_cognitive_learning_coefficient.text()
        social_learning_coefficient = self.__text_social_learning_coefficient.text()
        iterations_number = self.__text_iterations_number.text()
        if not (swarm_size and particle_size and inertia_coefficient and cognitive_learning_coefficient
                and social_learning_coefficient and iterations_number):
            return
        self.__controller.set_problem_params({
            'swarm_size': int(swarm_size),
            'particle_size': int(particle_size),
            'inertia_coefficient': float(inertia_coefficient),
            'cognitive_learning_coefficient': float(cognitive_learning_coefficient),
            'social_learning_coefficient': float(social_learning_coefficient),
        })
        x = Thread(target=self.__thread_run_pso, args=(int(iterations_number),), daemon=True)
        x.start()
        self.__button_run_pso_problem.setEnabled(False)

    def __thread_run_pso(self, iterations_number):
        output = self.__controller.run_pso(iterations_number)
        for key in output.keys():
            print(f'{key}    ->    {output[key]}')
        y = Thread(target=output['solution'].show, daemon=True)
        y.start()
        self.__button_run_pso_problem.setEnabled(True)


