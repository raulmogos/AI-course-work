
class UI:
    def __init__(self, controller):
        self.__controller = controller

    def run(self):
        while True:
            print('MENU:')
            print('\t0 - exit')
            print('\t1 - train')
            print('\t2 - decision tree')
            print('\t3 - test')
            try:
                ans = int(input(' >> '))
                if ans == 0:
                    return
                elif ans == 1:
                    self.__controller.run_train()
                elif ans == 2:
                    self.__controller.get_tree().to_string()
                elif ans == 3:
                    self.__controller.run_tests()
            except Exception as e:
                print(e)
