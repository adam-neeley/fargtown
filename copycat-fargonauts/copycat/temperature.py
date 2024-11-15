import math

# Alternate formulas for getAdjustedProbability

def _original(temp, prob):
    if prob == 0 or prob == 0.5 or temp == 0:
        return prob
    if prob < 0.5:
        return 1.0 - _original(temp, 1.0 - prob)
    coldness = 100.0 - temp
    a = math.sqrt(coldness)
    c = (10 - a) / 100
    f = (c + 1) * prob
    return max(f, 0.5)

def _entropy(temp, prob):
    if prob == 0 or prob == 0.5 or temp == 0:
        return prob
    if prob < 0.5:
        return 1.0 - _original(temp, 1.0 - prob)
    coldness = 100.0 - temp
    a = math.sqrt(coldness)
    c = (10 - a) / 100
    f = (c + 1) * prob
    return -f * math.log2(f)

def _weighted(temp, s, u):
    weighted = (temp / 100) * s + ((100 - temp) / 100) * u 
    return weighted

def _weighted_inverse(temp, prob):
    iprob = 1 - prob
    return _weighted(temp, iprob, prob)

def _fifty_converge(temp, prob): # Uses .5 instead of 1-prob
    return _weighted(temp, .5, prob)

def _soft_curve(temp, prob): # Curves to the average of the (1-p) and .5
    return min(1, _weighted(temp, (1.5-prob)/2, prob))

def _weighted_soft_curve(temp, prob): # Curves to the weighted average of the (1-p) and .5
    weight = 100
    gamma  = .5  # convergance value
    alpha  = 1   # gamma weight
    beta   = 3   # iprob weight
    curved = min(1, (temp / weight) * ((alpha * gamma + beta * (1 - prob)) / (alpha + beta)) + ((weight - temp) / weight) * prob)
    return curved

def _alt_fifty(temp, prob):
    s = .5
    u = prob ** 2 if prob < .5 else math.sqrt(prob)
    return _weighted(temp, s, u)

def _averaged_alt(temp, prob):
    s = (1.5 - prob)/2
    u = prob ** 2 if prob < .5 else math.sqrt(prob)
    return _weighted(temp, s, u)


def _working_best(temp, prob):
    s = .5   # convergence
    r = 1.05 # power
    u = prob ** r if prob < .5 else prob ** (1/r)
    return _weighted(temp, s, u)

def _soft_best(temp, prob):
    s = .5   # convergence
    r = 1.05 # power
    u = prob ** r if prob < .5 else prob ** (1/r)
    return _weighted(temp, s, u)

def _parameterized_best(temp, prob):
    # (D$66/100)*($E$64*$B68 + $G$64*$F$64)/($E$64 + $G$64)+((100-D$66)/100)*IF($B68 > 0.5, $B68^(1/$H$64), $B68^$H$64)
    # (T/100) * (alpha * p + beta * .5) / (alpha + beta) + ((100 - T)/100) * IF(p > .5, p^(1/2), p^2)
    alpha = 5
    beta  = 1
    s     = .5
    s     = (alpha * prob + beta * s) / (alpha + beta)
    r     = 1.05
    u = prob ** r if prob < .5 else prob ** (1/r)
    return _weighted(temp, s, u)

def _meta(temp, prob):
    r = _weighted(temp, 1, 2) # Make r a function of temperature
    s = .5
    u = prob ** r if prob < .5 else prob ** (1/r)
    return _weighted(temp, s, u)

def _meta_parameterized(temp, prob):
    r = _weighted(temp, 1, 2) # Make r a function of temperature

    alpha = 5
    beta  = 1
    s     = .5
    s     = (alpha * prob + beta * s) / (alpha + beta)
    u = prob ** r if prob < .5 else prob ** (1/r)

    return _weighted(temp, s, u)

def _none(temp, prob):
    return prob

class Temperature(object):
    def __init__(self):
        self.reset()
        self.adjustmentType = 'inverse'
        self._adjustmentFormulas = {
                'original'       : _original,
                'entropy'        : _entropy,
                'inverse'        : _weighted_inverse,
                'fifty_converge' : _fifty_converge,
                'soft'           : _soft_curve,
                'weighted_soft'  : _weighted_soft_curve,
                'alt_fifty'      : _alt_fifty,
                'average_alt'    : _averaged_alt,
                'best'           : _working_best,
                'sbest'          : _soft_best,
                'pbest'          : _parameterized_best,
                'meta'           : _meta,
                'pmeta'          : _meta_parameterized,
                'none'           : _none}
        self.diffs  = 0
        self.ndiffs = 0

    def reset(self):
        self.history = [100.0]
        self.actual_value = 100.0
        self.last_unclamped_value = 100.0
        self.clamped = True
        self.clampTime = 30

    def update(self, value):
        self.last_unclamped_value = value
        if self.clamped:
            self.actual_value = 100.0
        else:
            self.history.append(value)
            self.actual_value = value

    def clampUntil(self, when):
        self.clamped = True
        self.clampTime = when
        # but do not modify self.actual_value until someone calls update()

    def tryUnclamp(self, currentTime):
        if self.clamped and currentTime >= self.clampTime:
            self.clamped = False

    def value(self):
        return 100.0 if self.clamped else self.actual_value

    def getAdjustedValue(self, value):
        return value ** (((100.0 - self.value()) / 30.0) + 0.5)

    def getAdjustedProbability(self, value):
        temp = self.value()
        prob = value
        adjusted = self._adjustmentFormulas[self.adjustmentType](temp, prob)

        self.diffs  += abs(adjusted - prob)
        self.ndiffs += 1
        return adjusted

    def getAverageDifference(self):
        return self.diffs / self.ndiffs

    def useAdj(self, adj):
        print('Changing to adjustment formula {}'.format(adj))
        self.adjustmentType = adj

    def getAdj(self):
        return self.adjustmentType

    def adj_formulas(self):
        return self._adjustmentFormulas.keys()
