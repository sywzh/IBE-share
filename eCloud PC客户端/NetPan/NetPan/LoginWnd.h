#pragma once
#include "duilib.h"
#include "SetWnd.h"
#include "MainUIWnd.h"
#include "LoSSL.h"
#include <string>
#include <atlstr.h>
#include <vector>
using namespace std;

#define USER L"USER"
#define COUNT L"COUNT"
#define USERID L"USERID"
#define PASSWORD L"PASSWORD"
#define AUTOMATIC L"AUTOMATIC"
static const TCHAR* FILEPATH = L"C:\\Users\\user.ini";
#define WM_USERLOGIN WM_USER+20

using namespace NETPAN_TOOL;
namespace NETPAN_WND{

	class CLoginWnd :
		public CNetPanWnd
	{
	public:
		explicit  CLoginWnd(LPCTSTR pszNetPanPath);
		~CLoginWnd(void);
		virtual void InitWindow();
		virtual CControlUI* CreateControl(LPCTSTR pstrClassName);
		virtual void Notify(TNotifyUI& msg);
		virtual LRESULT HandleMessage(UINT uMsg, WPARAM wParam, LPARAM lParam);
		virtual void OnClick(TNotifyUI& msg);
		virtual LRESULT OnNcHitTest(UINT uMsg, WPARAM wParam, LPARAM lParam, BOOL& bHandled);

		bool LoginISRight(bool Flag);
		bool Verry_Data(char* buf, unsigned int &length);
		bool LoginSSL(CString usrdata);

		void SwitchWind(bool dlg = true);

		string_t FormnameToPassword(LPCTSTR name);
		bool QurreyUser(LPCTSTR username);
		void ReadUser();
		void WriteConfigFile();
		void ReadConfigFile(vector<wstring>& alluser, vector<wstring>& allpassword);

		static void CALLBACK SendLoginWM(HWND hwnd, UINT uMsg, UINT_PTR idEvent, DWORD dwTime );
		void Login(WPARAM wParam, LPARAM lParam);
		DUI_DECLARE_MESSAGE_MAP()

	private:
		bool m_buserislogin;
		bool m_bautomatic;
		bool m_bautomaticloginbool;
		bool m_bcAncelogin;
		LoSSL* ssl;
		CButtonUI * m_PbtnReg;
		CButtonUI* m_pbtnLogin;
		CLabelUI* m_pLab;
		CComboUI* m_pCom;
		COptionUI* m_psavepassword;
		COptionUI* m_pautomaticlogin;
		CEditUI* m_pUser;
		CEditUI* m_pPassWord;
		CString m_szuser;
		CString m_szpasswrod;
		vector<string_t> m_Valluserdata;
		vector<string_t> m_Vallpassworddata;
	};

}
