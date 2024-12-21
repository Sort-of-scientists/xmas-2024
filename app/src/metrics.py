import numpy as np

from .entities import Provider
from typing import List


def compute_expected_processing_time(chain: List[Provider]) -> float:
    probas, values = [], []

    for k in range(len(chain)):
        multiplication = np.prod([1 - provider.conversion for provider in chain[:k]])

        probas.append(multiplication * chain[k].conversion)

        values.append(np.sum([provider.processing_time for provider in chain[:k + 1]]))

    probas, values = np.array(probas), np.array(values)

    return probas.dot(values)


def compute_expected_conversion(chain: List[Provider]) -> float:
    return 1 - np.prod([1 - provider.conversion for provider in chain])


def compute_expected_commission(chain: List[Provider]) -> float:
    probas, values = [], []

    for k in range(len(chain)):
        multiplication = np.prod([1 - provider.conversion for provider in chain[:k]])

        probas.append(multiplication * chain[k].conversion)
        values.append(chain[k].commission)

    probas, values = np.array(probas), np.array(values)

    return probas.dot(values)