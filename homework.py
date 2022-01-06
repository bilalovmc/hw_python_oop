class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        if self.duration > 0:
            """преодоленная_дистанция_за_тренировку / время_тренировки"""
            speed = self.get_distance() / self.duration
            return speed
        else:
            return 0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        """определяются в подклассах"""
        return 0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info = InfoMessage(self, self.duration, distance, speed, calories)
        return info


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def __str__(self):
        return 'Running'

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration_min = self.duration * 60
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        calori_running = ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                          * self.weight / super().M_IN_KM * duration_min)
        return calori_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def __str__(self):
        return 'SportsWalking'

    def get_spent_calories(self) -> float:
        mean_speed = super().get_mean_speed()
        duration_min = self.duration * 60
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 2
        coeff_calorie_3 = 0.029
        if self.height > 0:
            calori_running = ((coeff_calorie_1 * self.weight
                              + (mean_speed**coeff_calorie_2 // self.height)
                              * coeff_calorie_3 * self.weight) * duration_min)
            return calori_running
        else:
            return 0


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def __str__(self):
        return 'Swimming'

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        """длина_бассейна * count_pool / M_IN_KM / время_тренировки"""
        speed = (self.length_pool * self.count_pool
                 / super().M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        """(средняя_скорость + 1.1) * 2 * вес"""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        calori_running = ((mean_speed + coeff_calorie_1)
                          * coeff_calorie_2 * self.weight)
        return calori_running


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    action = data[0]
    duration = data[1]
    weight = data[2]

    if workout_type == 'SWM':
        length_pool = data[3]
        count_pool = data[4]
        return Swimming(action, duration, weight, length_pool, count_pool)
    elif workout_type == 'RUN':
        return Running(action, duration, weight)
    elif workout_type == 'WLK':
        height = data[3]
        return SportsWalking(action, duration, weight, height)
    else:
        return Training(action, duration, weight)


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
