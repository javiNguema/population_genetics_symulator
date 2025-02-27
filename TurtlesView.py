import customtkinter as ctk
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import numpy.typing as npt
from typing import Dict, Tuple, List
import tkinter as tk
import functools
from TurtlesModel import TurtleBlueprint
import random
import time

text_font = 'Arial', 15
SETTING_FWIDTH = 200
VIEW_FWIDTH = 765
VIEW_FHEIGHT = 765
UPER_MARGIN = 5
SIDE_MARGIN = 0.1
ENV_SPACE_WIDTH = 600
ENV_SPACE_HEIGH = 600
RESOURCE_SIZE = 10
POP_DENSITY = 1.5


class TurtleInfo(ctk.CTkToplevel):
    def __init__(self, data):
        """This is a toplevel that displays turtles information.
        Args:
            data (Dict): This is the data of the turtle that are going to be displayed once we click
            over the turtle.
        """
        super().__init__()
        self.title(f'turtle id {data.ID}')
        self.geometry('300x380')
        self.resizable(width=False, height=False)

        frames = []
        for i in range(2):
            frame = ctk.CTkFrame(self)
            if i == 1:
                frame.pack_configure(side = 'left', pady = 5, padx = 40, anchor='e')
                frames.append(frame)
            else:
                frame.pack_configure(side = 'left', pady = 5, padx = 10, anchor='w')
                frames.append(frame)
        
        lbl_frame, info_frame = frames
        for lbl, info in data.items():
            if lbl == 'turtle_btn':
                continue
            if lbl != 'location':
                ctk.CTkLabel(lbl_frame, font = ('Arial', 15), text= lbl).pack_configure(side = 'top', anchor='w', pady = 5, padx=5)
                ctk.CTkLabel(info_frame, font = ('Arial', 15), text= info).pack_configure(side = 'top', anchor='w', pady = 5, padx=5)
            else:
                ctk.CTkLabel(lbl_frame, font = ('Arial', 15), text= lbl).pack_configure(side = 'top', anchor='w', pady = 5, padx=5)
                ctk.CTkLabel(info_frame, font = ('Arial', 15), text= f'x: {info[0]}, y: {info[1]}').pack_configure(side = 'top', anchor='w', pady = 5, padx=5)
                
        self.attributes('-topmost', 'true') # ensure the toplevel to stay on top of all windows 
        


