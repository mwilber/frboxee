#
#  frboxee.py
#  FRBoxee
#
import time
import os 

import PyFR.WaitController
import objc
import Foundation
import AppKit

#import modules required by application
import PyFR.Appliance
#import PyFR.Debugging

from ScriptingBridge import *

objc.loadBundle("BackRow", globals(), bundle_path=objc.pathForFramework("/System/Library/PrivateFrameworks/BackRow.framework" ))

class BoxeeLaunch(PyFR.WaitController.WaitController):
	def init(self):
		PyFR.WaitController.WaitController.initWithText_( self, 'Launching Boxee' )
		return self

	def PyFR_start(self):
		# Added applescript to launch boxee because launching it directly does not change focus
		self.launchApp( 'Applications/LaunchBoxee.app', None )
		#self.launchApp( '/Applications/Boxee.app/Contents/MacOS/Boxee', None )
        # FR automatically quits after 20 minutes.  This should disable that behavior...
		foo=objc.lookUpClass("FRAutoQuitManager")
		foo.sharedManager().setAutoQuitEnabled_(False)

	def launchApp(self, appToLaunch, fileToLoad=None):
		""" launches the application specified by appToLaunch.

			appToLaunch is a full path to an application. For example,
			to launch Sarafi, it would be:
				"/Applications/Safari.app"
		"""

		self.launchedApp = appToLaunch
		self.lookForApp = self.launchedApp.split('/')[-1][:-4]

		# Launch the app
		app = SBApplication.applicationWithURL_( NSURL.alloc().initFileURLWithPath_( self.launchedApp ) )
		app.activate()
		#os.execv(self.launchedApp, [''])

		# __IsRunning does not recognise Boxee for some reason. Just assume it's running.
		#while not self.__IsRunning():
		time.sleep(0.25)
		# Prep FrontRow to hide
		self.AboutToHideFR()

		# Hide FrontRow
		frController = BRAppManager.sharedApplication().delegate()
		self.fireMethod( frController, "_continueDestroyScene:", None )

		# Tell the app to load the file we want to open, if necessary.
		if fileToLoad is not None:
			app.open_( fileToLoad )

		# Since boxee does not appear in the app list FrontRow can't monitor/
		# Start a timer
		#self.timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "launchedAppTick:", None, True )


class RUIfrboxee( PyFR.Appliance.Appliance ):
	def getController(self):
		return BoxeeLaunch.alloc().init()






