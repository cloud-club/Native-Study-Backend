import typing as t
from pathlib import Path

from dotenv import find_dotenv

ENV_PATH = Path(find_dotenv())


def read_env():
    envs = list()
    with open(ENV_PATH, "r") as file_io:
        envs = file_io.readlines()
    return envs


def remove_value(envs: t.List[str]):
    env_examples = list()
    for env in envs:
        if len(env) < 1:
            env_examples.append("\n")
        elif "=" not in env or env[0] == "#":
            env_examples.append(env)
        else:
            env = env.split("=")[0]
            env_examples.append(f"{env}=\n")
    return env_examples


def save_env_example(env_examples: t.List[str]):
    env_path = ENV_PATH.parent.joinpath(".env.example")
    with open(env_path, "w") as file_io:
        file_io.writelines(env_examples)


if __name__ == "__main__":
    envs = read_env()
    env_examples = remove_value(envs)
    save_env_example(env_examples)
