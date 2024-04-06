from collections import deque

from agents.base_agent import BaseAgent
from tensorflow.keras import models, layers, initializers
import random

class DQNAgent(BaseAgent):
    # Modeling DQN from https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
    def __init__(self, action_space, state_visual_dim=(284, 380), state_numerical_dim=1, history_length=5, epsilon = 0.1):
        super().__init__(action_space)

        self.state_shape = None
        self.history = deque(maxlen=history_length)
        self.epsilon = epsilon

        # Using Experience Replay (s_t, a_t, r_t, s_t+1)
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
        merged = layers.Dense(1024, activation='relu')(merged)

        # Output Values
        action_values = layers.Dense(len(action_space), activation='linear')(merged)

        model = models.Model(inputs=[visual_input, optimizer_input], outputs=action_values)
        model.compile(loss='mse', optimizer='adam')

        initializer = initializers.glorot_uniform(seed=123456)
        for layer in model.layers:
            if hasattr(layer, 'kernel_initializer'):
                layer.kernel_initializer = initializer

        self.model = model

    # Epsilon Greedy Action Picker
    def observe_state(self, state):
        pass

    def get_action(self):
        # Todo
        eps = 0
        if eps < self.epsilon:
            return random.choice(self.action_space)
        else:
            return self.model.predict()

    def learn(self, experience):
        pass
