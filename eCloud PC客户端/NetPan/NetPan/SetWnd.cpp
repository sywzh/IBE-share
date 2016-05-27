#include "StdAfx.h"
#include "SetWnd.h"
using namespace NETPAN_WND;
CSetWnd::CSetWnd(LPCTSTR pszNetPanPath)
:CNetPanWnd(pszNetPanPath)
{
}
CSetWnd::~CSetWnd(void)
{
}
CControlUI* CSetWnd::CreateControl( LPCTSTR pstrClassName )
{
	CDuiString     strXML;
	CDialogBuilder builder;

	if (_tcsicmp(pstrClassName, _T("NormalPage")) == 0)
	{
		strXML = _T("NormalSkin.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("AccountPage")) == 0)
	{
		strXML = _T("AccountSkin.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("NetPage")) == 0)
	{
		strXML = _T("NetSkin.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("CachePage")) == 0)
	{
		strXML = _T("CacheSkin.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("VIPPage")) == 0)
	{
		strXML = _T("VIPSkin.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("LoginSettingPage")) == 0)
	{
		strXML = _T("LoginSettingSkin.xml");
	}
	if (! strXML.IsEmpty())
	{
		CControlUI* pUI = builder.Create(strXML.GetData(), NULL, NULL, &m_PaintManager, NULL); 
		return pUI;
	}
	return NULL;
}
void CSetWnd::Notify( TNotifyUI& msg )
{
	if(msg.sType == _T("selectchanged"))
	{
		CDuiString    strName   = msg.pSender->GetName();
		CTabLayoutUI* pControl = static_cast<CTabLayoutUI*>(m_PaintManager.FindControl(_T("switch")));
		if(strName == _T("OptNormal"))
			pControl->SelectItem(0);
		else if(strName == _T("OptAccount"))
			pControl->SelectItem(1);
		else if(strName == _T("OptNet"))
			pControl->SelectItem(2);
		else if(strName == _T("OptVIP"))
			pControl->SelectItem(3);
		else if(strName == _T("OptCache"))
			pControl->SelectItem(4);
		else if(strName == _T("OptLoginSetting"))
			pControl->SelectItem(5);
	}
	__super::Notify(msg);
}
