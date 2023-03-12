import time
import pygame
import eval_table
import game_engine

game_mode = 'bogart'
et = eval_table.get_eval_table(game_mode=game_mode)
pygame.init()
WIDTH = 880
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

def load(name, size='tile', rotate=0):
    sizes = {'tile': (WIDTH / 3 * 0.95, WIDTH / 3 * 0.95), 'full': (WIDTH, WIDTH)}
    return pygame.transform.scale(pygame.image.load("Images/"+name+".jpeg").convert(), sizes[size])

images = {'0': load('r2'), 'X': load('r2'), '1': load('p1'), '2': load('q2'), 'intro': load('intro', size='full'), 'back': load('back', size='full')}

def skin(position):

    return position

def intro():
    win.fill((255,255,255))
    win.blit(images['intro'], (0, 0))
    win.blit(pygame.font.SysFont('Comic Sans MS', WIDTH//8).render('Pick Side', False, (255, 255, 255)), (WIDTH//4, WIDTH//8))
    pygame.display.update()

def render(position):
    win.blit(images['back'], (0, 0))
    for i in range(9):
        char = position[i+2]
        win.blit(images[char], (i%3*WIDTH/3 + WIDTH/6*0.05, i//3*WIDTH/3 + WIDTH/6*0.05))
    pygame.display.update()

def winner(position, w, move_count):
    win.blit(images['back'], (0, 0))
    position = position.replace(str(3-int(w)), '0')
    for i in range(9):
        char = position[i+2]
        win.blit(images[char], (i%3*WIDTH/3 + WIDTH/6*0.05, i//3*WIDTH/3 + WIDTH/6*0.05))
    texts = {'1': ' Pigs Win ', '2': 'Apples Win'}
    win.blit(pygame.font.SysFont('Comic Sans MS', WIDTH//8).render(texts[w], False, (255, 255, 255)), (WIDTH//6, 2*WIDTH//5))
    win.blit(pygame.font.SysFont('Comic Sans MS', WIDTH//12).render('moves: '+str(move_count), False, (255, 255, 255)), (WIDTH//3, 3*WIDTH//5))
    pygame.display.update()

def intro_click():
    m_x, m_y = pygame.mouse.get_pos()
    if WIDTH*1/3 < m_y < WIDTH*2/3:
        if m_x < WIDTH/2:
            return 'pig'
        else:
            return 'apple'
    return ''

def add_click(position):
    m_x, m_y = pygame.mouse.get_pos()
    i = int(2 + m_x//(WIDTH/3)+3*(m_y//(WIDTH/3)))
    if position[i] == '0':
        return (str(3-int(position[0]))+position[1:i]+position[0]+position[i+1:]).replace('X', '0')
    return position

def remove_click(position, game_mode='basic'):
    m_x, m_y = pygame.mouse.get_pos()
    i = int(2 + m_x//(WIDTH/3)+3*(m_y//(WIDTH/3)))
    if game_mode == 'basic':
        if position[i] == position[0]:
            return position[:i]+'X'+position[i+1:]
        else:
            return position
    if game_mode == 'bogart' or game_mode == 'bogart2':
        if position[2+4] == position[0]:
            if i == 2+4:
                return position[:i] + 'X' + position[i + 1:]
            return position
        elif position[i] == position[0]:
            return position[:i]+'X'+position[i+1:]
        else:
            return position

def main():
    while True:
        delay = 1
        start = ''
        while start == '':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = intro_click()
            intro()
        move_count = 1
        position = '1_000000000'
        evaluation = et.loc[position]['eval']
        print(move_count, position, evaluation)
        print(et.loc[position]['successors'], et.loc[position]['successors_evals'])
        render(skin(position))
        if start == 'apple':
            time.sleep(delay)
            position = game_engine.make_move(et.loc[position])
            evaluation = et.loc[position]['eval']
            print(move_count, position, evaluation)
            print(et.loc[position]['successors'], et.loc[position]['successors_evals'])
        while -1 < evaluation < 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if position.count('0') + position.count('X') == 3:
                        position = remove_click(position, game_mode=game_mode)
                    else:
                        position = add_click(position)
                        if not 'X' in position:
                            move_count += 1
                            evaluation = et.loc[position]['eval']
                            print(move_count, position, evaluation)
                            print(et.loc[position]['successors'], et.loc[position]['successors_evals'])
                            render(position)
                            time.sleep(delay)
                            if -1 < evaluation < 1:
                                position = game_engine.make_move(et.loc[position])
                                evaluation = et.loc[position]['eval']
                                print(move_count, position, evaluation)
                                print(et.loc[position]['successors'], et.loc[position]['successors_evals'])
            render(skin(position))
        time.sleep(delay)
        count = 0
        while count<2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    count += 1
            if evaluation == 1:
                winner(position, '1', move_count)
            if evaluation == -1:
                winner(position, '2', move_count)

while True:
    if __name__ == '__main__':
        main()