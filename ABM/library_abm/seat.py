from mesa import Agent

class Seat(Agent):
    """
    A Seat agent that can be occupied by a student.
    It doesn't move but exists in the environment to be interacted with.
    """
    def __init__(self, unique_id, model, seat_type):
        super().__init__(unique_id, model)
        self.seat_type = seat_type  # The preference category: 'quiet', 'window', 'charging', 'normal'
        self.occupied = False
