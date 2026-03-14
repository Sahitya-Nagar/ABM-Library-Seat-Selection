import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from seat import Seat
from student_agent import StudentAgent

# Reporter functions for DataCollector

def get_total_entered(model):
    """Returns the total number of students who entered the library."""
    return model.metrics["total_entered"]

def get_seated(model):
    """Returns the total number of students currently seated."""
    return model.metrics["seated"]

def get_rejected(model):
    """Returns the total number of students who left because they couldn't find a seat."""
    return model.metrics["rejected"]

def get_avg_satisfaction(model):
    """Calculates the average satisfaction of currently seated students."""
    students = [a for a in model.schedule.agents if isinstance(a, StudentAgent) and a.seated]
    if not students:
        return 0
    total_score = sum(student.satisfaction_score for student in students)
    return total_score / len(students)

def get_utilization(model):
    """Calculates the percentage of seats currently occupied."""
    seats = [a for a in model.schedule.agents if isinstance(a, Seat)]
    if not seats:
        return 0
    occupied = sum(1 for seat in seats if seat.occupied)
    # Utilization as a percentage 0-100
    return (occupied / len(seats)) * 100

class LibraryModel(Model):
    """
    # Library Seat Selection Agent-Based Model

    An Agent-Based Model simulating how students choose seats in a university library based on preferences and availability.

    ## How it Works
    * **Students (Green Circles)** arrive at the library entrance (top-left) with a predetermined seat preference (quiet, window, charging, or normal) and a random study duration.
    * **Seats (Colored Squares)** are randomly scattered around the library based on your slider settings.
        * **Blue Square:** Quiet Seat
        * **Cyan Square:** Window Seat
        * **Orange Square:** Charging Seat
        * **Grey Square:** Normal Seat
    * When a student occupies a seat, it turns **Red** and displays an **"S"**.
    * If a student cannot find their preferred seat, they will settle for any available seat (temporarily lowering their satisfaction score). 
    * If the library is at 100% capacity, students are turned away (increasing the Rejected graph line).

    ## How to Test and Break the Model
    By default, the library rarely reaches 100% capacity because students leave their seats just as fast as new ones arrive.
    
    If you want to see the **Rejected graph spike**:
    1. Check the left sidebar sliders. Wait for the simulation to tick a few times.
    2. Set **Students per step** up to maximum (`10`).
    3. Set **Total Capacity** down to minimum (`50`).
    4. Click the **Reset** button at the top right, then click **Start**. 
    5. The library will hit 100% bounds almost instantly and rejections will skyrocket!
    """
    
    def __init__(self, width=20, height=20,
                 students_per_step=2,
                 num_quiet=30,
                 num_charging=25,
                 total_capacity=144):
        super().__init__()
        if total_capacity > width * height:
            total_capacity = width * height

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0

        # User defined parameters
        self.students_per_step = students_per_step
        self.num_quiet = num_quiet
        self.num_charging = num_charging
        self.total_capacity = total_capacity

        # System metrics
        self.metrics = {
            "total_entered": 0,
            "seated": 0,
            "rejected": 0
        }
        
        # Generate the library layout with seats
        self.create_library_layout()
        
        # DataCollector for collecting metrics at each tick
        self.datacollector = DataCollector(
            model_reporters={
                "Total Entered": get_total_entered,
                "Seated": get_seated,
                "Rejected": get_rejected,
                "Average Satisfaction": get_avg_satisfaction,
                "Seat Utilization (%)": get_utilization
            }
        )
        self.running = True
        
    def next_id(self):
        """Generates unique IDs for agents."""
        self.current_id += 1
        return self.current_id

    def create_library_layout(self):
        """
        Creates a structured library floor plan with 4 distinct seat zones,
        organised desk clusters, and clear walking corridors.

        Layout (y=0 is bottom / entrance, y=19 is top):
          - x=0          : Left entrance corridor (always empty)
          - y=0          : Bottom entrance row (always empty)
          - x=10, y=10   : Central cross-shaped corridor (always empty)
          - y=19 / x=19  : Window seats along top wall and right wall
          - x=1-9, y=12-18 : QUIET zone (top-left quadrant)
          - x=11-17, y=12-18: CHARGING zone (top-right quadrant)
          - x=1-17, y=1-8  : REGULAR seats (bottom half, both sides)
        """
        seat_assignments = {}  # (x, y) -> seat_type

        # ------------------------------------------------------------------
        # WINDOW seats: top wall (y=19) and right wall (x=19)
        # ------------------------------------------------------------------
        for x in list(range(1, 10)) + list(range(11, 19)):
            seat_assignments[(x, 19)] = 'window'      # top row
        for y in list(range(1, 10)) + list(range(11, 19)):
            seat_assignments[(19, y)] = 'window'      # right column

        # ------------------------------------------------------------------
        # QUIET seats: top-left quadrant, organised desk clusters
        # Rows y=12,13 | aisle y=14 | rows y=15,16 | aisle y=17 | row y=18
        # Columns x=1,2 | aisle x=3 | x=4,5 | aisle x=6 | x=7,8
        # ------------------------------------------------------------------
        quiet_ys = [12, 13, 15, 16, 18]
        quiet_xs = [1, 2, 4, 5, 7, 8]
        all_quiet = [(x, y) for y in quiet_ys for x in quiet_xs]
        # Honour the num_quiet slider (max 30)
        num_quiet = max(0, min(self.num_quiet, len(all_quiet)))
        chosen_quiet = self.random.sample(all_quiet, num_quiet) if num_quiet < len(all_quiet) else all_quiet # type: ignore
        for pos in chosen_quiet:
            seat_assignments[pos] = 'quiet'

        # ------------------------------------------------------------------
        # CHARGING seats: top-right quadrant, same cluster pattern
        # Columns x=11,12 | aisle x=13 | x=14,15 | aisle x=16 | x=17
        # ------------------------------------------------------------------
        charging_xs = [11, 12, 14, 15, 17]
        all_charging = [(x, y) for y in quiet_ys for x in charging_xs]
        # Honour the num_charging slider (max 25)
        num_charging = max(0, min(self.num_charging, len(all_charging)))
        chosen_charging = self.random.sample(all_charging, num_charging) if num_charging < len(all_charging) else all_charging # type: ignore
        for pos in chosen_charging:
            seat_assignments[pos] = 'charging'

        # ------------------------------------------------------------------
        # REGULAR seats: bottom half (y=1-8, both left and right sides)
        # Rows y=2,3 | aisle y=4 | y=5,6 | aisle y=7 | y=8
        # ------------------------------------------------------------------
        regular_ys = [2, 3, 5, 6, 8]
        for y in regular_ys:
            for x in quiet_xs:       # left side
                seat_assignments[(x, y)] = 'normal'
            for x in charging_xs:    # right side
                seat_assignments[(x, y)] = 'normal'

        # Always keep entrance and corridors clear
        for pos in [(0, 0), (10, 10)]:
            seat_assignments.pop(pos, None)

        # Honour total_capacity limit (sample if layout exceeds it)
        all_seats = list(seat_assignments.items())
        if self.total_capacity < len(all_seats):
            all_seats = self.random.sample(all_seats, self.total_capacity) # type: ignore

        for (x, y), seat_type in all_seats:
            seat = Seat(self.next_id(), self, seat_type)
            self.schedule.add(seat)
            self.grid.place_agent(seat, (x, y))

    def step(self):
        """Advance the model by one step."""
        # Spawn new students arriving at the entrance
        for _ in range(self.students_per_step):
            # Assign random preference to student
            preference = self.random.choice(['quiet', 'window', 'charging', 'normal']) # type: ignore
            study_time = self.random.randint(10, 50) # type: ignore
            
            student = StudentAgent(self.next_id(), self, preference, study_time)
            self.schedule.add(student)
            
            # Place at entrance (0, 0)
            self.grid.place_agent(student, (0, 0))
            self.metrics["total_entered"] += 1
            
        # Step all agents
        self.schedule.step()
        
        # Collect data at the end of the step
        self.datacollector.collect(self)
