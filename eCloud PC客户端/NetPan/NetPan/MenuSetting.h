#pragma once
#include "duilib.h"

namespace NETPAN_WND {

	class CMenuSetting :public CNetPanWnd
	{
	public:
		explicit CMenuSetting(LPCTSTR pszNetPanPath);
		virtual LRESULT OnKillFocus(UINT uMsg, WPARAM wParam, LPARAM lParam, BOOL& bHandled);
		void Init(CPaintManagerUI *pOwnerPM, POINT ptPos,CControlUI* pOwner);
		virtual LRESULT HandleMessage(UINT uMsg, WPARAM wParam, LPARAM lParam);
		virtual void Notify( TNotifyUI& msg );
	protected:
		virtual ~CMenuSetting(void);
	private:
		CPaintManagerUI *m_pOwnerPM;
		CControlUI* m_POwner;
	};

}

