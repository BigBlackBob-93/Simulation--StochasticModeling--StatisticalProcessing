import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QPushButton,
    QDoubleSpinBox
)
from random import random
from objects import obj
from constants import number_of_events

spin_boxes: list[QDoubleSpinBox] = obj.objects.get('spinbox')
buttons: list[QPushButton] = obj.objects.get('button')


def start():
    trails = spin_boxes[-1].value()  # N
    intervals: list[float] = get_intervals()
    frequencies: list[int] = [0 for k in range(number_of_events)]  # n
    relative_frequencies: list[int] = []  # empirical probabilities: p^ = n/N

    for i in range(trails):
        frequencies[define_interval(intervals, random())] += 1

    for frequency in frequencies:
        relative_frequencies.append(frequency / trails)

    draw_bar(relative_frequencies)


def define_expected_probabilities(expected_probabilities: list[float]):
    count: float = 0
    for i in range(len(expected_probabilities)):
        count += spin_boxes[i].value()
        if count > 1:
            spin_boxes[i].setValue(0)
        else:
            expected_probabilities[i] = spin_boxes[i].value()

    if sum(expected_probabilities) < 1:
        expected_probabilities[-1] += 1 - sum(expected_probabilities)
        spin_boxes[number_of_events - 1].setValue(expected_probabilities[-1])


def get_intervals() -> list[float]:
    expected_probabilities: list[float] = [0.0 for k in range(number_of_events)]
    define_expected_probabilities(expected_probabilities)
    for i in range(1, len(expected_probabilities)):
        expected_probabilities[i] += expected_probabilities[i - 1]
    return expected_probabilities


def define_interval(intervals: list[float], alpha: float) -> int:
    if alpha <= intervals[0]:
        return 0
    for j in range(1, len(intervals)):
        if (alpha <= intervals[j]) and (alpha > intervals[j - 1]):
            return j
    return len(intervals) - 1


def draw_bar(relative_frequencies: list[int]) -> None:
    courses = [f"{i}" for i in range(1, len(relative_frequencies) + 1)]
    values = relative_frequencies
    plt.bar(courses, values)
    plt.xlabel("Events")
    plt.ylabel("Frequencies")
    plt.show()


buttons[0].clicked.connect(start)
