import pathlib
from collections import deque
from typing import Tuple, List

from agents.base_agent import BaseAgent
from tensorflow.keras import models, layers, initializers
import random
import numpy as np

"""
Implementation of Deep Q Learning using Experience Replay

The agent takes in visual input (game frames) and other numerical state input (game gems)
The agent keeps track of a history of the past 5 game frames captured.

Model utilizes a deep Q network to learn Q-function, which is comprised of a convolutional network and a 
fully connected network.

Action is determined using an epsilon greedy policy. Where with epsilon probability a random action is picked,
otherwise the best action is picked according to the Q-function.

Agent learns using experience replay where tuples of (state, action, reward, next_state, done) added to replay buffer.
To learn, agent samples experiences from replay buffer. Optimization is based on MSE.

Initial weights are initialized randomly, using glorot initialization.
"""


class DQNAgent(BaseAgent):
    # Modeling DQN from https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
    def __init__(self, action_space, state_visual_dim=(284, 380), state_numerical_dim=1, history_length=5,
                 epsilon=0.1,
                 batch_size=64, discount_factor=0.95):
        super().__init__(action_space)

        self.state_visual_dim = state_visual_dim
        self.state_numerical_dim = state_numerical_dim
        self.state_history: List[Tuple[np.ndarray, int]] = []
        self.state_history_len = history_length
        self.epsilon = epsilon
        self.batch_size = 20
        self.discount_factor = discount_factor

        # Replay memory buffer
        self.replay_memory = deque(maxlen=10000)

        # CNN to process visual information
        visual_input = layers.Input(shape=(state_visual_dim[0], state_visual_dim[1], history_length))
        visual_features = layers.Conv2D(32, kernel_size=(3, 3), activation='relu')(visual_input)
        visual_features = layers.Conv2D(64, kernel_size=(3, 3), activation='relu')(visual_features)
        visual_features = layers.MaxPooling2D(pool_size=(2, 2))(visual_features)
        visual_features = layers.Flatten()(visual_features)

        # Numerical information (gems)
        optimizer_input = layers.Input(shape=(state_numerical_dim,))
        numerical_features = layers.Dense(64, activation='relu')(optimizer_input)

        # Merged Layers
        merged = layers.concatenate([visual_features, numerical_features])
        merged = layers.Dense(512, activation='relu')(merged)

        # Output Values
        action_values = layers.Dense(len(action_space), activation='linear')(merged)

        model = models.Model(inputs=[visual_input, optimizer_input], outputs=action_values)
        model.compile(loss='mse', optimizer='adam')

        initializer = initializers.glorot_uniform(seed=123456)
        for layer in model.layers:
            if hasattr(layer, 'kernel_initializer'):
                layer.kernel_initializer = initializer

        if pathlib.Path('./models/dqn_model.weights.h5').exists():
            print('Model already exists, loading weights')
            model.load_weights('dqn_model.weights.h5')
        self.model = model

    """
    Prepares state_history for model prediction or training.
    """

    def prepare_current_state(self, state_history: List[Tuple[np.ndarray, int]]):
        visual_data = [state[0] for state in state_history]
        numerical_data = [state[1] for state in state_history]

        visual_data = np.array(visual_data)
        numerical_data = np.array(numerical_data)

        visual_data = np.transpose(visual_data, (1, 2, 0)).reshape(1, *self.state_visual_dim, self.state_history_len)
        visual_data = visual_data / 255.0  # Normalize data

        numerical_data = numerical_data[-1].reshape(1, self.state_numerical_dim)

        return visual_data, numerical_data

    # Epsilon Greedy Action Picker
    def observe_state(self, state):
        frame = state.get('current_frame')
        gems = state.get('current_gems')
        state_tuple = (frame, gems)

        # Fill frame history with first frame on first call.
        if len(self.state_history) < self.state_history_len:
            while len(self.state_history) < self.state_history_len:
                self.state_history.append(state_tuple)

        self.state_history.pop(0)
        self.state_history.append(state_tuple)

    def get_action(self):
        eps = random.random()
        if eps < self.epsilon:
            return random.randint(0, len(self.action_space) - 1)
        else:
            q_values = self.model.predict(self.prepare_current_state(self.state_history))[0]
            # return the index of the action to take
            return np.argmax(q_values)

    def store_experience(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done, self.state_history))

    def learn(self):
        if len(self.replay_memory) < self.batch_size:
            # Not enough experiences to train reasonably
            return

        batch = random.sample(self.replay_memory, self.batch_size)
        states, actions, rewards, next_states, dones, states_histories = zip(*batch)

        prepared_states = []
        prepared_next_states = []
        for i, state in enumerate(states):
            history = states_histories[i]
            prepared_states.append(self.prepare_current_state(history))

        for i, next_state in enumerate(next_states):
            history = states_histories[i]
            history.pop(0)
            history.append((next_state.get('current_frame'), next_state.get('current_gems')))
            prepared_next_states.append(self.prepare_current_state(history))

        current_states = np.vstack([state[0] for state in prepared_states])
        current_gems = np.vstack([state[1] for state in prepared_states])

        next_states = np.vstack([state[0] for state in prepared_next_states])
        next_gems = np.vstack([state[1] for state in prepared_next_states])

        current_q_values = self.model.predict([current_states, current_gems])
        next_q_values = self.model.predict([next_states, next_gems])

        max_q_values = np.max(next_q_values, axis=1)
        targets = np.array(rewards) + (1 - np.array(dones)) * max_q_values * self.discount_factor

        target_q_values = current_q_values.copy()
        for i, action in enumerate(actions):
            target_q_values[i][action] = targets[i]

        self.model.fit([current_states, current_gems], target_q_values, epochs=1, verbose=0,
                       batch_size=self.batch_size)

    def reset(self):
        self.state_history = []

    def quit(self):
        self.save_model()

    def save_model(self):
        print('Saving DQN agent model weights')
        self.model.save_weights('models/dqn_model.weights.h5')
