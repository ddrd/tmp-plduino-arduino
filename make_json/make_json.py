import re
import sys
import os
from boards import *
from esptools import *

def make_json():
	return (
"""{
	"packages": [{
		"maintainer": "Digital Loggers Inc", 
		"websiteURL": "https://github.com/digitalloggers/", 
		"name": "PLDuino",
		"platforms": [$PLATFORMS$
		],
		"tools": [
			$TOOLS$
		]
	}]
}""".replace("$PLATFORMS$", make_boards())
	.replace("$TOOLS$", make_esptools()))
