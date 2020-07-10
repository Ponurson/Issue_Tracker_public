class Record(dict):

    def __init__(self, mic, date, problem, solution, name):

        self.date = date
        if problem == "":
            self.problem = "BRAK"
        else:
            self.problem = problem
        if solution == '':
            self.solution = "BRAK"
        else:
            self.solution = solution
        if name == '':
            self.name = "BRAK"
        else:
            self.name = name
        self.mic = mic
        self.id = None

