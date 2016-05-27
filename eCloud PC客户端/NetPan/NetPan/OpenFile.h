#pragma once
#include "duilib.h"

namespace NETPAN_TOOL {
	class COpenFile
	{
	public:
		TCHAR szPathName[MAX_PATH];  
		COpenFile(void)
		{
			memset(szPathName,0,sizeof(szPathName));
		}
		BOOL Openfile()
		{
			OPENFILENAME ofn = { OPENFILENAME_SIZE_VERSION_400 }; 
			ofn.hwndOwner =GetForegroundWindow();
			ofn.lpstrFilter = NULL;   
			lstrcpy(szPathName, TEXT(""));  
			ofn.lpstrFile = szPathName;  
			ofn.nMaxFile = sizeof(szPathName);
			ofn.lpstrTitle = TEXT("Ñ¡ÔñÎÄ¼þ");
			TCHAR szCurDir[MAX_PATH];  
			GetCurrentDirectory(sizeof(szCurDir),szCurDir);  
			ofn.lpstrInitialDir=szCurDir;
			ofn.Flags = OFN_EXPLORER |OFN_ALLOWMULTISELECT| OFN_FILEMUSTEXIST;
			_tprintf(TEXT("select file/n"));  
			BOOL bOk = GetOpenFileName(&ofn);
			if (bOk)  
			{  
				return TRUE;
			} 
			else
			{
				return FALSE;
			}
		}
		CDuiString GetFilePath()
		{
			CDuiString str;
			str.Format(_T("%s"),szPathName);
			return str;
		}
	};


}