class EvolutionFigure:
    def __init__(self, frame) -> None:
        f_width = 7.8
        f_height = 10

        self.f = Figure(figsize=(f_width, f_height), dpi=100)
        self.f.subplots_adjust(hspace=0.2, wspace=0, bottom=0.13, top=0.95, right=0.95)


        self.fig = self.f.subplots(nrows =2, ncols=1)

        self.pop_evol_line, = self.fig[0].plot([], [], 'g-', lw=1, label = 'alive')
        self.pop_death, = self.fig[0].plot([], [], 'r-', lw=1, label= 'dead')
        self.fig[0].legend()
        self.fig[0].set_xlabel('time (ticks)')
        self.fig[0].set_ylabel('turtles population (individuals)')
        

        self.aa_freq, = self.fig[1].plot([], [], 'g-', lw=1, label = 'aa')
        self.Aa_freq, = self.fig[1].plot([], [], 'b-', lw=1, label= 'Ab')
        self.AA_freq, = self.fig[1].plot([], [], 'r-', lw=1, label= 'AA')

        self.fig[1].legend()
        self.fig[1].set_xlabel('time (ticks)')
        self.fig[1].set_ylabel('genotype frequency')



        # self.f2 = Figure(figsize=(f_width, f_height), dpi=100)
        # self.f2.subplots_adjust(hspace=0, wspace=0, bottom = 0.13, top=0.95, right=0.95)
        
        # self.fig_genotype = self.f2.add_subplot(111)
        # self.aa_freq, = self.fig_genotype.plot([], [], 'k--', lw=2, label = 'aa')
        # self.Aa_freq, = self.fig_genotype.plot([], [], 'k^-', lw=2, label = 'Aa')
        # self.AA_freq, = self.fig_genotype.plot([], [], 'ko-', lw=2, label = 'AA')
        # self.f2.legend()

        # self.fig.set_ylabel('Population of Turtles')
        # self.fig_genotype.set_xlabel('Ticks')
        # self.fig_genotype.set_ylabel('genotype frequency')
        
        self.canvas_1 = FigureCanvasTkAgg(self.f, frame)
        self.canvas_1.get_tk_widget().pack(side = 'top', fill = 'both')

        self.canvas_2 = FigureCanvasTkAgg(self.f, frame)
        self.canvas_2.get_tk_widget().pack(side = 'top', fill = 'both')

    

    def population_evolution(self, ticks: int, turtle_count: int, accumulated_turtles:npt.NDArray, death_count:int, accumulated_deaths:npt.NDArray) -> Tuple[npt.NDArray, npt.NDArray]:
        """draws the evolution of the population in the simulation, plots both the living and dead turtles.

        Args:
            ticks (int): time coordinates of the evolution plot (in ticks)
            turtle_count (int): is the number of living turtles in the simulation at each tick.
            accumulated_turtles (npt.NDArray): accumulates the values of number of living turtles for each tick
            death_count (int): is the number of dead turtles in the simulation at each tick.
            accumulated_deaths (npt.NDArray): accumulates the values of number of death turtles for each tick

        Returns:
            Tuple[npt.NDArray, npt.NDArray, npt.NDArray]: tuple containing acummulated dead turtles, and accumulates living turtles
        """
        accumulated_turtles = np.append(accumulated_turtles, turtle_count)
        accumulated_deaths = np.append(accumulated_deaths, death_count)
        
        x_data = np.arange(ticks+1)
        self.pop_evol_line.set_data(x_data, accumulated_turtles)
        self.pop_death.set_data(x_data, accumulated_deaths)
        
        
        max_death = max(accumulated_deaths)
        max_alive = max(accumulated_turtles) 
        
        self.fig[0].set_xlim(0, ticks + SIDE_MARGIN)
        self.fig[0].set_ylim(0, max(1, max([max_death, max_alive]) + UPER_MARGIN))
        self.canvas_1.draw()
        

        return accumulated_turtles, accumulated_deaths
    
    def population_genetics(self, ticks:int, all_turtles:List, genotypes:Dict, cummulative_genotypes:Tuple[npt.NDArray, npt.NDArray, npt.NDArray]) -> Tuple[npt.NDArray, npt.NDArray, npt.NDArray]:
        """Draws the evolution plots of the frequency of genotypes in the living population.

        Args:
            ticks (int): time coordinates of the evolution plot (in ticks)
            all_turtles (List): _description_
            genotypes (Dict): contain all the genotyopes organized in key-value structure so AA: [AA, AA, AA, ...], Aa: [Aa, Aa, Aa, ...]...
            cummulative_genotypes (Tuple[npt.NDArray, npt.NDArray, npt.NDArray]): contains three arrays, each containing the ammount of the three genotypes along the time (ticks)

        Returns:
            Tuple[npt.NDArray, npt.NDArray, npt.NDArray]: tuple containing acummulated genotypes.
        """
        

        cummulative_aa, cummulative_Aa, cummulative_AA = cummulative_genotypes
    
        cummulative_count_aa = round(len(genotypes['aa'])/len(all_turtles), 4)
        cummulative_count_Aa = round(len(genotypes['Aa'])/len(all_turtles), 4)
        cummulative_count_AA = round(len(genotypes['AA'])/len(all_turtles), 4)
        
        cummulative_aa = np.append(cummulative_aa, cummulative_count_aa)
        cummulative_Aa = np.append(cummulative_Aa, cummulative_count_Aa)
        cummulative_AA = np.append(cummulative_AA, cummulative_count_AA)
        
        self.fig[1].set_xlim(0, ticks + SIDE_MARGIN)
        self.fig[1].set_ylim(0, 1.2)


        x_data = np.arange(ticks+1)
        self.aa_freq.set_data(x_data, cummulative_aa)
        self.Aa_freq.set_data(x_data, cummulative_Aa)
        self.AA_freq.set_data(x_data, cummulative_AA)
        
        self.canvas_2.draw()
        
        cummulative_genotypes_updated = (cummulative_aa, cummulative_Aa, cummulative_AA)
        return cummulative_genotypes_updated
    
    def energy_bar_life(self, turtle):
        if turtle.energy_life != 0:
            turtle.energy_life -=1



