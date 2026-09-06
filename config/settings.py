import os 
from pathlib import Path 
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(BOOL,False)

)
environ.Env.read_env(os.path.join(Base_DIR,'.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
