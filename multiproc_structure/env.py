import gymnasium as gym
from gymnasium.spaces import Dict, Box
from .ros_int import RosInt
import numpy as np
import time
import rclpy

class Env(gym.Env):
    def __init__(self, ros_int : RosInt) -> None:
        super().__init__()
        self.ros_int = ros_int
        self.node = self.ros_int.node
        self.is_resetting = False
        self.namespace = self.node.get_namespace()
        self.step_count = 0
        self.observation_space = Dict(
            {
                'observation': Box(low=-1, high=1, shape=(1,), dtype=np.float32),
            }
        )
        self.action_space = Box(low=-1, high=1, shape=(1,), dtype=np.float32)

    def step(self, action):
        self.step_count += 1
        if self.step_count == 10 and self.namespace == '/env_0':
            self.reset()

        if self.reset_future.done() and self.is_resetting:
            self.node.get_logger().info(f'[{self.namespace[1:]}] Reset done')
            self.is_resetting = False

        if not self.is_resetting:
            print(f"[{self.namespace[1:]}] step {self.step_count}")
            time.sleep(1)
            observation = {
                'observation': np.array([0.0]),
            }
            reward = 0.0
            terminated = False
            truncated = False
            info = {}
        else:
            time.sleep(1)
            observation = {
                'observation': np.array([0.0]),
            }
            reward = 0.0
            terminated = False
            truncated = False
            info = {}    


        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        if not self.is_resetting:
            print(f"[{self.namespace[1:]}] reset")
            self.reset_future = self.ros_int.call_test_service()
            self.is_resetting = True
        observation = {
            'observation': np.array([0.0]),
        }
        info = {}


        return observation, info


