# from environment import Street, WORLD_WIDTH, WORLD_LENGTH
# from bike import Bike

# import curses
# import time

# import numpy as np



# class Engine():

#     def __init__(self):

#         self.graph_matrix = self.create_graph_matrix()

#     def create_graph_matrix(self):

#         self.graph_matrix = np.zeros((WORLD_WIDTH, WORLD_LENGTH))

#     def generate_graph_matrix(self, bike_graph_matrix, env_graph_matrix):

#         return np.add(env_graph_matrix, bike_graph_matrix)




# def display_street(engine_graph_matrix, last_key_pressed):
#     """progress: 0-10"""

#     stdscr.addstr(0, 0, f"last key pressed: {last_key_pressed}")

#     for i in range(len(engine_graph_matrix)):
#         this_str = "".join(["#" if item == 1 else 'X' if item == 100 else " " if item == 0 else "🔥" for item in engine_graph_matrix[i].tolist()[0]])
#         # print(this_str)
#         # print("###")
#         # print(f"{i}")
#         stdscr.addstr(i+1, 0, this_str)
        

#     # stdscr.addstr(0, 0, "Moving file: {0}".format(filename))
#     # stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(progress * 10, "#" * progress))
#     stdscr.refresh()


# if __name__ == "__main__":

#     street = Street()
#     engine = Engine()
#     bike = Bike()

#     stdscr = curses.initscr()
#     stdscr.nodelay(1)
#     curses.noecho()
#     curses.cbreak()
#     last_key_pressed = ""

#     try:
#         for i in range(400):

#             street.update_street()
#             bike.update_bike(last_key_pressed)
#             engine_graph_matrix = engine.generate_graph_matrix(
#                 bike_graph_matrix=bike.create_graph_matrix(),
#                 env_graph_matrix=street.get_graph_matrix
#             )
            
#             display_street(engine_graph_matrix=engine_graph_matrix, last_key_pressed=last_key_pressed)
#             last_key_pressed = stdscr.getch()
#             time.sleep(0.05)
#     finally:
#         curses.echo()
#         curses.nocbreak()
#         curses.endwin()