
from string import ascii_letters
from random import randint, choices, seed, choice
import time
from typing import Any, Tuple, Dict, List
import random
import customtkinter as ctk
import math
seed(time.time())



VIEW_FWIDTH = 765
VIEW_FHEIGHT = 765
TURTLE_SIZE = 10
LIFE = 100
MAX_DISTANCE_FOR_BIRTH = 20
ENV_SPACE_WIDTH = 600
ENV_SPACE_HEIGH = 600
INITIAL_STATE_AVG_ENERGY = 10


class TurtlesData(dict):
    def __init__(self, **kwargs) -> None:
        """Turtle is a dict-like data structure that takes argumets rlifespan, fenotype and genotype and create an individual with the specified traits
        each time we instantiate the object, we get a specific object with a specific ID. We can access the id by calling the method id_inspect or 
        using the notation to call an attribute.
        Args:
            rlifespan (int, optional): is the remaining life span that the turle has. Defaults to None.
            fenotype (str, optional): is the (color) appearence that the turtle displays. Defaults to None.
            genotype (str, optional): is the coding gene of the displayed fenotype (color). Defaults to None.
        """
        super(TurtlesData, self).__init__(**kwargs)
        self.ID = ''.join(([str(randint(10000, 99999))]) + (choices(ascii_letters, k =3)))
        self.sex = choice(['F', 'M'])
        # self.energy = INITIAL_STATE_AVG_ENERGY + random.randint(0, 9)
        
        
    def __getattr__(self, key) -> Any:
        if key in self:
            return self[key]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    def __setattr__(self, key, value):
        self[key] = value
        
        

class Inheritance:
    def __init__(self, turtle) -> None:
        self.turtle = turtle
        self.turtle.genotype = random.choice(['AA', 'aa'])

    @classmethod
    def segregation(cls, genotype1, genotype2, cache=None, count =0):
        genotype1 = list(genotype1)
        genotype2 = list(genotype2)
        if cache is None:
            cache = []
        if len(genotype1) == 0:
            return cache
        candidate = genotype1[0]
        for allele in genotype2:
            cache.append(candidate+allele)
        genotype1.pop(0)
        count +=1
        return cls.segregation(genotype1=''.join(genotype1), genotype2=''.join(genotype2), cache =cache, count=count)

    @classmethod
    def homozigous_parents(cls, parent1, parent2) -> str:
        genotype1 = parent1.genotype
        genotype2 = parent2.genotype
        candidates_genotypes =  Inheritance.segregation(genotype1=genotype1, genotype2=genotype2)
        offspring = random.choice(candidates_genotypes)
        return offspring
    


