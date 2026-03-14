import random
from mesa import Agent
from seat import Seat

class StudentAgent(Agent):
    """
    A Student agent that enters the library and searches for a seat
    matching their preference.
    """
    def __init__(self, unique_id, model, preference_type, study_time):
        super().__init__(unique_id, model)
        self.preference_type = preference_type
        self.study_time = study_time
        
        self.seated = False
        self.satisfaction_score = 0

    def step(self):
        """
        The agent's action at each time step.
        """
        # If the student is already seated, they just study
        if self.seated:
            self.study_time -= 1
            if self.study_time <= 0:
                self.leave_seat()
            return

        # If the student is not seated, they search for a seat
        self.search_and_occupy_seat()

    def search_and_occupy_seat(self):
        """
        Student looks for an available seat. 
        Prioritizes the preferred seat type.
        """
        # Find all seats in the simulation
        all_agents = self.model.schedule.agents
        empty_seats = [a for a in all_agents if isinstance(a, Seat) and not a.occupied]

        # If no seats are available, the student is rejected and leaves
        if not empty_seats:
            self.model.metrics["rejected"] += 1
            
            # Remove agent from the grid and the schedule to exit the simulation
            if self.pos is not None:
                self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.seated = False # Just to be safe
            return

        # Look for seats that match preference
        preferred_seats = [s for s in empty_seats if s.seat_type == self.preference_type]

        if len(preferred_seats) > 0:
            # Pick a random preferred seat
            chosen_seat = self.random.choice(preferred_seats)
            self.satisfaction_score = 100
        else:
            # Pick any random available seat if preferred is not found
            chosen_seat = self.random.choice(empty_seats)
            self.satisfaction_score = 50

        # Occupy the seat
        chosen_seat.occupied = True
        self.seated = True
        self.model.metrics["seated"] += 1
        
        # Move visually to the seat directly
        self.model.grid.move_agent(self, chosen_seat.pos)

    def leave_seat(self):
        """
        The student finishes studying, vacates the seat, and leaves the library.
        """
        # Find the seat at the current grid position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, Seat):
                agent.occupied = False
                break
                
        # Remove agent from grid and schedule
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
