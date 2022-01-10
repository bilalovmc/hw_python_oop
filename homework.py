from dataclasses import dataclass
from typing import Any


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: Any
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        if self.duration > 0:
            return self.get_distance() / self.duration
        return 0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите run в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self, self.duration, distance, speed, calories)


@dataclass
class Running(Training):
    """Тренировка: бег."""
    action: int
    duration: float
    weight: float

    def __str__(self):
        return 'Running'

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration_min = self.duration * 60
        mean_speed_coeff_1 = 18
        mean_speed_coeff_2 = 20
        return ((mean_speed_coeff_1 * mean_speed - mean_speed_coeff_2)
                * self.weight / super().M_IN_KM * duration_min)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: int

    def __str__(self):
        return 'SportsWalking'

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration_min = self.duration * 60
        weight_coeff_1 = 0.035
        mean_speed_coeff_1 = 2
        mean_speed_coeff_2 = 0.029
        if self.height > 0:
            return ((weight_coeff_1 * self.weight
                    + (mean_speed**mean_speed_coeff_1 // self.height)
                    * mean_speed_coeff_2 * self.weight) * duration_min)
        return 0


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    def __str__(self):
        return 'Swimming'

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / super().M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        mean_speed_coeff_1 = 1.1
        mean_speed_coeff_2 = 2
        return ((mean_speed + mean_speed_coeff_1)
                * mean_speed_coeff_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    return {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }.get(workout_type, Training)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
