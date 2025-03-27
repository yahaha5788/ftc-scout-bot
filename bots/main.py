#this will be the file to run all the bots
#might also have some logging stuff too

from polaroidsupercolorinstantcamera import bot as polaroid
from harold import bot as harold
from robobot import bot as robobot

from dotenv import dotenv_values

config = dotenv_values("C:/Users/thomp/bots/keys.env")

polaroid.run(config["POLAROID_KEY"]
robobot.run(config["ROBOBOT_KEY"]
harold.run(config["HAROLD_KEY"]