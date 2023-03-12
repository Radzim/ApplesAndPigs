import itertools
import numpy as np
import pandas as pd


def check_valid(s):
    return not check_winner(str(3 - int(s[0])) + s[1:])

def check_winner(s):
    last_move = str(3 - int(s[0]))
    lines = [[2, 3, 4], [5, 6, 7], [8, 9, 10], [2, 5, 8], [3, 6, 9], [4, 7, 10], [2, 6, 10], [4, 6, 8]]
    for l in lines:
        if s[l[0]] == s[l[1]] == s[l[2]] == last_move:
            return True
    return False

def successors(position, game_mode='basic'):
    successors_ = []
    pieces_dict = {'pig': ['1', '2', '3'], 'apple': ['1', '2', '3']}
    pieces = {x: set([(x, y) for y in pieces_dict[x]]) for x in pieces_dict}
    to_move, array = position
    if sum([1 for x in array if x[0] == to_move]) < 3:
        pieces_to_move = pieces[to_move] - set(array)
        empty_indices = [i for i,val in enumerate(array) if val is None]
        for i in empty_indices:
            for piece in pieces_to_move:
                successor_ = position.copy() # check if necessary
                successor_[0] = set(pieces_dict.keys())
                successor_[1][i] = piece
                successors_.append(successor_)
    else:
        for i in range(9):
            if s[2+i] == to_move:
                for j in range(9):
                    if game_mode == 'basic':
                        if s[2+j] == '0':
                            s2 = s.copy()
                            s2[2 + j] = to_move
                            s2[2 + i] = '0'
                            s2[0] = str(3 - int(s2[0]))
                            suc.append(''.join(s2))
                    if game_mode == 'bogart':
                        if s[2 + 4] == s[0] and i != 4:
                            pass
                        elif s[2+j] == '0':
                            s2 = s.copy()
                            s2[2 + j] = to_move
                            s2[2 + i] = '0'
                            s2[0] = str(3 - int(s2[0]))
                            suc.append(''.join(s2))
    return suc

def get_eval_table(game_mode='basic'):
    try:
        return pd.read_pickle('eval_table_'+game_mode+'.pkl')
    except:
        starting_position = ('pig', tuple([None]*9))
        df = pd.DataFrame(columns=['position', 'successors', 'eval'])
        queue = []
        while len(queue) > 0:
            position_ = queue.pop()
            successors_ = successors(position_)
            queue.extend(successors(position_))
            eval_ = basic_eval(position_)
            df.append([position_, successors_, eval_])

        # checker = 0
        # while len(set(eval_table['eval'].values)) != checker:
        #     checker = len(set(eval_table['eval'].values))
        #     eval_table['eval'] = eval_table.apply(lambda x: (max(x['successors_evals'])/2 if x.name[0]=='1' else min(x['successors_evals'])/2) if -1 < x['eval'] < 1 else x['eval'], axis=1)
        #     eval_table['successors_evals'] = eval_table.apply(lambda x: [eval_table.loc[i]['eval'] for i in x['successors']], axis=1)
        #     print(set(eval_table['eval'].values))
        # eval_table['best_move'] = eval_table.apply(lambda x: (x['successors'][np.argmax(x['successors_evals'])] if x.name[0]=='1' else x['successors'][np.argmin(x['successors_evals'])]) if -1 < x['eval'] < 1 else 'game_over', axis=1)
        # eval_table['trickiness'] = eval_table.apply(lambda x: sum([-1/xx for xx in x['successors_evals'] if xx<0]) if x.name[0]=='1' else sum([1/xx for xx in x['successors_evals'] if xx>0]) if -1 < x['eval'] < 1 else x['eval'], axis=1)
        # eval_table['successors_trickiness'] = eval_table.apply(lambda x: [eval_table.loc[i]['trickiness'] for i in x['successors']], axis=1)
        df.to_pickle('eval_table_'+game_mode+'.pkl')
        return pd.read_pickle('eval_table_'+game_mode+'.pkl')
