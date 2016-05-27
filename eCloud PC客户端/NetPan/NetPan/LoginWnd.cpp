#include "StdAfx.h"
#include "LoginWnd.h"
#include "controls_ex.h"
using namespace NETPAN_WND;

CLoginWnd::CLoginWnd(LPCTSTR pszNetPanPath)
:CNetPanWnd(pszNetPanPath)
{
	m_buserislogin = false;
	m_bautomatic = false;
	m_bcAncelogin = false;
	m_bautomaticloginbool = false;
	ssl = new LoSSL;
}

CLoginWnd::~CLoginWnd()
{
	if (ssl) {
		delete ssl;
		ssl = NULL;
	}
}

void CLoginWnd::InitWindow()
{
	ssl->Initialize();
	m_PbtnReg = static_cast<CButtonUI*>(m_PaintManager.FindControl(_T("UserLink")));
	m_pbtnLogin = static_cast<CButtonUI*>(m_PaintManager.FindControl(_T("ButtonLogin")));
	m_pLab = static_cast<CLabelUI*>(m_PaintManager.FindControl(_T("UserTip")));
	m_pCom = static_cast<CComboUI*>(m_PaintManager.FindControl(_T("ComboAccount")));
	m_pUser = static_cast<CEditUI*>(m_PaintManager.FindControl(_T("EditAccount")));
	m_pPassWord = static_cast<CEditUI*>(m_PaintManager.FindControl(_T("EditPassword")));
	m_psavepassword = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("OptionRemLogin")));
	m_pautomaticlogin = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("OptionAutoLogin")));

	ReadUser();
}

CControlUI*CLoginWnd::CreateControl(LPCTSTR pstrClassName)
{
	if (_tcsicmp(pstrClassName, _T("ButtonGif")) == 0) {
		return new CButtonGifUI;
	}
	return NULL;
}

void CLoginWnd::Notify(TNotifyUI& msg)
{
	  if(msg.sType == _T("itemselect"))
	  {
		  CDuiString str = m_pCom->GetText();
		  m_pUser->SetText(str);
		  m_pPassWord->SetText(FormnameToPassword(str).c_str());
		  m_psavepassword->Selected(true);
	  }
	__super::Notify(msg);
}

LRESULT CLoginWnd::HandleMessage(UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	LRESULT lRes = __super::HandleMessage(uMsg, wParam, lParam);
	switch (uMsg)
	{
	case WM_USERLOGIN:
		{
			KillTimer(this->m_hWnd, 1);
			Login(wParam, lParam);
		}
		break;
	default:
		break;
	}
	return lRes;
}

DUI_BEGIN_MESSAGE_MAP(CLoginWnd, CNotifyPump)
DUI_ON_MSGTYPE(DUI_MSGTYPE_CLICK,OnClick)
DUI_END_MESSAGE_MAP()

void CLoginWnd::OnClick(TNotifyUI& msg)
{
	if( msg.pSender->GetName() == _T("UserLink") ) {
		//ע������
		ShellExecute(NULL, NULL, L"http://10.10.4.121:9000/", NULL, NULL, SW_NORMAL);

	} else if (msg.pSender->GetName() == _T("OptionRemLogin")) {
		//��������
		if (!m_psavepassword->IsSelected()) {
			m_buserislogin = true;
		} else {
			m_buserislogin = false;
		}

	} else if (msg.pSender->GetName() == _T("OptionAutoLogin")) {
		//�Զ���¼
		if (!m_pautomaticlogin->IsSelected()) {
			m_bautomatic = true;
		} else {
			m_bautomatic = false;
		}

	} else if (msg.pSender->GetName() == _T("CancelLogin")) {
		//ȡ����¼
		KillTimer(this->m_hWnd, 1);
		m_bcAncelogin = true;
		SwitchWind(false);

	} else if( msg.pSender->GetName() == _T("ButtonLogin") ) {
		//�����¼
		SwitchWind();
		SetTimer(this->m_hWnd, 1, 2000, SendLoginWM);
	}

	__super::OnClick(msg);
}

