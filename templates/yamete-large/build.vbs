Set oShell = WScript.CreateObject("WScript.Shell")
oShell.Run "cmd /c tar -cf LogiSound.dat config.ini yamete_large.png yamete_large.mp3", 0, True
