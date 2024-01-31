Set FSO = CreateObject("Scripting.FileSystemObject")
TargetPath = FSO.GetFile("LogiSound.exe").ShortPath
WorkingDirectory = FSO.GetFolder(FSO.GetParentFolderName(TargetPath)).ShortPath
Set lnk = CreateObject("WScript.Shell").CreateShortcut(WScript.CreateObject("WScript.Shell").SpecialFolders("Startup") & "\LogiSound.lnk")
    lnk.TargetPath = TargetPath
    lnk.WorkingDirectory = WorkingDirectory
    On Error Resume Next 'Enable error handling
    lnk.Save 'Try to save the shortcut
    If Err.Number <> 0 Then 'Check if an error occurred
        MsgBox "Error: " & Err.Description, vbCritical, "Failed to create shortcut." 'Show an error message
        Err.Clear 'Clear the error
    Else
        MsgBox "Setup completed successfully.", vbInformation, "Setup completed" 'Show a success message
    End If
    On Error Goto 0 'Disable error handling