class Universe(ctk.CTk): # environment where the tortles evolve
    is_initialized = False
    is_evolving = False
    def __init__(self, frame_size: str= '1520x660', simulation_time: int =20, n_turtles: int= 1) -> None:
        super().__init__()
        self.geometry(frame_size)
        self.resizable(width = False, height=False)
        self.title('Inheritance laws symulator')
        self.simulation_time = simulation_time
        self.n_turtles = n_turtles
        self.ui()
        self.plot = EvolutionFigure(frame = self.plotting_frame)

    def ui(self) -> None: #user interface function
        self.frames = []
        for i in range(3):
            if i == 0:
                width = SETTING_FWIDTH
            else:
                width = VIEW_FWIDTH

            # create all the main frames of the interface, indcluding, button holder, ecosystem holder and plot holder
            frame = ctk.CTkFrame(self, width = width, height=VIEW_FHEIGHT, #fg_color='grey70', 
                                 )
            frame._set_scaling(1.0, 1.0) # change scaling factor to 1.0 to keep VIEW_FHEIGHT and VIEW_FWIDTH size
            frame.pack_configure(side = 'left', padx = 5, anchor = 'nw')
            self.frames.append(frame)
            
        settings_frame = self.frames[0]
        self.cfbuttons = {'initialize': (..., self._initialize_universe),
                          'start': (..., self.start_simulation),
                          'stop': (..., self.stop_simulation),
                          'pause': (..., self.pause_simulation),
                          'resume': (..., self.resume_simulation),
                          }
        
        # setting the button widgets 
        
        for name, (_, callback) in self.cfbuttons.items():
            btn_widget = ctk.CTkButton(master = settings_frame, width = 255, text = name, font=text_font)
            btn_widget.pack_configure(side = 'top', pady = 5, padx = 3, anchor = 'w', fill='x')
            btn_widget.bind('<Button-1>', callback)
            self.cfbuttons[name] = (btn_widget, callback)
            
        sliders = {'lifespan':(..., self._set_lifespan),
                   'symulation speed':(..., self._set_simulation_speed),
                   'birth rate':(..., self._set_birth_rate),
                   'population size': (..., self._set_population_size),
                   'fertility period': (..., self._set_fertility_period),
                   'maturity age': (..., self._set_maturity_age)
                   }
        self.lbl_slider_values = []

        # setting labels and slides widgets

        for lbl, (_, callback) in sliders.items():
            
            lbl_widget = ctk.CTkLabel(settings_frame, text= lbl, font=text_font)
            lbl_widget.pack_configure(side = 'top', anchor='w', pady = 5, padx = 3)
            
            frame_sldr = ctk.CTkFrame(settings_frame)
            frame_sldr.pack_configure(side = 'top', pady = 5, padx = 3, anchor = 'w')
            
            if lbl == 'lifespan':
                slider_widget = ctk.CTkSlider(frame_sldr, from_ = 0, to =100, number_of_steps=100, command= callback)
                slider_widget.set(output_value=30) # default state of slider lifespan
            elif lbl == 'population size':
                slider_widget = ctk.CTkSlider(frame_sldr, from_ = 0, to =300, number_of_steps=300, command= callback)
                slider_widget.set(output_value=12) # default state of slider population size
            elif lbl == 'fertility period':
                slider_widget = ctk.CTkSlider(frame_sldr, from_ = 0, to =20, number_of_steps=20, command= callback)
                slider_widget.set(output_value=10)
            elif lbl == 'maturity age':
                slider_widget = ctk.CTkSlider(frame_sldr, from_ = 0, to =20, number_of_steps=20, command= callback)
                slider_widget.set(output_value=18)
            elif lbl == 'symulation speed':
                slider_widget = ctk.CTkSlider(frame_sldr, from_ = 0, to =0.1, number_of_steps=10000, command= callback)
                slider_widget.set(output_value=18)
            else:
                slider_widget = ctk.CTkSlider(frame_sldr, from_ = 0, to =1, number_of_steps=1000, command= callback)

            slider_widget.pack_configure(side = 'left', padx = 5)
            sliders[lbl] = (slider_widget, callback)
            
            if lbl == 'population size' or lbl == 'lifespan':
                lbl_slider_value = ctk.CTkLabel(frame_sldr, text= f'{int(slider_widget.get())}', font=text_font)
            else:
                lbl_slider_value = ctk.CTkLabel(frame_sldr, text= f'{slider_widget.get()}', font=text_font)
            
            lbl_slider_value.pack_configure(side = 'left', anchor='e', padx = 3)
            self.lbl_slider_values.append(lbl_slider_value)
        
        self.lifespan_lbl, self.simulation_speed_lbl,\
            self.birth_rate_lbl, self.population_size_lbl,\
                self.fertility_period_lbl, self.maturity_age = self.lbl_slider_values
    
        self.environment = self.frames[1]
        self.environment.configure(fg_color = 'black', width =ENV_SPACE_WIDTH, height = ENV_SPACE_HEIGH)


        # set the resources in the system
        
        self.plotting_frame = self.frames[2]
        
    
    def stop_simulation(self, event=None):
        self.STOP = True
        
    def pause_simulation(self, event = None):
        self.RESUME = False
        self.PAUSE = True
        
    def resume_simulation(self, event = None):
        self.RESUME = True
        self.PAUSE = False
        if  self.is_evolving or not self.is_initialized:
            return
        if not self.STOP:
            self.is_evolving = True
            self.continue_run_evolve()
            self.is_evolving = False
        self.run_evolve(all_turtles=self.all_turtles)
        
        

    def _show_turtle_info(self, event:tk.Event=None) -> None:
        btn_triggered = str(event.widget)
        btn_triggered = '.'.join(btn_triggered.split('.')[0:-1])
        for turtle in self.all_turtles:
            match tuple(turtle.items()):
                case id_, sex, (_, widget), *_:
                    if str(widget) == btn_triggered:
                        TurtleInfo(data = turtle)
                        
    def _set_lifespan(self, event=None) -> None:
        self.lifespan_lbl.configure(text= f'{int(event)}')

    
    def _set_simulation_speed(self, event=None) -> None:
        self.simulation_speed_lbl.configure(text= f'{round(float(event), 5)}')

        
    def _set_birth_rate(self, event=None) -> None:
        self.birth_rate_lbl.configure(text= f'{round(float(event), 5)}')

    
    def _set_population_size(self, event=None) -> None:
        self.population_size_lbl.configure(text = f'{int(event)}')
        
    
    def _set_fertility_period(self, event = None) -> None:
        self.fertility_period_lbl.configure(text = f'{int(event)}')
        
    def _set_maturity_age(self, event = None) -> None:
        self.maturity_age.configure(text = f'{int(event)}')
        
    
    def _initialize_universe(self, event=None):

        if self.is_evolving:
            return
        self.PAUSE = False
        self.STOP = False
        self.is_initialized = True
        self.simulation_time = 200 # we have to create a widget to be able to tweak this parameter
        

        for child in self.environment.winfo_children():
            child.place_forget()
            
        lifespan_value, sim_speed_value, birth_rate_value, population_size_value, fertility_period, maturity_age = [item._text for item in self.lbl_slider_values]
        self.all_turtles = []
        self.genotypes = {'aa': [], 
                          'Aa': [], 
                          'AA': []
                          }
        
        for _ in range(int(population_size_value)):
            myturtle = TurtleBlueprint(frame = self.environment)
            myturtle.turtle_btn.bind("<Button-1>", self._show_turtle_info)
            self.all_turtles.append(myturtle.get_data(lifespan=int(lifespan_value), fertility_period=float(fertility_period), maturity_age=float(maturity_age)))

        self.run_evolve = functools.partial(self._run_evolve,
                                            lifespan_value = float(lifespan_value),
                                            birth_rate_value = float(birth_rate_value),
                                            sim_speed_value = float(sim_speed_value),
                                            fertility_period = float(fertility_period), 
                                            maturity_age = float(maturity_age), 
                                            )   # apply the sliders constant parameters

        for turtle in self.all_turtles:
            if turtle.genotype == 'aa':
                self.genotypes['aa'].append(turtle.genotype)
            elif turtle.genotype == 'Aa' or turtle.genotype == 'aA':
                self.genotypes['Aa'].append(turtle.genotype)
            elif turtle.genotype == 'AA':
                self.genotypes['AA'].append(turtle.genotype)
                
                
        self.plot.population_genetics(ticks=0,
                                      all_turtles=self.all_turtles,
                                      genotypes=self.genotypes,
                                      cummulative_genotypes = (np.zeros(0), np.zeros(0), np.zeros(0))
                                      )
        
        self.plot.population_evolution(ticks=0,
                            turtle_count=len(self.all_turtles),
                            accumulated_turtles=np.zeros(0),
                            death_count=0,
                            accumulated_deaths=np.zeros(0))
        
        # resources = Resources(frame = self.environment, number_agents=int(population_size_value))

    def _run_evolve(self,
                    lifespan_value: int,
                    birth_rate_value: float,
                    sim_speed_value: int,
                    fertility_period: int,
                    maturity_age: int,
                    all_turtles: list,
                    death_turtles: set=None,
                    ticks: int = None,
                    accumulated_turtles: list = None,
                    accumulated_deaths: list = None,
                    genotypes:Dict = None,
                    cummulative_genotypes: Tuple= None
                    ):
        

        while self.simulation_time:
            if ticks is None:
                ticks = 0
            if accumulated_turtles is None:
                accumulated_turtles = np.zeros(ticks)
            if accumulated_deaths is None:
                accumulated_deaths = np.zeros(ticks)
            if cummulative_genotypes is None:
                cummulative_genotypes = (np.zeros(ticks), np.zeros(ticks), np.zeros(ticks))
            if genotypes is None:
                genotypes = self.genotypes
            if death_turtles is None:
                death_turtles = set()
        
            if not all_turtles:
                return
            
            if self.PAUSE == True:
                    self.continue_run_evolve = functools.partial(self._run_evolve,
                                                lifespan_value=lifespan_value,
                                                birth_rate_value=birth_rate_value,
                                                sim_speed_value=sim_speed_value,
                                                fertility_period=fertility_period, 
                                                maturity_age=maturity_age,
                                                all_turtles=all_turtles, 
                                                death_turtles=death_turtles,
                                                ticks=ticks,
                                                accumulated_turtles=accumulated_turtles,
                                                accumulated_deaths=accumulated_deaths,
                                                genotypes=genotypes, 
                                                cummulative_genotypes=cummulative_genotypes)
                    return
                
            if self.STOP == True:
                return
            
            all_turtles_update = all_turtles.copy()
            
            cummulative_genotypes = self.plot.population_genetics(ticks, all_turtles_update, genotypes, cummulative_genotypes)
            accumulated_turtles, accumulated_deaths = self.plot.population_evolution(ticks=ticks,
                                                                turtle_count=len(all_turtles_update),
                                                                accumulated_turtles=accumulated_turtles,
                                                                death_count=len(death_turtles),
                                                                accumulated_deaths=accumulated_deaths)
            
            nturtles = len(all_turtles_update)
            n = 0
            while nturtles:
                new_born = None
                turtle = all_turtles_update[n]
                
                closest_neighbors = TurtleBlueprint.inspect_closest_neighbour(turtle_instance=turtle, all_turtles=all_turtles_update)
                if closest_neighbors is not None:
                    new_born = TurtleBlueprint.give_birth(parents=closest_neighbors,
                                                        environment=self.environment,
                                                        lifespan=lifespan_value,
                                                        birth_chances=birth_rate_value,
                                                        fertility_period=fertility_period,
                                                        maturity_age=maturity_age)
                if new_born is not None:
                    new_born.turtle_btn.bind('<Button-1>', self._show_turtle_info)
                    all_turtles.append(new_born)
                    if new_born.genotype == 'aA' or  new_born.genotype == 'Aa':
                        genotypes['Aa'].append('Aa')
                    elif new_born.genotype == 'aa':
                        genotypes['aa'].append('aa')
                    elif new_born.genotype == 'AA':
                        genotypes['AA'].append('AA')
                        
                    
                if turtle.maturity_state == 'mature' and turtle.fertility_state == 'fertile':
                    TurtleBlueprint.search_for_mates(turtle, all_turtles)
                else:
                    TurtleBlueprint.random_step(turtle)


                turtle.lifespan -= 1 if turtle.lifespan != 0 else 0
                if  0 <= turtle.fertility_period < fertility_period:
                    turtle.fertility_period +=1
                else:
                    turtle.fertility_period = fertility_period
                    turtle.fertility_state = 'fertile'        # if fertility is at it max then the turtle is fertile
                                                            # anyware bellow the fertility_period, is infertile.
                
                if turtle.maturity_age < maturity_age:
                    turtle.maturity_age +=1 
                else:
                    turtle.maturity_age = maturity_age
                    turtle.maturity_state = 'mature'
                    turtle.turtle_btn.configure(fg_color = 'yellow')
                    
                turtle.turtle_btn.update()
                
                if (turtle.lifespan == 0):
                    TurtleBlueprint.die(turtle, all_turtles, death_turtles, genotypes)

                n +=1
                nturtles -=1

            time.sleep(0.1 - sim_speed_value)
            self.simulation_time -=1
            ticks +=1

    
    def start_simulation(self, event=None):
        if self.STOP:
            return
        if  self.is_evolving or not self.is_initialized: # if is evolving already or is not initialized already, then we do not evolve
            return
        self.is_evolving = True
        self.run_evolve(all_turtles=self.all_turtles)
        self.is_evolving = False
    


class Resources:
    def __init__(self, frame, number_agents, density = None):
        self.frame = frame
        
        if density is None:
            density = POP_DENSITY
        self.population_size = int(density*number_agents)
        self.populate()
    
    def sprout(self):
        ...

    def populate(self):
        for i in range(self.population_size):
            resource = ctk.CTkButton(master = self.frame, text='', width = 5, height= 8, border_width=0, border_spacing=0, fg_color='green')
            resource.place(x=random.randint(1, ENV_SPACE_WIDTH), y =random.randint(1, ENV_SPACE_HEIGH))

    


if __name__ == '__main__':
    myuniverse = Universe(n_turtles=10, simulation_time=100)
    myuniverse.mainloop()