import os, json, logging
from sys import argv, exit
from time import sleep

from core.vars import BASE_DIR
from core.api import MPServerAPI
from core.video_pad import MPVideoPad

ZERO = 13
ONE = 3

KEY_MAP = {
	"main_menu" : ["software_menu", "hardware_menu"],
	"software_menu" : ["yes_self_critical_stopped_working", "no_self_critical_stopped_working"],
	"hardware_menu" : [],
	"yes_self_critical_stopped_working" : ["yes_tendency_to_overheat", "no_tendency_to_overheat"],
	"no_self_critical_stopped_working" : [],
	"yes_tendency_to_overheat" : ["yes_eaten_siblings", "no_eaten_siblings"],
	"no_tendency_to_overheat" : ["yes_control_freakiness", "no_control_freakiness"],
	"yes_eaten_siblings" : ["presents_himself_as_victim", "spyware_outdated"],
	"no_eaten_siblings" : [],
	"presents_himself_as_victim" : ["unable_to_connect", "perverts_network"],
	"spyware_outdated" : ["over_expresses", "files_open_with_wrong_program"],
	"unable_to_connect" : None,
	"perverts_network" : None,
	"over_expresses" : None,
	"files_open_with_wrong_program" : None,
	"no_eaten_siblings" : ["yes_let_strangers_use_your_identity", "no_let_strangers_use_your_identity"],
	"yes_let_strangers_use_your_identity" : ["catastrophic_failure", "other_bugs_menu"],
	"no_let_strangers_use_your_identity" : ["yes_infected_by_porn_virus", "no_infected_by_porn_virus"],
	"catastrophic_failure" : None,
	"yes_infected_by_porn_virus" : None,
	"no_infected_by_porn_virus" : None,
	"yes_control_freakiness" : ["yes_drunk_all_the_time", "no_drunk_all_the_time"],
	"no_control_freakiness" : ["yes_unable_to_open_help", "no_unable_to_open_help"],
	"yes_drunk_all_the_time" : ["zero_glitch_end", "one_glitch_end"],
	"no_drunk_all_the_time" : ["yes_transfer_user_account", "no_transfer_user_account"],
	"zero_glitch_end" : None,
	"one_glitch_end" : None,
	"yes_transfer_user_account" : None,
	"no_transfer_user_account" : None,
	"yes_unable_to_open_help" : ["no_mistress", "no_mistress"],
	"no_unable_to_open_help" : ["update_software_available", "update_software_available"],
	"no_mistress" : None
}

class BadDadAndBeyond(MPServerAPI, MPVideoPad):
	def __init__(self):
		MPServerAPI.__init__(self)

	def route_next(self, route=None):
		if route = None:
			route = "main_menu"

		route_prompt = os.path.join(self.conf['media_dir'], "prompts", "%s.wav" % route)

		if KEY_MAP[route] != None:
			choice = self.prompt(route_prompt, release_keys=[ZERO, ONE])
			if choice == ZERO:
				next_route = KEY_MAP[route][0]
			elif choice == ONE:
				next_route = KEY_MAP[route][1]

			return self.route_next(route=next_route)
		else:
			return self.say(route_prompt)

		return False

	def reset_for_call(self):
		for video_mapping in self.video_mappings:
			self.db.delete("video_%s" % video_mapping.index)

		super(BadDadAndBeyond, self).reset_for_call()

	def on_hang_up(self):
		self.stop_video_pad()
		return super(BadDadAndBeyond, self).on_hang_up()

	def run_script(self):
		super(BadDadAndBeyond, self).run_script()
		self.route_next()

if __name__ == "__main__":
	res = False
	bdab = BadDadAndBeyond()

	if argv[1] in ['--stop', '--restart']:
		res = bdab.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = bdab.start()

	exit(0 if res else -1)

