import os, json, logging
from sys import argv, exit
from time import sleep

from core.vars import BASE_DIR
from core.api import MPServerAPI
from core.video_pad import MPVideoPad

ZERO = 3
ONE = 4

KEY_MAP = {
	'1_BadDadMenu':['2_SoftwareMenu','61_HardwareMenu_New'],
	'2_SoftwareMenu':['3_YesSelfCriticalStoppedWorkingMenu','31_NoSelfCriticalStoppedWorkingMenu'],
	'3_YesSelfCriticalStoppedWorkingMenu':['4_YesTendencyToOverheatMenu','18_NoTendencyToOverheatMenu'],
	'4_YesTendencyToOverheatMenu':['5_YesEatenSiblingsMenu','12_NoEatenSiblingsMenu'],
	'5_YesEatenSiblingsMenu':['6_PresentsHimselfAsVictimMenu','9_SpywareOutdatedMenu'],
	'6_PresentsHimselfAsVictimMenu':['7_UnableToConnectEnd', '8_pervertsNetworkEnd_New'],
	'7_UnableToConnectEnd':None,
	'8_pervertsNetworkEnd_New':None,
	'9_SpywareOutdatedMenu':['10_OverExpressesEnd', '11_FilesOpenWithWrongProgramEnd'],
	'10_OverExpressesEnd':None,
	'11_FilesOpenWithWrongProgramEnd':None,
	'12_NoEatenSiblingsMenu':['13_YesLetStrangersUseYourIdentityMenu', '15_NoLetStrangersUseYourIdentityMenu'],
	'13_YesLetStrangersUseYourIdentityMenu':['14_CatastrophicFailureEnd','8_pervertsNetworkEnd_New'],
	'14_CatastrophicFailureEnd':None,
	'15_NoLetStrangersUseYourIdentityMenu':['16_YesInfectedbyPornVirusEnd', '17_NoInfectedbyPornVirusEnd'],
	'16_YesInfectedbyPornVirusEnd':None,
	'17_NoInfectedbyPornVirusEnd':None,
	'18_NoTendencyToOverheatMenu':['19_YesControlFreakinessMenu', '26_NoControlFreakinessMenu'],
	'19_YesControlFreakinessMenu':['20_YesDrunkAllTheTimeMenu','23_NoDrunkAllTheTimeMenu'],
	'20_YesDrunkAllTheTimeMenu':['21_ZeroGlitchEnd','22_OneGlitchEnd'],
	'21_ZeroGlitchEnd':None,
	'22_OneGlitchEnd':None,
	'23_NoDrunkAllTheTimeMenu':['24_YesTriedTransferringHisUserAccountEnd','25_NoTriedTransferringHisUserAccountEnd'],
	'24_YesTriedTransferringHisUserAccountEnd':None,
	'25_NoTriedTransferringHisUserAccountEnd':None,
	'26_NoControlFreakinessMenu':['27_YesUnableToOpenHelpAndSupportMenu_New', '29_NoUnableToOpenHelpAndSupportMenu'],
	'27_YesUnableToOpenHelpAndSupportMenu_New':['28_NoMistressEnd','22_OneGlitchEnd'],
	'28_NoMistressEnd':None,
	'29_NoUnableToOpenHelpAndSupportMenu':['30_UpdateSoftwareAvailableEnd_New', '22_OneGlitchEnd'],
	'30_UpdateSoftwareAvailableEnd_New':None,
	'31_NoSelfCriticalStoppedWorkingMenu':['32_LimboLassoMercuryNoSelfCriticalMenu','95_ExecutableUMLDracoNoFearLossOfControlMenu'],
	'32_LimboLassoMercuryNoSelfCriticalMenu':['33_YesSomaticNarcissistMenu','40_NoSomaticNarcissistMenu'],
	'33_YesSomaticNarcissistMenu':['34_YesPayMoreToAvoidTaxesMenu','37_NoPayMoreToAvoidTaxesMenu'],
	'34_YesPayMoreToAvoidTaxesMenu':['35_YesTartuffeEnd','36_NoTartuffeEnd'],
	'35_YesTartuffeEnd':None,
	'36_NoTartuffeEnd':None,
	'37_NoPayMoreToAvoidTaxesMenu':['38_YesSacrificeChildrenEnd','39_NoSacrificeChildrenEnd_New'],
	'38_YesSacrificeChildrenEnd':None,
	'39_NoSacrificeChildrenEnd_New':None,
	'40_NoSomaticNarcissistMenu':['41_YesFatheredMoreMenu','44_NoFatheredMoreMenu'],
	'41_YesFatheredMoreMenu':['42_YesRootkitViolateEnd','43_NoRootkitViolateEnd'],
	'42_YesRootkitViolateEnd':None,
	'43_NoRootkitViolateEnd':None,
	'44_NoFatheredMoreMenu':['45_YesStuckInfiniteLoopsEnd','46_NoStuckInfiniteLoopsEnd'],
	'45_YesStuckInfiniteLoopsEnd':None,
	'46_NoStuckInfiniteLoopsEnd':None,
	'47_ExecutableUMLDracoNoSelfCriticalMenu':['48_YesMaskOfKindnessMenu','55_NoMaskOfKindnessMenu'],
	'48_YesMaskOfKindnessMenu':['49_YesConstantPopUpsMenu','52_NoConstantPopUpsMenu'],
	'49_YesConstantPopUpsMenu':['50_YesKilledAllCrewEnd','51_NoKilledAllCrewEnd'],
	'50_YesKilledAllCrewEnd':None,
	'51_NoKilledAllCrewEnd':None,
	'52_NoConstantPopUpsMenu':['53_YesStoppedRespondingToTextEnd','54_NoStoppedRespondingToTextEnd'],
	'53_YesStoppedRespondingToTextEnd':None,
	'54_NoStoppedRespondingToTextEnd':None,
	'55_NoMaskOfKindnessMenu':['56_YesApplicationManifestRunningImproperlyMenu','58_NoApplicationManifestRunningImproperlyMenu'],
	'56_YesApplicationManifestRunningImproperlyMenu':['30_UpdateSoftwareAvailableEnd_New', '57_NoCompensatedForResourceLeaksEnd'],
	'57_NoCompensatedForResourceLeaksEnd':None,
	'58_NoApplicationManifestRunningImproperlyMenu':['59_YesGivenInToMadnessEnd', '60_NoGivenInToMadnessEnd'],
	'59_YesGivenInToMadnessEnd':None,
	'60_NoGivenInToMadnessEnd':None,
	'61_HardwareMenu_New':['62_YesObsessedWithFailureMenu','83_NoObsessedWithFailureMenu'],
	'62_YesObsessedWithFailureMenu':['31_NoSelfCriticalStoppedWorkingMenu','72_NoAffectedByCorruptedBloodMenu'],
	'63_LimboLassoMercuryCorruptedBloodMenu':['64_YesOpenAndCloseProgramsMenu', '66_NoOpenAndCloseProgramsMenu'],
	'64_YesOpenAndCloseProgramsMenu':['42_YesRootkitViolateEnd','65_NoObsessedWithHisPowerSupplyEnd'],
	'65_NoObsessedWithHisPowerSupplyEnd':None,
	'66_NoOpenAndCloseProgramsMenu':['59_YesGivenInToMadnessEnd','67_NoDisplayErrorMessageEnd'],
	'67_NoDisplayErrorMessageEnd':None,
	'68_ExecutableUMLDracoCorruptedBloodMenu_New':['69_YesSinOfSelfLoveMenu', '70_NoSinOfSelfLoveMenu'],
	'69_YesSinOfSelfLoveMenu':['51_NoKilledAllCrewEnd', '60_NoGivenInToMadnessEnd'],
	'70_NoSinOfSelfLoveMenu':['35_YesTartuffeEnd', '71_NoSystemFreezeEnd'],
	'71_NoSystemFreezeEnd':None,
	'72_NoAffectedByCorruptedBloodMenu':['73_YesStrangeNoisesMenu', '79_NoStrangeNoisesMenu'],
	'73_YesStrangeNoisesMenu':['74_YesLogicGateInputsFaultyMenu','76_NoLogicGateInputsFaultyMenu'],
	'74_YesLogicGateInputsFaultyMenu':['25_NoTriedTransferringHisUserAccountEnd','75_NoCapsLockEnd'],
	'75_NoCapsLockEnd':None,
	'76_NoLogicGateInputsFaultyMenu':['77_YesOpenFilesAtRandomEnd','78_NoOpenFilesAtRandomEnd'],
	'77_YesOpenFilesAtRandomEnd':None,
	'78_NoOpenFilesAtRandomEnd':None,
	'79_NoStrangeNoisesMenu':['80_YesTrappedYouInLabyrinthMenu','81_NoTrappedYouInLabyrinthMenu'],
	'80_YesTrappedYouInLabyrinthMenu':['16_YesInfectedbyPornVirusEnd','25_NoTriedTransferringHisUserAccountEnd'],
	'81_NoTrappedYouInLabyrinthMenu':['75_NoCapsLockEnd','82_NoBasicInputOutputSystemEnd'],
	'82_NoBasicInputOutputSystemEnd':None,
	'83_NoObsessedWithFailureMenu':['84_YesFearLossOfControlMenu','31_NoSelfCriticalStoppedWorkingMenu'],
	'84_YesFearLossOfControlMenu':['85_YesStoppedYouFromConnectingMenu','88_NoStoppedYouFromConnectingMenu'],
	'85_YesStoppedYouFromConnectingMenu':['86_YesControlledRemotelyMenu','87_NoControlledRemotelyMenu'],
	'86_YesControlledRemotelyMenu':['8_pervertsNetworkEnd_New', '60_NoGivenInToMadnessEnd'],
	'87_NoControlledRemotelyMenu':['54_NoStoppedRespondingToTextEnd', '45_YesStuckInfiniteLoopsEnd'], 
	'88_NoStoppedYouFromConnectingMenu':['89_YesObsoleteMenu', '92_NoObsoleteMenu'],
	'89_YesObsoleteMenu':['90_YesUninstallEnd', '91_NoUninstallEnd'],
	'90_YesUninstallEnd':None,
	'91_NoUninstallEnd':None,
	'92_NoObsoleteMenu':['93_YesLazyEnd', '94_NoLazyEnd'],
	'93_YesLazyEnd':None,
	'94_NoLazyEnd':None,
	'95_ExecutableUMLDracoNoFearLossOfControlMenu':['96_YesPromisesMenu','98_NoPromisesMenu'],
	'96_YesPromisesMenu':['97_YesSortingAlgorithmMalfunctioningEnd', '94_NoLazyEnd'],
	'97_YesSortingAlgorithmMalfunctioningEnd':None,
	'98_NoPromisesMenu':['104_YesDataflowSquigglyColdAndCalculatingEnd','99_NoDataflowSquigglyPromisesEnd'],
	'99_NoDataflowSquigglyPromisesEnd':None,
	'100_LimboLassoMercuryNoFearLossOfControlMenu':['101_YesColdAndCalculatingMenu','98_NoPromisesMenu'],
	'101_YesColdAndCalculatingMenu':['102_YesFaultTolerantEnd', '103_NoFaultTolerantEnd'],
	'102_YesFaultTolerantEnd':None,
	'103_NoFaultTolerantEnd':None,
	'104_YesDataflowSquigglyColdAndCalculatingEnd':None
}

class BadDadAndBeyond(MPServerAPI, MPVideoPad):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.conf['d_files'].update({
			'vid' : {
				'log' : os.path.join(BASE_DIR, ".monitor", "%s.log.txt" % self.conf['rpi_id'])
			},
			'video_listener_callback' : {
				'log' : os.path.join(BASE_DIR, ".monitor", "%s.log.txt" % self.conf['rpi_id']),
				'pid' : os.path.join(BASE_DIR, ".monitor", "video_listener_callback.pid.txt")
			}
		})

		MPVideoPad.__init__(self)
		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def route_next(self, route=None):
		if route is None:
			route = "1_BadDadMenu"

		route_prompt = os.path.join(self.conf['media_dir'], "prompts", "%s.wav" % route)

		if KEY_MAP[route] != None:
			choice = self.prompt(route_prompt, release_keys=[ZERO, ONE])
			return self.route_next(route=KEY_MAP[route][0 if choice is ZERO else 1])
		else:
			if self.say(route_prompt, interruptable=False):
				self.stop_video_pad()

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
		self.play_video("BAD_DAD.mp4", with_extras={"loop":""})
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

