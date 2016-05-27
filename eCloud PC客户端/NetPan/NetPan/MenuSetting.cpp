#include "StdAfx.h"
#include "MenuSetting.h"
#include "SetWnd.h"

using namespace NETPAN_WND;
CMenuSetting::CMenuSetting(LPCTSTR pszNetPanPath)
:CNetPanWnd(pszNetPanPath)
{
}

CMenuSetting::~CMenuSetting(void)
{
}

LRESULT CMenuSetting::OnKillFocus(UINT uMsg, WPARAM wParam, LPARAM lParam, BOOL& bHandled)
{
	Close();
	bHandled = FALSE;
	return 0;
}
void CMenuSetting::Init(CPaintManagerUI *pOwnerPM, POINT ptPos,CControlUI* pOwner)
{
	if( pOwnerPM == NULL ) 
	{
		return;
	}
	m_pOwnerPM = pOwnerPM;
	m_POwner = pOwner;
	Create(pOwnerPM->GetPaintWindow(), _T("MenuWnd"), UI_WNDSTYLE_FRAME, WS_EX_WINDOWEDGE);
	::ClientToScreen(pOwnerPM->GetPaintWindow(), &ptPos);
	::SetWindowPos(*this, NULL, ptPos.x, ptPos.y, 0, 0, SWP_NOZORDER | SWP_NOSIZE | SWP_NOACTIVATE);
}
 LRESULT CMenuSetting::HandleMessage(UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	LRESULT lRes = 0;
	BOOL    bHandled = TRUE;

	switch( uMsg )
	{
	case WM_KILLFOCUS:    
		lRes = OnKillFocus(uMsg, wParam, lParam, bHandled); 
		break; 
	default:
		bHandled = FALSE;
	}
	if(bHandled || m_PaintManager.MessageHandler(uMsg, wParam, lParam, lRes)) 
	{
		return lRes;
	}
	return __super::HandleMessage(uMsg, wParam, lParam);
}
 void CMenuSetting::Notify( TNotifyUI& msg )
 {
	 if( msg.sType == _T("itemselect") ) {
		 Close();
	 }
	 else if( msg.sType == _T("itemclick") ) 
	 {
		 if( msg.pSender->GetName() == _T("menu_setting") ) 
		 {
			 CSetWnd* pSet = new CSetWnd(_T("SettingSkin.xml"));
			 pSet->Create(NULL, _T("ÉèÖÃ"), UI_WNDSTYLE_FRAME, WS_EX_WINDOWEDGE | WS_EX_ACCEPTFILES);
			 pSet->CenterWindow();
			 pSet->ShowModal();
			 delete pSet;
			 //if( m_POwner ) m_POwner->GetManager()->SendNotify(m_POwner, _T("menu_delete"), 0, 0, true);
		 }
	 }
	 __super::Notify(msg);
 }