LRESULT CLoginWnd::OnNcHitTest(UINT uMsg, WPARAM wParam, LPARAM lParam, BOOL& bHandled)
{
	return __super::OnNcHitTest(uMsg, wParam, lParam, bHandled);
}

void CLoginWnd::SendLoginWM(HWND hwnd, UINT uMsg, UINT_PTR idEvent, DWORD dwTime )
{
	::PostMessage(hwnd, WM_USERLOGIN, NULL, NULL);
	
}

void CLoginWnd::Login(WPARAM wParam, LPARAM lParam)
{
	m_bcAncelogin = false;
	m_buserislogin = true;
	//�û���¼
	if (!m_bcAncelogin) {
		CString userdata;
		userdata.Empty();
		////�����û���Ϣ,����д�������ļ�
		m_szuser = m_pUser->GetText();
		m_szpasswrod = m_pPassWord->GetText();
		//userdata.Format(L"login %s %s\n", m_user, m_passwrod);
		////socket���ӷ���ͻ��˱���socket
		//bool ret = ssl->Connect("10.10.4.66", 4002);

		//if (!ret) {
		//	MessageBox(NULL, L"�����쳣���޷����ӵ�������", L"�û���¼", MB_OK);
		//} else {

		//	if (LoginSSL(userdata)) {
				LoginISRight(true);
			/*} else {
				MessageBox(NULL, L"��������������ʧ��", L"�û���¼", MB_OK);
			}

		}*/
	}
	
}

bool CLoginWnd::LoginISRight(bool Flag)
{
	/*CDuiString temp(_T("test003"));
	WriteConfigFile();

	this->Close();

	CMainUIWnd* pSet = new CMainUIWnd(_T("UISkin.xml"));
	pSet->SetUserWnd(temp);
	pSet->Create(NULL, _T("����"), UI_WNDSTYLE_FRAME, WS_EX_WINDOWEDGE | WS_EX_ACCEPTFILES);
	pSet->CenterWindow();
	pSet->ShowModal();
	delete pSet;
	pSet = NULL;*/

	MessageBox(m_hWnd, L"���ӷ���������", L"���Ӵ���", MB_OK);
	SwitchWind(false);

	return true;
}

bool CLoginWnd::LoginSSL(CString usrdata)
{
	unsigned int cmd_len = usrdata.GetLength()+1;
	char* senddata = new char[cmd_len];
	WideCharToMultiByte(CP_ACP, 0, usrdata.GetBuffer(), -1, senddata, usrdata.GetLength()+1, NULL, NULL);

	if (ssl->Write((unsigned char*)senddata, cmd_len) != cmd_len) {
		MessageBox(NULL, _T("ERR_SSL_WRITE"), _T("ERROR"), MB_OK);
		return false;
	}

	if (!Verry_Data(senddata, cmd_len)) {
		MessageBox(NULL, _T("�û������������"),_T("ERROR"),MB_OK);
		return false;
	}

	if (senddata) {
		delete senddata;
		senddata = NULL;
	}

	return true;
}

bool CLoginWnd::Verry_Data(char* buf, unsigned int &length)
{
	unsigned char info[6] = {0};
	if (ssl->Read(info, 6) != 6) {
		return false;
	}
	if (info[0] != '#') {
		return false;
	}
	length = *(unsigned int*)(info+2);

	if (ssl->Read((unsigned char*)buf, length) != length) {
		return false;
	}

	if (info[1]) {
		return true;
	}
	return false;
}

bool CLoginWnd::QurreyUser(LPCTSTR username)
{
	//��ǰ�û��Ƿ��������û���ֻ�������û��Ŵ����Զ���¼�޸�
	if (!m_Valluserdata.empty()) {
		vector<wstring>::size_type i = 0;
		if (m_Valluserdata[i] == username) {
			return true;
		}
	}
	return false;
}

