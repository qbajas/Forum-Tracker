;NSIS Modern User Interface
;Basic Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Forum Tracker Client"
  OutFile "setup.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\Forum Tracker Client"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Forum Tracker Client" "InstDir"

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin
  
;--------------------------------

  Var StartMenuFolder

;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "licencja.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY

 ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Forum Tracker Client" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "Polish"

;--------------------------------
;Installer Sections


Section "Forum Tracker Client (wymagane)" ForumTrackerClient
  
  SectionIn RO
  SetOutPath "$INSTDIR"
  

  
  
  
  ;ADD YOUR OWN FILES HERE...
  File "dist\msvcp90.dll"
  File "dist\client.exe"
  File "dist\splash.png"
  File "dist\icon.ico"
  
  ; Write the installation path into the registry
  WriteRegStr HKCU "Forum Tracker Client" "InstDir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Forum Tracker Client" "DisplayName" "Forum Tracker Client"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Forum Tracker Client" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Forum Tracker Client" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Forum Tracker Client" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  ;Create shortcuts
  CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Forum Tracker Client.lnk" "$INSTDIR\client.exe" "" "$INSTDIR\icon.ico"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Usuñ.lnk" "$INSTDIR\Uninstall.exe"
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd


Section "Skrót na pulpicie" Skrot
  CreateShortCut "$DESKTOP\Forum Tracker Client.lnk" "$INSTDIR\client.exe" "" "$INSTDIR\icon.ico"
SectionEnd
;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_ForumTrackerClient ${LANG_POLISH} "Program Forum Tracker Client."
  LangString DESC_Skrot ${LANG_POLISH} "Skrót na pulpicie do aplikacji."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${ForumTrackerClient} $(DESC_ForumTrackerClient)
	!insertmacro MUI_DESCRIPTION_TEXT ${Skrot} $(DESC_Skrot)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete $INSTDIR\w9xpopen.exe
  Delete $INSTDIR\client.exe
  Delete $INSTDIR\splash.png
  Delete $INSTDIR\icon.ico
  
  Delete "$INSTDIR\uninstall.exe"

  RMDir "$INSTDIR"

  DeleteRegKey HKCU "Software\Forum Tracker Client"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Forum Tracker Client"

  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder  
  Delete "$SMPROGRAMS\$StartMenuFolder\Forum Tracker Client.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Usuñ.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"
  Delete "$DESKTOP\Forum Tracker Client.lnk"
  
SectionEnd