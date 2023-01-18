import os

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(env_file=os.path.join("chat_chak/.env"))