void CLoginWnd::WriteConfigFile()
{
	if (m_buserislogin && (m_szuser != "")) {
		TCHAR count[10] = {0};
		int usercount;
		::GetPrivateProfileString(USER, COUNT, L"", count, sizeof(count), FILEPATH);
		usercount = _ttoi(count);

		if (!QurreyUser(m_szuser)) {
			usercount++;
		}

		CString temp;
		temp.Format(L"%d", usercount);

		if (m_bautomatic) {
			::WritePrivateProfileString(USER, temp+AUTOMATIC, L"true", FILEPATH);
		} else {
			::WritePrivateProfileString(USER, temp+AUTOMATIC, L"false", FILEPATH);
		}

		::WritePrivateProfileString(USER, COUNT, temp, FILEPATH);
		::WritePrivateProfileString(USER, temp+USER, m_szuser, FILEPATH);
		::WritePrivateProfileString(USER, temp+PASSWORD, m_szpasswrod, FILEPATH);
		
	}
}

void CLoginWnd::ReadConfigFile(vector<string_t>& alluser, vector<string_t>& allpassword)
{
	TCHAR count[10] = {0};
	int usercount;
	::GetPrivateProfileString(USER, COUNT, L"", count, sizeof(count), FILEPATH);
	usercount = _ttoi(count);

	//�����ȡ����ȡ���һ�ε�¼
	bool lastest = true;
	for (int i = usercount; i > 0; i--)
	{
		CString temp;
		temp.Format(L"%d", i);
		TCHAR user[50] = {0};
		TCHAR password[50] = {0};
		TCHAR automatic[50] = {0};

		if (lastest) {
			::GetPrivateProfileString(USER, temp+AUTOMATIC, L"", automatic, sizeof(automatic), FILEPATH);
			if (_tcsicmp(automatic, L"true") == 0) {
				m_bautomaticloginbool = true;
			} else {
				m_bautomaticloginbool = false;
			}
			lastest = false;
		}
		::GetPrivateProfileString(USER, temp+USER, L"", user, sizeof(user), FILEPATH);
		::GetPrivateProfileString(USER, temp+PASSWORD, L"", password, sizeof(password), FILEPATH);
		allpassword.push_back(password);
		alluser.push_back(user);
	}
}

void CLoginWnd::ReadUser()
{
	ReadConfigFile(m_Valluserdata, m_Vallpassworddata);
	
	for (vector<string_t>::iterator it = m_Valluserdata.begin(); it != m_Valluserdata.end(); it++) 
	{
		CListLabelElementUI * pListElement = new CListLabelElementUI;
		pListElement->SetText((*it).c_str());
		m_pCom->Add(pListElement);
	}

	//�����һ���û������Զ���¼,���¼
	if (m_bautomaticloginbool) {
		vector<string_t>::iterator ite = m_Valluserdata.begin();
		string_t firstuser = *ite;
		m_pUser->SetText(firstuser.c_str());
		m_pPassWord->SetText(FormnameToPassword(firstuser.c_str()).c_str());
		m_psavepassword->Selected(true);
		m_pautomaticlogin->Selected(true);
		m_bautomatic = true;

		SwitchWind();
		SetTimer(this->m_hWnd, 1, 2000, SendLoginWM);
	}
}

string_t CLoginWnd::FormnameToPassword(LPCTSTR name)
{
	for (vector<wstring>::size_type i = 0; i != m_Valluserdata.size(); i++)
	{
		if (m_Valluserdata[i] == name) {
			return m_Vallpassworddata[i];
		}
	}
	return wstring(L"");
}

void CLoginWnd::SwitchWind(bool dlg /* = true */)
{
	//dlgΪtrue��ʾ��½�����л���dlgΪfalse��ʾͣ���л�
	CControlUI *pbtcancel = m_PaintManager.FindControl(_T("ContainerCancelLogin"));
	CControlUI *pbtlogin = m_PaintManager.FindControl(_T("ContainerForLogin"));
	
	if (dlg) {
		pbtcancel->SetVisible(true);
		pbtlogin->SetVisible(false);
	} else {
		pbtcancel->SetVisible(false);
		pbtlogin->SetVisible(true);
	}
}