from dataclasses import dataclass


@dataclass
class Resolution:
    horizontal_pixels_count: int = 0
    vertical_pixels_count: int = 0
    horizontal_position: int = 0
    vertical_position: int = 0
