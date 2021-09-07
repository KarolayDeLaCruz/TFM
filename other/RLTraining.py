from gym import Env
from gym.spaces import Discrete, Box
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from tensorflow.keras.optimizers import Adam




class Cat(Env):
    """
       Description:
           A cat has 5 action that can take based on 11 sensors and 4 personality parameters.

       Observation:
        Type: Box(15)
        Num     Observation               Min                     Max
        0       mic1                      -100                    100
        1       mic2                      -100                    100
        2       ultr                      -100                    100
        3-10    cap1-cap8                 -100                    100
        11-14   p1-p4                     0                       1

        Actions:
         Type: Discrete(8)
         Num   Action
         0     Start
         1     Explore
         2     Wait
         3     Hunt
         4     Groom
         5     Attention
         6     Sleep
         7     Play

        Reward:
                Reward is 1 for every step taken, including the termination step
        Starting State:
                All observations are assigned a uniform random value in [-1..1]
        Episode Termination:
                Solved Requirements:
                Considered solved when the average return is greater than or equal to
                195.0 over 100 consecutive trials.
    """

    def __init__(self):

        high = np.array([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
                        dtype=np.float32)
        self.action_space = Discrete(8)
        self.observation_space = Box(-high, high, dtype=np.float32)


        self.state = None


    def step(self, action):

        # # Sensors
        mic1 = 0.1
        mic2 = 0.2
        ultr = 0.1
        cap1 = 0.2
        cap2 = 0.1
        cap3 = 0.2
        cap4 = 0.3
        cap5 = 0.5
        cap6 = 0.6
        cap7 = 0.1
        cap8 = 0.2

        # # Personality
        p1 = 0.1
        p2 = 0.3
        p3 = 0.2
        p4 = 0.6

        self.state = (mic1,mic2,ultr,cap1,cap2,cap3,cap4,cap5,cap6,cap7,cap8,p1,p2,p3,p4)

        # Calculate reward
        #reward = input("\n Enter reward (-1) or 1:\n")
        #reward = int(reward)
        if action == 2:
            reward = 1
        else:
            reward = -1

        # Set placeholder for info
        info = {}
        done = True

        # Return step information
        print('\n Reward:{} Action:{} State:{}'.format(reward, action, self.state))
        return np.array(self.state), reward, done, info

    # Reset the environment and return to initial stat
    def reset(self):
        # Reset action
        self.state = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        return np.array(self.state)


# Enviroment
env = Cat()

# Observation space
env.observation_space.sample()
#
# # episodes = 10
# # for episode in range(1, episodes + 1):
# #     state = env.reset()
# #     done = False
# #     score = 0
# #
# #     while not done:
# #         action = env.action_space.sample()  # diferent actions
# #         n_state,reward, done, info = env.step(action)
# #         score += reward
# #     print('Episode:{} Score:{}'.format(episode, score))
#
## 2. Create a Deep Learning Model with Keras

states=env.observation_space.shape[0] #states available from enviroment
actions=env.action_space.n            #action

def build_model(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1, states)))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model

model = build_model(states, actions)
model.summary()


## 3. Build Agent with Keras-RL

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                  nb_actions=actions, nb_steps_warmup=10,
                   target_model_update=1e-2)
    return dqn


dqn = build_agent(model, actions)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])
#dqn.fit(env, nb_steps=5000, visualize=False, verbose=1)

#scores = dqn.test(env, nb_episodes=100, visualize=False)
#print(np.mean(scores.history['episode_reward']))


# 5. Save Agent from Memory
#dqn.save_weights('dqn_weights.h5f', overwrite=True)


dqn.load_weights('dqn_weights.h5f')
_ = dqn.test(env, nb_episodes=3, visualize=False)
