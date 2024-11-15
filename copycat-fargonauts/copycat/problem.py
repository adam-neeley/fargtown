from .copycat import Copycat

from pprint import pprint

class Problem:
    def __init__(self, initial, modified, target, iterations, distributions=None, formulas=None):
        self.formulas = formulas
        if formulas is not None:
            assert hasattr(Copycat(), 'temperature')
        else:
            if hasattr(Copycat(), 'temperature'):
                self.formulas = set(Copycat().temperature.adj_formulas())
        print(self.formulas)
        self.initial  = initial
        self.modified = modified
        self.target   = target

        self.iterations    = iterations
        if distributions is None:
            self.distributions = self.solve()
        else:
            self.distributions = distributions
        print(self.formulas)

    def test(self, comparison, expected=None):
        print('-' * 120)
        print('Testing copycat problem: {} : {} :: {} : _'.format(self.initial,
                                                                  self.modified,
                                                                  self.target))
        print('expected:')
        if expected is None:
            expected = self.distributions
        pprint(expected)

        actual = self.solve()
        print('actual:')
        pprint(actual)
        comparison(actual, expected)
        print('-' * 120)

    def solve(self):
        print('-' * 120)
        print('Testing copycat problem: {} : {} :: {} : _'.format(self.initial,
                                                                  self.modified,
                                                                  self.target))
        copycat = Copycat()
        answers  = dict()
        if self.formulas == None:
            if hasattr(copycat, 'temperature'):
                formula = copycat.temperature.getAdj()
            else:
                formula = None
            answers[formula] = copycat.run(self.initial,
                                self.modified,
                                self.target,
                                self.iterations)
        else:
            print(self.formulas)
            for formula in self.formulas:
                copycat.temperature.useAdj(formula)
                answers[formula] = copycat.run(self.initial,
                                        self.modified,
                                        self.target,
                                        self.iterations)
                print('Done with {}'.format(formula))
        return answers

    def generate(self):
        self.distributions = self.solve()
