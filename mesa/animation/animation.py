import time


class Animation:
    def __init__(self) -> None:
        self.val_list: list[AnimVal] = []

    def update(self):
        for value in self.val_list:
            value.update()


class AnimVal:
    def __init__(self, handler, value) -> None:
        handler.val_list.append(self)
        self.value = value
        self.start_value = value
        self.begin = time.time()
        self.current = time.time()
        self.begin_movement = False
        self.next_target_value = None
        self.anim_duration = 0
        self.value_diff = None
        self.animation_curve = None

    def is_moving(self):
        """Checks if the animation value has not reached its endpoints."""
        return self.begin_movement

    def perform(self):
        if self.next_target_value == None:
            return
        if self.current >= self.anim_duration:
            self.begin_movement = False
        if self.animation_curve:
            anim_pos = self.animation_curve(self.current / (self.anim_duration))
            self.value = self.start_value + anim_pos * self.value_diff
        else:
            self.value = -1

    def move_to(self, target_value, duration, curve):
        self.begin = time.time()
        self.begin_movement = True
        self.start_value = self.value
        self.next_target_value = target_value

        self.anim_duration = duration
        self.animation_curve = curve
        self.value_diff = target_value - self.value

    def update(self):
        if self.begin_movement:
            self.current = (time.time() - self.begin) * 100

            self.perform()