class TurtleBlueprint(TurtlesData):
    def __init__(self, frame: ctk.CTkFrame):
        super().__init__()
        x_lim, y_lim = ENV_SPACE_WIDTH - TURTLE_SIZE, ENV_SPACE_HEIGH - TURTLE_SIZE
        x_loc = random.randint(0, x_lim)
        y_loc = random.randint(0, y_lim)
        self.turtle_btn = ctk.CTkButton(frame, text=f'', hover=False, border_color='yellow', border_spacing=0, border_width=0,
                                        width=TURTLE_SIZE, height=TURTLE_SIZE, corner_radius=50, font=('Arial', 12), 
                                        fg_color='yellow')
        
        self.turtle_btn._set_scaling(1.0, 1.0)
        self.turtle_btn.place(x=x_loc, y=y_loc)
        
    def get_data(self, lifespan:int=15, genotype:str=None, fenotype: str=None, fertility_period: int=None, fertility_state:str = 'fertile', maturity_age: int=None, maturity_state:bool = 'mature') -> Dict:
        self.turtle_btn.update()
        x, y = self.turtle_btn.winfo_x(), self.turtle_btn.winfo_y()
        key_variables = ['location', 'lifespan', 'genotype', 'fenotype', 'fertility_period', 'fertility_state', 'maturity_age', 'maturity_state']
        age_gap = 4
        turtle_age = randint(a=lifespan, b=lifespan + age_gap)

        value_data = [(x, y),  turtle_age, genotype, Inheritance(turtle=self), fertility_period, fertility_state, maturity_age, maturity_state]
        for key, value in zip(key_variables, value_data):
            self.setdefault(key, value)
        return self
    
    @classmethod
    def random_step(cls, turtle) -> Tuple[str, Tuple[int, int]]:
        coor_move = {'west': (-1, 0),
                     'east': (1, 0),
                     'north': (0, 1),
                     'south': (0, -1),
                     'northwest': (-1, 1),
                     'northeast': (1, 1),
                     'southeast': (1, -1),
                     'southwest': (-1, -1)
                     }
        x_cloc, y_cloc = turtle.location
        new_step = random.choice(list(coor_move.items()))
        cardinals, (x_rloc, y_rloc) = new_step
        new_xloc = max(0, min(ENV_SPACE_WIDTH- TURTLE_SIZE, round(x_cloc + 10 * random.random() * x_rloc, ndigits=2)))
        new_yloc = max(0, min(ENV_SPACE_HEIGH - TURTLE_SIZE, round(y_cloc + 10 * random.random() * y_rloc, ndigits=2)))
        turtle.turtle_btn.place(x=new_xloc, y=new_yloc)
        turtle.location = (new_xloc, new_yloc)

    
    MALE = Dict
    FEMALE = Dict
    DISTANCE = Any

    @classmethod
    def inspect_closest_neighbour(cls, turtle_instance: Dict, all_turtles: list) -> Tuple[MALE, FEMALE, DISTANCE]:
        potential_partners = []
        male = None 
        female = None
        dist = None

        if len(all_turtles) <= 1:
            return None
        
        candidate_sex = ['M', 'F']
        candidate_sex.remove(turtle_instance.sex)

        mating_candidates = filter(lambda candidate: candidate if candidate.sex == candidate_sex[0] else None, all_turtles)
        x1, y1 = turtle_instance.location

        for turtle in mating_candidates:
            x2, y2 = turtle.location
            d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            potential_partners.append((turtle, d)) # a tuple with the canditates and distances to the instance


        if not potential_partners:
            return None
        partner, dist = min(potential_partners, key=lambda item: item[1]) # tuple with nearest candidate

        if candidate_sex[0] == 'F':
            female, male = partner, turtle_instance

        elif candidate_sex[0] == 'M':
            male, female = partner, turtle_instance

        return male, female, dist
            
    @classmethod
    def search_for_mates(cls, turtle_instance: Dict, all_turtles: List[Dict]):
        close_neigbors = TurtleBlueprint.inspect_closest_neighbour(turtle_instance=turtle_instance, all_turtles=all_turtles)

        if close_neigbors  is None:
            return
        
        male, female, dist = close_neigbors 

        if 'fertile' not in (female.fertility_state, male.fertility_state) and not 'mature' in (female.maturity_state, male.maturity_state):
            return None
        
        x1, y1 = male.location
        x2, y2 = female.location 
        if x1 > x2:
            x1 -= 10 * random.random()
            x2 += 10 * random.random()
        if x1 <x2:
            x1 += 10 * random.random()
            x2 -= 10 * random.random()
        if y1 > y2:
            y1 -= 10 * random.random()
            y2 += 10 * random.random()
        if y1 <y2:
            y1 += 10 * random.random()
            y2 -= 10 * random.random()
            
        male.turtle_btn.place_configure(x = x1, y= y1)
        female.turtle_btn.place_configure(x = x2, y= y2)
        male.location = (round(x1, ndigits=2), round(y1, ndigits=2))
        female.location = (round(x2, ndigits=2), round(y2, ndigits=2))
    
    @classmethod
    def search_for_food(self, turtle_instance: Dict, all_turtles: List[Dict]):
        ...


    @classmethod
    def give_birth(cls, parents:Tuple[MALE, FEMALE, DISTANCE], 
                   environment:ctk.CTkFrame, 
                   lifespan:int, 
                   birth_chances: float, 
                   fertility_period: int, 
                   maturity_age: int
                   ) -> Any:

        male, female, dist = parents

        birth_coeff = random.gauss(mu = 0.50, sigma=0.05)
        if (dist <= MAX_DISTANCE_FOR_BIRTH) \
            and (float(male.lifespan) > 0) \
            and (float(female.lifespan) > 0) \
            and (birth_coeff <= birth_chances) \
            and (int(male.fertility_period) == fertility_period) \
            and (int(female.fertility_period) == fertility_period) \
            and (int(male.maturity_age) == maturity_age) \
            and (int(female.maturity_age) == maturity_age):
                
                
            x_loc, y_loc = female.location
            new_born = cls(environment)

            new_born.location = female.location
            new_born.lifespan = lifespan

            new_born_genotype = Inheritance.homozigous_parents(parent1=male, parent2=female)
            new_born.genotype = new_born_genotype
            new_born.fenotype = 'None'
            new_born.fertility_period = fertility_period
            new_born.maturity_age = 0
            new_born.maturity_state = 'immature'
            new_born.fertility_state = 'infertile'

            male.fertility_period = 0
            female.fertility_period = 0
            male.fertility_state = 'infertile'
            female.fertility_state = 'infertile'

            new_born.turtle_btn.place_configure(x = x_loc, y = y_loc)
            new_born.turtle_btn.configure(fg_color = 'green')

            return new_born
    
    @classmethod
    def die(cls, turtle, all_turtles, death_turtles, genotypes):
        death_turtles.add(turtle.ID)
        turtle.turtle_btn.destroy()
        all_turtles.remove(turtle)
        if turtle.genotype == 'Aa' or turtle.genotype == 'aA':
            genotypes['Aa'].pop(0)
        else:
            genotypes[turtle.genotype].pop(0)



