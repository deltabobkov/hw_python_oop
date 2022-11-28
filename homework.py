from dataclasses import dataclass
from typing import ClassVar, List, TypeVar
from typing_extensions import Final

T = TypeVar("T", int, float)


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE_TEXT = (
        "Тип тренировки: {0}; Длительность: {1:.3f} ч.; "
        "Дистанция: {2:.3f} км; Ср. скорость: {3:.3f} км/ч; "
        "Потрачено ккал: {4:.3f}."
    )
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Формирование сообщения о тренировке."""
        return self.MESSAGE_TEXT.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories,
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: Final = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_H: Final = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Указать get_spent_calories в %s." % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: Final = 18
    CALORIES_MEAN_SPEED_SHIFT: Final = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: Final = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: Final = 0.029
    CM_IN_M: Final = 100
    KMH_IN_MSEC: Final = 0.278

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий.

        Получение количества затраченных калорий при спортивной хотьбе.
        """
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + (
                (super().get_mean_speed() * self.KMH_IN_MSEC) ** 2
                / (self.height / self.CM_IN_M)
            )
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight
        ) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: Final = 1.1
    CALORIES_WEIGHT_MULTIPLIER: Final = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий.

        Получение количества затраченных калорий во время плавания.
        """
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[T]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_train_cls_map = {
        "RUN": Running,
        "WLK": SportsWalking,
        "SWM": Swimming,
    }
    try:
        if workout_type not in workout_type_train_cls_map.keys():
            raise ValueError()
    except ValueError:
        print("Ошибка ввода типа тренировки")
    return workout_type_train_cls_map[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
