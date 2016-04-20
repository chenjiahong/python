
On Error Resume Next
set pptApp = CreateObject("powerpoint.application")
pptApp.visible = true
dim a
a = 0
Set fso = CreateObject("Scripting.FileSystemObject")
set resFile = fso.createtextfile("d:\openFailed.txt")
set fd = fso.getfolder("D:\save_as")
SearchFolder fd:OpenFileInFolder fd
resFile.close
pptApp.Quit
MsgBox a

Sub SearchFolder(folder)
	On Error Resume Next
	Dim i
	For Each i In folder.SubFolders
	OpenFileInFolder i
	Next
	set subFolders = folder.subfolders
	for each subFolder in subFolders
		SearchFolder subFolder
	next
End Sub

Sub OpenFileInFolder(fol)
	On Error Resume Next
	Dim i
	For Each i In fol.Files
	If LCase(fso.GetExtensionName(i)) = "pptx" or LCase(fso.GetExtensionName(i)) = "ppt" Then
	dim absName
	absName	= fso.GetAbsolutePathName(i)
	OpenPresentaion absName
	End If
	Next
End Sub

Sub OpenPresentaion(absName)
	On Error Resume Next
	if pptApp is nothing then
	set pptApp = CreateObject("powerpoint.application")
	pptApp.visible = true
	end if
	set currPres = pptApp.Presentations.Open(absName)
	if currPres is nothing Then
	'MsgBox absName & " open fialed!"
	resFile.writeLine absName
	exit Sub
	end if	
	a = a + 1
	currPres.Close
End Sub