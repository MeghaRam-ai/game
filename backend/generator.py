import pandas as pd
from tensorflow.python.estimator import keras
import numpy as np
from keras.preprocessing import sequence
import keras.models

game = pd.concat([pd.read_json('game1.json'), pd.read_json('game2.json')], ignore_index=True)
game['time'] = game['norm'].apply(lambda x: len(x) / 50)


def select_random_action(current_time, total_duration):
    '''

    :param current_time: updated time in each new item in the sequence
    :param total_duration: total game duration
    :return:
    '''
    all_actions = game[
        (game['time'] + current_time <= total_duration) & (game['time'] > 0.1) & (game['time'] < 3.0)]
    if len(all_actions) == 0:
        return None
    return all_actions.sample(1).iloc[0]


def regenerate(total_duration=400):
    '''

    :param total_duration: Duration of the regenerated game
    :return: sequence of actions and norm
    '''
    current_time = 0
    generated_data = pd.DataFrame(columns=['label', 'norm'])
    max_occurance = 3
    previous_label = None
    consecutive_occurance_count = 0
    while current_time < total_duration:
        # Select a random action
        selected_action = select_random_action(current_time, total_duration)

        # Ensure that a valid action was selected
        if selected_action is None:
            break

        # Check if the selected label is the same as the previous label
        if selected_action['label'] == previous_label:
            consecutive_occurance_count += 1
            if consecutive_occurance_count > max_occurance:
                continue
        else:
            consecutive_occurance_count = 0

        generated_data = pd.concat([generated_data, selected_action.to_frame().T], ignore_index=True)
        current_time += selected_action['time']
        previous_label = selected_action['label']

    generated_data.reset_index(drop=True, inplace=True)
    return generated_data[['label', 'norm']]


def generate_new_game_sequence(max_duration):
    '''
    Use the RNN model to predict the next actions based on the current sequence
    :param time:
    :return:
    '''
    match_2 = pd.read_json('game2.json')
    x_test = match_2['norm'].tolist()
    x_test = sequence.pad_sequences(x_test, maxlen=227)
    x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
    input = x_test[0].reshape((1, 1, 227))

    model  = keras.models.load_model('models/my_game_model.h5')
    total_duration = max_duration * 60
    current_duration = 0
    simulation = []

    initial_sequence = input
    while current_duration < total_duration:
        predicted_actions = model.predict(initial_sequence)
        duration = np.random.uniform(1, 10)
        if current_duration + duration > total_duration:
            duration = total_duration - current_duration
        simulation.extend(predicted_actions)
        current_duration += duration

    return simulation


