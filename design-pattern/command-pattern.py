"""
식당으로 비유하면, 
Command Interface -> menu
Concrete Command -> Dish order
Receiver -> Kitchen staff
Waiter -> Invoker

Receiver 에 필요한 로직을 담고, 로직의 조합을 Command에 넣은 후
Client 에서 객체 생성 후 invoke 를 통해서 넣어줌
Invoker는 Command 호출 외 필요한 작업을 수행
"""

from abc import ABC, abstractmethodㄹ
from typing import List


# Command Interface
class Command(ABC):
    """
    Command Class Interface
    """

    @abstractmethod
    def execute(self):
        pass


class LightOnCommand(Command):

    def __init__(self, light):
        self.light: Light = light  # Client에서 Receiver를 주입받음

    def execute(self):
        self.light.turn_on()


class LightOffCommand(Command):
    def __init__(self, light):
        self.light: Light = light

    def execute(self):
        self.light.turn_off()


# Receiver, 실제 Logic을 포함하고 있음
class Light:

    def __init__(self):
        self.status = False

    def turn_on(self):
        if not self.status:
            print("Light is ON")
            self.status = True

    def turn_off(self):
        if self.status:
            print("Light is OFF")
            self.status = False


# Invoker
# command를 실행시켜주고, history 나 로깅 등 의 기능을 사용할 수 있음
class LightController:

    def __init__(self):
        self.history: List[str] = []

    def execute(self, command):
        command.execute()
        self.history.append(command)


def main():
    # client에서 receiver 객체 생성
    light = Light()

    com_light_on = LightOnCommand(light=light)
    com_light_off = LightOffCommand(light=light)

    # Create Invoker
    # 하나의 invoker에서 필요한 command를 받아서 수행해주는 느낌
    invoker = LightController()
    invoker.execute(com_light_on)
    invoker.execute(com_light_off)


if __name__ == "__main__":
    main()
