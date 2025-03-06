import rclpy
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
import rclpy.executors
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import PPO
import threading

from .ros_int import RosInt
from .env import Env


def make_env(rank):
    def _init():
        return Env(RosInt(f'/env_{rank}'))
    return _init



def main():
    vec_env = SubprocVecEnv([make_env(i) for i in range(2)]) 
    model = PPO('MultiInputPolicy', vec_env, verbose=1)
    model.learn(total_timesteps=1000)
    

if __name__ == '__main__':
    main()
