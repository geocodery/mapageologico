Dim sInput
sInput = InputBox("Add Python path for ArcGIS", "Setup MG 1:50000")
Set fso = CreateObject("Scripting.FileSystemObject")
Set oShell = CreateObject("WScript.Shell")

exists = fso.FolderExists(sInput)

if NOT (sInput=False) then
	if exists then
		oShell.CurrentDirectory = sInput
		cmd_01 = "cmd /K python \\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\install\modules\get-pip.py"
		cmd_02 = " & cd /d Scripts"
		cmd_03 = " & pip install -U -r \\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\install\requirements.txt"
		cmd_04 = " & exit"
		Command = cmd_01&cmd_02&cmd_03&cmd_04
		oShell.Run Command,1,True
	else
		MsgBox ("No such directory: " & sInput)
	end if
end if
