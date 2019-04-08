from optparse import OptionParser
import importlib

def create_optparser():
	usage_str = "python %prog [options] <game> [game_level]"
	description_str = \
		"\"game\" is the name of the game. " \
		"\"game_level\" is an optional argument (not needed " \
		"by every game) to specify the level of the game."

	parser = OptionParser(usage = usage_str, description = description_str)
	parser.add_option("-f", "--fps", \
		action = "store", type = "int", dest = "fps", default = 30, \
		help = "the updating rate of the game process [default: %default]")
	parser.add_option("-m", "--manual", \
		action = "store_true", dest = "manual_mode", default = False, \
		help = "start the game in the manual mode instead of " \
		"the machine learning mode [default: %default]")
	parser.add_option("-r", "--record", \
		action = "store_true", dest = "record", default = False, \
		help = "Pickle the game progress (a list of scene info) to the log files "\
		"[default: %default]")

	return parser

def has_ml_script(game_name: str):
	import os.path

	dir_path = os.path.dirname(__file__)
	ml_script_path = os.path.join(dir_path, "{}/ml/ml_play.py".format(game_name))

	return os.path.exists(ml_script_path)

if __name__ == "__main__":
	optparser = create_optparser()
	(options, args) = optparser.parse_args()

	try:
		game_name = args[0].lower()
		game_options = args[1:]
		game = importlib.import_module("{}.main".format(game_name))

		if not options.manual_mode and not has_ml_script(game_name):
			raise FileNotFoundError

	except IndexError:
		print("Error: <game> is not specified. Use -h to see help.")
		print(optparser.get_usage()[:-1])
	except ModuleNotFoundError:
		print("Error: Game \"{}\" is not found.".format(game_name))
	except FileNotFoundError:
		print("Error: The script \"{}/ml/ml_play.py\" is not provided. " \
			"Cannot start the machine learning mode.".format(game_name))
	else:
		if options.manual_mode:
			game.manual_mode(options.fps, options.record, *game_options)
		else:
			game.ml_mode(options.fps, options.record, *game_options)