import PySimpleGUI as sg
import maze

# --------------------------- GUI Setup & Create Window -------------------------------

sg.theme('LightGrey1')

algorithm_dict = {'Binary Tree': 'binary tree',
                  'Aldous-Broder': 'aldous broder',
                  'Wilson': 'wilson',
                  'Recursive Backtracking': 'recursive backtracking',
                  'Hunt and Kill': 'hunt and kill',
                  'Prims': 'prim',
                  'Kruskal': 'kruskal'}

animation_speed_dict = {'Very Slow': 0.4,
                        'Slow': 0.2,
                        'Medium': 0.1,
                        'Fast': 0.02,
                        'Very Fast': 0.005}

grid_size_dict = {'Small': 8,
                  'Medium': 16,
                  'Large': 25}


right_col = [[sg.T('Algorithm')],
            [sg.Listbox(list(algorithm_dict), default_values=[list(algorithm_dict)[0]], size=(20, 7), key='LB-Algo')]]


left_col = [[sg.T('Animation Speed')],
            [sg.Listbox(list(reversed(animation_speed_dict)), default_values=[list(animation_speed_dict)[4]], size=(10, 4), key='LB-Speed')],
            [sg.T('Grid Size')],
            [sg.Listbox(list(grid_size_dict), default_values=[list(grid_size_dict)[0]], size=(10, 3), key='LB-GridSize')]]

gui_buttons = [[sg.Button('Create Maze')],
                [sg.Exit()]]

layout = [[sg.Titlebar('MazeMaker')],
          [sg.T(' '*10), sg.T('Select Maze Parameters', font=18, justification = 'center')],
          [sg.Column(left_col, element_justification = 'center'), sg.Column(right_col, element_justification = 'center', vertical_alignment = 'top')],
          [sg.Column(gui_buttons, element_justification = 'right', justification = 'right')]]

window = sg.Window('MazeMaker', layout)


# # ------------------------ Integrates PyGame and Graph Element to Embed into single window------------------
# graph = window[]           # type: sg.Graph
# embed = graph.TKCanvas
# os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# os.environ['SDL_VIDEODRIVER'] = 'windib'


def main():

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Create Maze':
            algo = algorithm_dict.get(values['LB-Algo'][0], list(algorithm_dict.values())[0])
            speed = animation_speed_dict.get(values['LB-Speed'][0], list(animation_speed_dict.values())[0])
            size = grid_size_dict.get(values['LB-GridSize'][0], list(grid_size_dict.values())[0])

            maze.run(algo, speed, size)

    window.close()

if __name__ == "__main__":
    main()
