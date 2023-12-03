
class CubeSubset:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
    
    def parse(subset_line: str):
        def peek_l(x):
            print(x, type(x), type(x[0]), type(x[1]))
            return x

        color_lines = subset_line.split(',')
        color_lines = map(lambda x: x.strip(), color_lines)
        word_number_lines = map(lambda x: x.split(' '), color_lines)
        color_numbers = map(lambda x: (x[1], int(x[0])), word_number_lines)

        colors = {'red': 0, 'green': 0, 'blue': 0}
        for (color, number) in color_numbers:
            colors[color] = number
        return CubeSubset(**colors)

    def __repr__(self):
        return f'{{{self.red}, {self.green}, {self.blue}}}'

class Game:
    def __init__(self, id, cube_subsets):
        self.cube_subsets = cube_subsets
        self.id = id

    def parse(game_line: str):
        game_id_line, set_line = game_line.split(":")

        game_id_line = game_id_line.strip()
        set_line = set_line.strip()

        game_id = int(game_id_line.split(' ')[1])

        subset_lines = map(lambda x: x.strip(''), set_line.split(';'))
        subsets = list(map(lambda line: CubeSubset.parse(line), subset_lines))

        return Game(game_id, subsets)

    def __repr__(self):
        subset_string = ','.join((repr(subset) for subset in self.cube_subsets))
        return f"{self.id}: {subset_string}"

class GameGroup:
    def __init__(self, games):
        self.games = games

    def parse(game_lines: [str]):
        return GameGroup([Game.parse(line) for line in game_lines])

    def __repr__(self):
        games_string = '\n'.join((repr(game) for game in self.games))
        return games_string


def parse_input(text: str):
    return GameGroup.parse(text)

def solve_part1(game_group):
    max_set = CubeSubset(12, 13, 14)

    valid_game_id_sum = 0
    for game in game_group.games:
        valid_game = True
        for subset in game.cube_subsets:
            if subset.red > max_set.red or subset.green > max_set.green or subset.blue > max_set.blue:
                valid_game = False

        if valid_game:
            valid_game_id_sum += game.id

    return valid_game_id_sum

def solve_part2(game_group):

    total_set_power = 0
    
    for game in game_group.games:
        game_max_set = CubeSubset(0, 0, 0)
        for subset in game.cube_subsets:
            if subset.red > game_max_set.red:
                game_max_set.red = subset.red
            if subset.green > game_max_set.green:
                game_max_set.green = subset.green
            if subset.blue > game_max_set.blue:
                game_max_set.blue = subset.blue
        game_power = game_max_set.red * game_max_set.green * game_max_set.blue
        
        total_set_power += game_power

    return total_set_power


def example(file_name, solver):
    with open(file_name) as fd:
        game_group = parse_input(fd.readlines())
    
    print(f'{file_name}: {solver(game_group)}')

def main():
    example('input1.txt', solve_part1)
    example('input2.txt', solve_part1)
    example('input3.txt', solve_part2)
    example('input4.txt', solve_part2)
    
if __name__ == '__main__':
    main()
