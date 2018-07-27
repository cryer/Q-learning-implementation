# _*_coding:utf-8_*_
import time
import random

N_STATES = 6
ACTIONS = ['left', 'right']
EPSILON = 0.9
ALPHA = 0.1
GAMMA = 0.9
MAX_EPISODES = 13
FRESH_TIME = 0.3


def build_q_table():
    table = list(
        [[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0]]
    )
    return table


def choose_action(state, q_table):
    state_actions = q_table[state]
    if (random.random() > EPSILON) or (state_actions[0] == 0.0 and state_actions[1] == 0.0):
        action_name = random.choice(ACTIONS)
    else:
        action_name = 'left' if state_actions.index(max(state_actions)) == 0 else 'right'
    return action_name


def get_env_feedback(S, A):
    if A == 'right':
        if S == N_STATES - 2:
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:
        R = 0
        if S == 0:
            S_ = S
        else:
            S_ = S - 1
    return S_, R


def update_env(S, episode, step_counter):
    env_list = ['-'] * (N_STATES - 1) + ['T']  # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode + 1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl():
    # main part of RL loop
    q_table = build_q_table()
    for episode in range(MAX_EPISODES):  # 循环的回合数
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:  # 循环直到一局游戏结束

            A = choose_action(S, q_table)  # 根据状态选择动作
            S_, R = get_env_feedback(S, A)  # 获取环境的反馈
            a = 0 if A == 'left' else 1
            q_predict = q_table[S][a]
            if S_ != 'terminal':  # 如果没有结束就更新q target值
                q_target = R + GAMMA * max(q_table[S_])
            else:  # 游戏结束
                q_target = R
                is_terminated = True
            # 根据公式，增进式跟新q值
            q_table[S][a] += ALPHA * (q_target - q_predict)
            S = S_  # 进入下一状态
            # 跟新环境，并且计数加一，判断获取宝藏前走了多少步
            update_env(S, episode, step_counter + 1)
            step_counter += 1
    return q_table


if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)
