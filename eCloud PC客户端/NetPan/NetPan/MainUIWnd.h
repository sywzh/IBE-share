#pragma once
#include "duilib.h"
#include "NetDiskWnd.h"
#include "MenuFileList.h"
#include "MenuSetting.h"
#include "OpenFile.h"
using namespace NETPAN_TOOL;
namespace NETPAN_WND {

	class CMainUIWnd :public CNetPanWnd
	{
	public:
		explicit CMainUIWnd(LPCTSTR pszNetPanPath);
		~CMainUIWnd(void);
		virtual CControlUI* CreateControl( LPCTSTR pstrClassName );
		virtual void Notify( TNotifyUI& msg );
		virtual void OnClick(TNotifyUI& msg);
		virtual void InitWindow();
		DUI_DECLARE_MESSAGE_MAP()

	public:
		enum DLG {
			DLG_START = 0L,
			DLG_END = 1L
		};

		enum Wnd {
			Wnd_NULL,
			Wnd_MYDISK,
			Wnd_TRANTS
		};

		enum STATUS {
			FILE_DOWN = 0L,
			FILE_UP = 1L,
			FILE_SUCCED = 2L
		};

		enum RETURN {
			SUCCED = 0L
		};

	public:
		void SetUserWnd();
		void SetUserWnd(CDuiString wnd_name);

	private:
		//activex
		void AddActiveX();
		//文件封装函数
		BOOL InitTreeControl();
		void ListAddFile(CDuiString fname, CDuiString ftype, CDuiString fsize, CDuiString fdate = L"");
		//使用前，请先设置其text属性
		void SetLabelName(CLabelUI* plabel, CDuiString textname, CDuiString filename);
		void AddPro(CButtonUI* pbut, CProgressUI* pros, CLabelUI* pname, CLabelUI* pspeed, CLabelUI* ptime);
		void ListAddProgress(STATUS staus, CButtonUI* pbut, CProgressUI* pros, CLabelUI* pname, CLabelUI* pspeed, CLabelUI* ptime);

		//对话框窗口函数
		
		void BeginThread(DLG nMode);
		static UINT AlphaDlg(LPVOID pParam);

		RETURN SwitchDlg(bool btn = true);

	private:
		Wnd m_eWnd;

		CDuiString m_strUserWnd;

	protected:

		CListUI* m_FileList;
		CTreeViewUI *m_pDirTree;
		//传输管理
		CTreeViewUI* m_pSendTree;
		CListUI* m_pSendFileList;

	};

	typedef  struct ThreaData {
		CMainUIWnd* pDlg;
		CMainUIWnd::DLG nMode;
		static bool bAlphaThreadOK;
	}THREADATA;
}
