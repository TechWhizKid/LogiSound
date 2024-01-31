Set oShell = WScript.CreateObject("WScript.Shell")
oShell.Run "cmd /c tar -cf LogiSound.dat config.ini yamete_mini.png yamete_mini.mp3", 0, True
