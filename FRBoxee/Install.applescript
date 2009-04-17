-- uninstall old version
try
  do shell script "/bin/rm -rf /System/Library/CoreServices/Front\\ Row.app/Contents/PlugIns/Boxee.frappliance" with administrator privileges
end try
try
  do shell script "/bin/rm -rf /System/Library/CoreServices/Front\\ Row.app/Contents/PlugIns/RunBoxee.frappliance" with administrator privileges
end try

--install new version
tell application "Finder"
	set path_ to (folder of file (path to me)) as string
	set path_ to POSIX path of path_
end tell
do shell script "cp -Rfp " & path_ & "/RunBoxee.frappliance /System/Library/CoreServices/Front\\ Row.app/Contents/PlugIns" with administrator privileges
do shell script "cp -Rfp " & path_ & "/LaunchBoxee.app /Applications" with administrator privileges

--copy icon from Boxee application
try
  do shell script "cp /Applications/Boxee.app/Contents/Resources/Boxee.icns /System/Library/CoreServices/Front\\ Row.app/Contents/PlugIns/Boxee.frappliance/Contents/Resources/ApplianceIcon.png" with administrator privileges
on error
  display dialog "Could not find Boxee icon, you won't have a pretty Boxee icon."
end try

--terminate Front Row so that it will pick up changes
do shell script "killall Front\\ Row 2>/dev/null; /usr/bin/true"

display dialog "FRBoxee is now installed.


