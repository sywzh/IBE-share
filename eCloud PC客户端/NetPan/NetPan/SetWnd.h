#pragma once
#include "duilib.h"
namespace NETPAN_WND {
	class CSetWnd :public CNetPanWnd
	{
	public:
		explicit CSetWnd(LPCTSTR pszNetPanPath);
		~CSetWnd(void);
		CControlUI* CreateControl( LPCTSTR pstrClassName );
		virtual void Notify( TNotifyUI& msg );
	};
}

