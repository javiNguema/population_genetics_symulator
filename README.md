# population_genetics_symulator
This program simulates the growth of a population and tracks the evolution of genetic traits over time. The assumptions guiding this simulation are as follows:

1. The universe (development space of turtles) is confined.
2. The movement of turtles follows two rules based on their reproductive state: if fertile, the turtle seeks a mate for mating, otherwise, the turtle's movement is random in all directions.
3. The genotype of offspring from two parents follows Mendelian inheritance laws.
4. There is no environmental variance effect, nor considerations for genetic-environmental effects; only genetic effects are considered.
5. The initial generation consists of a 'purebred line', signifying that the starting population is homozygous.


EXECUTION INSTRUCTIONS:

For non-developers:

1. Download the GenEvol.rar file.
2. Extract the file GenEvol.exe (for winOS users) from the downloaded package.
3. Run GenEvol.exe, and you're all set!

For Python developers:

Python version requirement: 3.10 or higher.

Steps to follow:

1. Install the required modules listed in the requirements.txt file.
   - This can be done manually by installing each module individually.
   - Alternatively, you can install all the required modules using the following command in the shell terminal:

      ```
      python -m pip install -r requirements.txt
      ```

2. Download the code files: TurtlesModel.py and TurlesView.py.
3. Place both files in the same folder (directory).
4. Run the TurtlesView.py file.

That's it! If you need further assistance, feel free to ask.
