#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

import os 
import time 
import threading

# Import backrow
objc.loadBundle("BackRow", globals(), bundle_path=objc.pathForFramework("/System/Library/PrivateFrameworks/BackRow.framework" ))

# Logging.
def log(s):
    Foundation.NSLog( "FrontMyth: %s" % str(s) )


key = u"com.apple.frontrow.appliance.boxee"


# this class is the glue that allows us to be loaded by frontrow.
# If you want to create you own plugins, the only thing you need to change is 
# the applianceController method. 
class RUIPythonAppliance( BRAppliance ):

    sanityCheck = False

    @classmethod
    def initialize(cls):
        name = NSString.alloc().initWithString_( key )
        BRFeatureManager.sharedInstance().enableFeatureNamed_( name )

    @classmethod
    def className(cls):

        clsName = NSString.alloc().initWithString_( cls.__name__ )

        backtrace = BRBacktracingException.backtrace()
        range = backtrace.rangeOfString_( "_loadApplianceInfoAtPath:" )

        if range.location == Foundation.NSNotFound and cls.sanityCheck == False:
            range = backtrace.rangeOfString_( "(in BackRow)" )
            cls.sanityCheck = True
        
        if range.location != Foundation.NSNotFound:
            clsName = NSString.alloc().initWithString_( "RUIMoviesAppliance" )

        return clsName

    def applianceController(self):
        return MythPlugin.alloc().init()


class MythPlugin(BRController):


    def __setupText(self):
        ''' Set up the text field '''
        attribs = BRThemeInfo.sharedTheme().paragraphTextAttributes()
        self.textController = BRHeaderControl.alloc().init()
        self.textController.setTitle_( u"Loading Boxee" )

        # There's probably a better way to do this,
        masterFrame = BRRenderScene.singleton().size()
        w = masterFrame[0]
        h = masterFrame[1]

        origin = ( 0, 
                   (h * 0.5))

        size = ( w, h * 0.25 )
        

        # Where it goes, and how big
        self.textController.setFrame_( ( origin, size ) )

        self.addControl_(self.textController)

    def __setupSpinner(self):
        self.spinner = BRWaitSpinnerControl.alloc().init()
        self.spinner.controlWasActivated()

        masterFrame = BRRenderScene.singleton().size()

        log(masterFrame)
        w = masterFrame[0]
        h = masterFrame[1]

        origin = (w*0.25, 0)
        size = (w*0.5, h*0.5)

        self.spinner.setFrame_( ( origin, size ) )

        self.addControl_(self.spinner)

    def init(self):
        BRController.init(self)

        self.__setupText()
        self.__setupSpinner()

        return self

    def wasPushed(self):

	# Get FR out of the way. Boy was this fun trying to figure out.
        frController = BRAppManager.sharedApplication().delegate()
        frController._hideFrontRow()

        # Load Myth
        ws = NSWorkspace.sharedWorkspace()
        ws.launchApplication_( "/Applications/Boxee.app/Contents/MacOS/Boxee" )
        
        # wait for Myth to launch
        found = True
        while not found:
            # I probably shouldn't use a sleep here, as thats not good GUI 
            # practice. But it works. Not like its going to be around long in 
            # here.
            time.sleep(.5)

            # check the list of launched app to see if Myth has finished loading.
            for app in NSWorkspace.sharedWorkspace().launchedApplications():
        
                if app['NSApplicationName'] == "BOXEE":
                    found = True
                    break
            if found:
                break

        
        
        # Start a timer
        #self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "tick:", None, True )

        # Make sure to call the parent!
        BRController.wasPushed(self)

    def tick_(self, senders):

        # Check to see if Myth is running.
        found = False
        for app in NSWorkspace.sharedWorkspace().launchedApplications():
            if app['NSApplicationName'] == "BOXEE":

                # Is it the active app?
                ws = NSWorkspace.sharedWorkspace()

                activeApp = ws.activeApplication()
                if activeApp['NSApplicationName'] != "BOXEE":

                    # ping it, so it becomes active.
                    # Why do we do this you ask? Well.. When we hide front row
                    # above, it brings the last active application to the front.
                    # Why? I don't know.
                    ws.launchApplication_( "/Applications/Boxee.app" )

                return

        # If we don't find Myth running, then we exited. So bring FR back.
        if not found:
            frController = BRAppManager.sharedApplication().delegate()
            frController._showFrontRow()

            # Make sure to turn off the timer!
            self.timer.invalidate()



        






