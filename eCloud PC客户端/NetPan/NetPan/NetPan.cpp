// NetPan.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "duilib.h"
#include <windows.h>
#include <tchar.h>
#include "LoginWnd.h"

using namespace NETPAN_WND;
int APIENTRY _tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	HRESULT hr = ::CoInitialize(NULL);
	CPaintManagerUI::SetInstance(hInstance);
	CPaintManagerUI::SetResourcePath(CPaintManagerUI::GetInstancePath() + _T("skin"));

	CLoginWnd pFrame(_T("Login.xml"));
	pFrame.Create(NULL, _T("����"), UI_WNDSTYLE_FRAME, WS_EX_WINDOWEDGE | WS_EX_ACCEPTFILES);
	pFrame.CenterWindow();
	pFrame.ShowModal();
	::CoUninitialize();
	return 0;
}

