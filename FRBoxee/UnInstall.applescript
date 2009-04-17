try
  do shell script "/bin/rm -rf /System/Library/CoreServices/Front\\ Row.app/Contents/PlugIns/RunBoxee.frappliance" with administrator privileges

  --terminate Front Row so that it will pick up changes
  do shell script "killall Front\\ Row 2>/dev/null; /usr/bin/true"

  display dialog "FRBoxee uninstalled" buttons {"Ok"}

on error
  display dialog "Error uninstalling FRBoxee." buttons {"Weird"}
end try


