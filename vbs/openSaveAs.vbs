set wppApp = CreateObject("kwpp.application")
wppApp.visible = true

dim a
a = 0
Set fso = CreateObject("Scripting.FileSystemObject")
set fd = fso.getfolder("D:\foundFile") '在这里修改文件夹地址
SearchFolder fd:OpenFileInFolder FD
msgbox a

wppApp.Quit()

Sub SearchFolder(folder)
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
  Dim i
  dim saveDir
  saveDir = "D:\save_as"
  For Each i In fol.Files
    If LCase(fso.GetExtensionName(i)) = "pptx" or LCase(fso.GetExtensionName(i)) = "ppt" Then
	a = a + 1
	dim absName
	absName	= fso.GetAbsolutePathName(i)
	dim fileName
	fileName = fso.GetBaseName(i)
	OpenPresentaion absName, saveDir, fileName
	End If
  Next
End Sub

Sub OpenPresentaion(absName, saveDir, fileName)
	set res	= wppApp.Presentations.Open(absName)
	if res is nothing Then
	MsgBox wppApp.Name & " open fialed!"
	return
	end if
	dim newPath
	newPath = saveDir & "\" & fileName & ".pptx"
	with wppApp.ActivePresentation
	.SaveAs newPath, ppSaveAsOpenDocumentPresentation
	end with
	wppApp.ActivePresentation.Close
End Sub
