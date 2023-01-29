# player class
class Player:
    def __init__(self, name, color, markers):
        self.name = name
        self.color = color
        self.markers = markers[:3]
        self.score = 0

    def add_marker(self, marker):
        if len(self.markers) < 3:
            self.markers.append(marker)
            return True
        return False

    def remove_marker(self, marker):
        self.markers.remove(marker)