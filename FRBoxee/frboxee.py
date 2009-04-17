#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
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
		#self.initWithApp_( self, 'Launching Boxee', 'Applications/Boxee.app' )
		PyFR.WaitController.WaitController.initWithText_( self, 'Launching Boxee' )
		return self

	def PyFR_start(self):
		self.launchApp( 'Applications/LaunchBoxee.app', None )
		#self.launchApp( 'System/Library/CoreServices/Front\ Row.app/Contents/PlugIns/RunBoxee.frappliance/Contents/MacOS/LaunchBoxee.app', None )
		#self.launchApp( '/Applications/Boxee.app/Contents/MacOS/Boxee', None )
        # FR automatically quits after 20 minutes.  This should disable that behavior...
        #   not tested here, you might need to do this a few seconds into your AppShouldExit callback
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

		# possibly Load App
		#while not self.__IsRunning():

			# I probably shouldn't use a sleep here, as thats not good GUI 
			# practice. But it works. Not like its going to be around long in 
			# here.
		time.sleep(0.25)

		# Well, we already hid, so we may move this. 
		self.AboutToHideFR()

		# Start hiding the display
		frController = BRAppManager.sharedApplication().delegate()
		# We use continue, since it seems to skip the -slow- fade out.
		# It also doesn't seem to kill the controller stack!
		self.fireMethod( frController, "_continueDestroyScene:", None )

		# Tell the app to load the file we want to open, if necessary.
		if fileToLoad is not None:
			app.open_( fileToLoad )

		# Start a timer
		#self.timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "launchedAppTick:", None, True )


class RUIfrboxee( PyFR.Appliance.Appliance ):
	def getController(self):
		return BoxeeLaunch.alloc().init()






