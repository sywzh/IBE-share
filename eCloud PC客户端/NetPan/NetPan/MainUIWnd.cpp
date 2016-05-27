#include "StdAfx.h"
#include "MainUIWnd.h"

using namespace NETPAN_WND;

bool ThreaData::bAlphaThreadOK = true;
CMainUIWnd::CMainUIWnd(LPCTSTR pszNetPanPath)
:CNetPanWnd(pszNetPanPath)
{
	m_eWnd = CMainUIWnd::Wnd_NULL;
}

CMainUIWnd::~CMainUIWnd(void)
{
}
CControlUI* CMainUIWnd::CreateControl( LPCTSTR pstrClassName )
{
	CDuiString     strXML;
	CDialogBuilder builder;

	if (_tcsicmp(pstrClassName, _T("HomePage")) == 0)
	{
		strXML = _T("HomePage.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("MyNetDisk")) == 0)
	{
		strXML = _T("MyNetDisk.xml");
	}
	else if (_tcsicmp(pstrClassName, _T("TransStatus")) == 0)
	{
		strXML = _T("TransStatus.xml");
	}
	if (! strXML.IsEmpty())
	{
		CControlUI* pUI = builder.Create(strXML.GetData(), NULL, NULL, &m_PaintManager, NULL); 
		return pUI;
	}
	return NULL;
}

void CMainUIWnd::Notify( TNotifyUI& msg )
{
	if(msg.sType == _T("selectchanged"))
	{
		CDuiString    strName   = msg.pSender->GetName();
		CTabLayoutUI* pControl = static_cast<CTabLayoutUI*>(m_PaintManager.FindControl(_T("switch")));
		
		
		if(strName == _T("homepage")) {
			pControl->SelectItem(0);
			m_eWnd = CMainUIWnd::Wnd_NULL;
		} else if(strName == _T("mynetdisk")) {
			pControl->SelectItem(1);
			m_eWnd = CMainUIWnd::Wnd_MYDISK;
		} else if(strName == _T("transstatus")) {
			pControl->SelectItem(2);
			m_eWnd = CMainUIWnd::Wnd_TRANTS;
		}
	}
	else if(msg.sType == _T("menu"))
	{
		 if( msg.pSender->GetName() != _T("TreeFileList") ) return;
		 POINT pt = {msg.ptMouse.x, msg.ptMouse.y};
		 ::ClientToScreen(*this, &pt);
		 CMenuWnd *pMenu = new CMenuWnd;
		 pMenu->Init( msg.pSender,pt);
		 pMenu->ShowWindow(TRUE);
	}
	else if(msg.sType == _T("menu_delete"))
	{
			int nSel = m_FileList->GetCurSel();
			if( nSel < 0 ) return;
			m_FileList->RemoveAt(nSel);
	}
	else if(msg.sType == _T("itemactivate"))
	{
		switch (m_eWnd)
		{
		case CMainUIWnd::Wnd_MYDISK:
			{
				/*if () {
				}*/
			}
			break;
		}
	}
	__super::Notify(msg);
}

DUI_BEGIN_MESSAGE_MAP(CMainUIWnd, CNotifyPump)
DUI_ON_MSGTYPE(DUI_MSGTYPE_CLICK,OnClick)
DUI_END_MESSAGE_MAP()

void CMainUIWnd::OnClick(TNotifyUI& msg)
{
	CTabLayoutUI* pControl2 = static_cast<CTabLayoutUI*>(m_PaintManager.FindControl(_T("tabTest")));
	if( msg.pSender->GetName() == _T("btnsetting") ) {
		//设置
		POINT pt = {msg.ptMouse.x, msg.ptMouse.y};
		CMenuSetting *pMenu = new CMenuSetting(_T("MenuSetting.xml"));
		pMenu->Init(&m_PaintManager, pt,msg.pSender);
		pMenu->ShowWindow(TRUE);

	} else if(msg.pSender->GetName() == _T("ButtonUploadL")) {
		COpenFile* opfi = new COpenFile();
		opfi->Openfile();

	} else if (msg.pSender->GetName() == _T("closeb")) {
		//重载关闭对话框，拦截消息
		BeginThread(DLG_END);

	} else if (msg.pSender->GetName() == _T("maxbtn")) {
		//最大化对话框，切回复
		SwitchDlg();

	} else if (msg.pSender->GetName() == _T("restorebtn")) {
		//回复对话框，切最大
		SwitchDlg(false);

	} else if (msg.pSender->GetName() == _T("Ad_line1")) {
		COptionUI* pOption1 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line1")));
		COptionUI* pOption2 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line2")));
		COptionUI* pOption3 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line3")));

		pOption2->Selected(false);
		pOption3->Selected(false);
		pControl2->SelectItem(0);

	}  else if (msg.pSender->GetName() == _T("Ad_line2")) {
		COptionUI* pOption1 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line1")));
		COptionUI* pOption2 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line2")));
		COptionUI* pOption3 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line3")));
		pOption1->Selected(false);

		pOption3->Selected(false);
		pControl2->SelectItem(1);

	}  else if (msg.pSender->GetName() == _T("Ad_line3")) {
		COptionUI* pOption1 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line1")));
		COptionUI* pOption2 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line2")));
		COptionUI* pOption3 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line3")));
		pOption1->Selected(false);
		pOption2->Selected(false);

		pControl2->SelectItem(2);

	} else if(msg.pSender->GetName() == _T("ButtonNewFolder")) {
		CListTextElementUI* pListElement = new CListTextElementUI;
		m_FileList->Add(pListElement);
		pListElement->SetText(0, _T("     新建文件夹"));
		pListElement->SetText(1, _T("2014-4-27"));
		pListElement->SetText(2, _T("文件夹"));
		pListElement->SetBkImage(_T("file='treeview_icon.png' source='64,0,80,16' dest='10,2,26,18'"));
		CTreeNodeUI* dstParent =(CTreeNodeUI*) m_pDirTree->GetItemAt(1);
		if(dstParent!=NULL)
		{
			CTreeNodeUI* pChildNode = new CTreeNodeUI();
			dstParent->AddChildNode(pChildNode);
			pChildNode->SetItemText(_T("新建文件夹"));
		}
	}
	__super::OnClick(msg);
}

void CMainUIWnd::InitWindow()
{
	//树形控件初始化
	InitTreeControl();
	SetUserWnd();
	//activex控件
	AddActiveX();

	//用户主页
	COptionUI* pOption1 = static_cast<COptionUI*>(m_PaintManager.FindControl(_T("Ad_line1")));
	pOption1->Selected(true);

	//我的网盘
	m_FileList = static_cast<CListUI*>(m_PaintManager.FindControl(_T("TreeFileList")));
	ListAddFile(_T("测试文档"), _T("DOC"), _T("87 KB"));
	/*ListAddFile(_T("总体设计"), _T("DOC"), _T("107 KB"));
	ListAddFile(_T("浅谈云存储之网盘分析"), _T("PDF"), _T("510 KB"));
	ListAddFile(_T("竞赛作品报告"), _T("DOC"), _T("210 KB"));
	ListAddFile(_T("2014年赛作品报告"), _T("DOC"), _T("198 KB"));
	ListAddFile(_T("功能模块"), _T("PNG"), _T("50 KB"));*/
	
	//下载管理
	m_pSendFileList = static_cast<CListUI*>(m_PaintManager.FindControl(_T("oLinkDownldList")));

	CButtonUI *b = new CButtonUI;
	CProgressUI *p = new CProgressUI;
	CLabelUI *n = new CLabelUI;
	CLabelUI *s = new CLabelUI;
	CLabelUI *t = new CLabelUI;
	SetLabelName(n, _T("测试文档"), _T("test_doc"));
	SetLabelName(s, _T("120KB/s"), _T("speed_doc"));
	SetLabelName(t, _T("00:00:23"), _T("time_doc"));
	ListAddProgress(CMainUIWnd::FILE_DOWN, b, p, n, s, t);

	SetWindowLong(this->m_hWnd, GWL_EXSTYLE, GetWindowLong(this->m_hWnd, GWL_EXSTYLE)^0x80000);
	BeginThread(DLG_START);
}

void CMainUIWnd::ListAddFile(CDuiString fname, CDuiString ftype, CDuiString fsize, CDuiString fdate /* = L"" */)
{
	CDuiString temp = L"    ";
	fname = temp+fname;

	if (fdate == L"") {
		time_t nowtime = time(NULL);
		struct tm ntime;
		localtime_s(&ntime, &nowtime);
		fdate.Format(L"%d-%0d-%0d %02d:%02d:%02d", ntime.tm_year+1900, ntime.tm_mon+1, ntime.tm_mday, 
			ntime.tm_hour, ntime.tm_min, ntime.tm_sec);
	}
	CListTextElementUI* pListElement = new CListTextElementUI;

	m_FileList->Add(pListElement);
	pListElement->SetText(0, fname);
	pListElement->SetText(1, fdate);
	pListElement->SetText(2, ftype);
	pListElement->SetText(3, fsize);
	pListElement->SetBkImage(_T("file='treeview_icon.png' source='592,0,608,16' dest='10,2,26,18'"));
}

void CMainUIWnd::SetLabelName(CLabelUI* plabel, CDuiString textname, CDuiString filename)
{
	plabel->SetText(textname);
	plabel->SetName(filename);
	plabel->ApplyAttributeList(_T("textcolor=\"#FFAAAAAA\" showhtml=\"true\" width=\"100\""));
}

void CMainUIWnd::AddPro(CButtonUI* pbut, CProgressUI* pros,
	CLabelUI* pname, CLabelUI* pspeed, CLabelUI* ptime)
{
	CListContainerElementUI* pDfile = new CListContainerElementUI;
	pDfile->ApplyAttributeList(_T("height=\"30\""));
	//总布局
	CHorizontalLayoutUI *new_h_lay = new CHorizontalLayoutUI;
	new_h_lay->ApplyAttributeList(_T("float=\"false\" ")\
		_T("childpadding=\"10\" inset=\"3,5,3,5\""));

	new_h_lay->Add(pbut);
	//新布局
	CVerticalLayoutUI *new_v_lay = new CVerticalLayoutUI;

	pros->SetMinValue(0);
	pros->SetMaxValue(160);
	pros->SetValue(50);
	pros->SetFixedWidth(100);
	pros->SetFixedHeight(10);
	pros->SetBkImage(_T("progressBG.png"));
	pros->SetForeImage(_T("progress.png"));
	pros->SetName(_T("down_progress"));

	new_v_lay->Add(pname);
	new_v_lay->Add(pros);
	new_h_lay->Add(new_v_lay);
	//新布局
	CVerticalLayoutUI* new_v_lay2 = new CVerticalLayoutUI;
	CLabelUI* Blanck = new CLabelUI;
	new_v_lay2->Add(Blanck);
	new_v_lay2->Add(pspeed);
	new_h_lay->Add(new_v_lay2);

	Blanck->ApplyAttributeList(
		_T("align=\"left\" text=\"\" textcolor=\"#FFAAAAAA\" showhtml=\"true\" height=\"8\""));

	//新布局
	CVerticalLayoutUI* new_v_lay3 = new CVerticalLayoutUI;
	CLabelUI* Blanck2 = new CLabelUI;
	new_v_lay3->Add(Blanck2);
	new_v_lay3->Add(ptime);
	new_h_lay->Add(new_v_lay3);

	Blanck2->ApplyAttributeList(
		_T("align=\"center\" text=\"\" textcolor=\"#FFAAAAAA\" showhtml=\"true\" height=\"8\""));

	pDfile->Add(new_h_lay);
	m_pSendFileList->Add(pDfile);
}

void CMainUIWnd::ListAddProgress(STATUS staus, CButtonUI* pbut, CProgressUI* pros,
	CLabelUI* pname, CLabelUI* pspeed, CLabelUI* ptime)
{
	switch (staus)
	{
	case CMainUIWnd::FILE_DOWN:
		{
			pbut->ApplyAttributeList(
				_T("name=\"down_ico\" float=\"false\" ")\
				_T("bordersize=\"0\" width=\"38\" maxheight=\"26\" ")\
				_T("normalimage=\"file='treeview_icon.png' source='208,0,224,16'\""));
			AddPro(pbut, pros, pname, pspeed, ptime);

		}
		break;
	case CMainUIWnd::FILE_UP:
		{
			pbut->ApplyAttributeList(
				_T("name=\"up_ico\" float=\"false\" ")\
				_T("bordersize=\"0\" width=\"38\" maxheight=\"26\" ")\
				_T("bkimage=\"glow.png\" ")\
				_T("normalimage=\"file='treeview_icon.png' source='192,0,208,16'\""));
			AddPro(pbut, pros, pname, pspeed, ptime);
		}
		break;

	case CMainUIWnd::FILE_SUCCED:
		{
			pbut->ApplyAttributeList(
				_T("name=\"succed_ico\" float=\"false\" ")\
				_T("bordersize=\"0\" width=\"38\" maxheight=\"26\" ")\
				_T("bkimage=\"glow.png\" ")\
				_T("normalimage=\"file='treeview_icon.png' source='240,0,256,16'\""));
			AddPro(pbut, pros, pname, pspeed, ptime);
		}
		break;
	}
}

BOOL CMainUIWnd::InitTreeControl()
{
	m_pDirTree= static_cast<CTreeViewUI*>(m_PaintManager.FindControl(_T("dirtree")));
	m_pSendTree = static_cast<CTreeViewUI*>(m_PaintManager.FindControl(_T("transtree")));
	//我的网盘
	CTreeNodeUI* pNode = new CTreeNodeUI();
	CTreeNodeUI* pChildNode2 = new CTreeNodeUI;
	CTreeNodeUI* pChildNode = new CTreeNodeUI();
	pNode->AddChildNode(pChildNode);
	pChildNode->SetItemText(_T("      用户文档"));
	pChildNode->SetBkImage(_T("file='treeview_icon.png' source='32,0,48,16' dest='36,0,52,16'"));
	pNode->AddChildNode(pChildNode2);
	pChildNode2->SetItemText(_T("      test"));
	pChildNode2->SetBkImage(_T("file='treeview_icon.png' source='64,0,80,16' dest='36,0,52,16'"));

	m_pDirTree->Add(pNode);
	pNode->SetAttribute(_T("folderattr"),_T("padding=\"0,1,0,0\" width=\"16\" height=\"16\" normalimage=\"file='Icon/treeview_b.png' source='0,0,16,16'\" hotimage=\"file='Icon/treeview_b.png' source='16,0,32,16'\" selectedimage=\"file='Icon/treeview_a.png' source='0,0,16,16' selectedhotimage=\"file='Icon/treeview_a.png' source='16,0,32,16'\""));
	pNode->SetItemText(_T("     网盘文件"));	 
	pNode->SetBkImage(_T("file='treeview_icon.png' source='0,0,16,16' dest='20,2,36,18'"));
	//传输管理
	CTreeNodeUI* pDownNode = new CTreeNodeUI;
	CTreeNodeUI* pDChild = new CTreeNodeUI;
	CTreeNodeUI* pDChild2 = new CTreeNodeUI;
	CTreeNodeUI* pUChild = new CTreeNodeUI;
	CTreeNodeUI* pUChild2 = new CTreeNodeUI;
	CTreeNodeUI* pUpNode = new CTreeNodeUI;

	pDownNode->AddChildNode(pDChild);
	pDChild->SetItemText(_T("     正在下载"));
	pDChild->SetBkImage(_T("file='treeview_icon.png' source='208,0,224,16' dest='36,0,52,16'"));
	pDownNode->AddChildNode(pDChild2);
	pDChild2->SetItemText(_T("     完成下载"));
	pDChild2->SetBkImage(_T("file='treeview_icon.png' source='240,0,256,16' dest='36,0,52,16'"));

	pUpNode->AddChildNode(pUChild);
	pUChild->SetItemText(_T("     正在上传"));
	pUChild->SetBkImage(_T("file='treeview_icon.png' source='192,0,208,16' dest='36,0,52,16'"));
	pUpNode->AddChildNode(pUChild2);
	pUChild2->SetItemText(_T("     完成上传"));
	pUChild2->SetBkImage(_T("file='treeview_icon.png' source='240,0,256,16' dest='36,0,52,16'"));

	m_pSendTree->Add(pDownNode);
	pDownNode->SetAttribute(_T("folderattr"),_T("padding=\"0,1,0,0\" width=\"16\" height=\"16\" normalimage=\"file='treeview_b1.png' source='0,0,16,16'\" hotimage=\"file='treeview_b1.png' source='16,0,32,16'\" selectedimage=\"file='treeview_a1.png' source='0,0,16,16' selectedhotimage=\"file='treeview_a1.png' source='16,0,32,16'\""));
	pDownNode->SetItemText(_T("     下载文件"));
	pDownNode->SetBkImage(_T("file='treeview_icon.png' source='80,0,96,16' dest='20,2,36,16'"));

	m_pSendTree->Add(pUpNode);
	pUpNode->SetAttribute(_T("folderattr"),_T("padding=\"0,1,0,0\" width=\"16\" height=\"16\" normalimage=\"file='treeview_b2.png' source='0,0,16,16'\" hotimage=\"file='treeview_b2.png' source='16,0,32,16'\" selectedimage=\"file='treeview_a2.png' source='0,0,16,16' selectedhotimage=\"file='treeview_a2.png' source='16,0,32,16'\""));
	pUpNode->SetItemText(_T("     上传文件"));
	pUpNode->SetBkImage(_T("file='treeview_icon2.png' source='128,0,144,16' dest='20,2,36,16'"));
	
	
	return TRUE;
}

void CMainUIWnd::BeginThread(DLG nMode)
{
	if (ThreaData::bAlphaThreadOK) {
		ThreaData* pData = new ThreaData;
		pData->pDlg = this;
		pData->nMode = (CMainUIWnd::DLG)nMode;
		pData->bAlphaThreadOK = false;

		AfxBeginThread(AlphaDlg, pData);
	}
}

UINT CMainUIWnd::AlphaDlg(LPVOID pParam)
{
	ThreaData* pData = (ThreaData*)pParam;

	switch (pData->nMode)
	{
	case DLG_START:
		{
			for (int i = 10;i < 240;i += 5)
			{
				SetLayeredWindowAttributes(pData->pDlg->m_hWnd, RGB(0, 0, 0), i, LWA_ALPHA);
				Sleep(15);
			}
		}
		break;
	case DLG_END:
		{
			for (int i = 240;i > 10;i -= 5)
			{
				SetLayeredWindowAttributes(pData->pDlg->m_hWnd, RGB(0,0,0), i, LWA_ALPHA);
				Sleep(15);
			}
			pData->pDlg->Close();
		}
		break;
	}
	
	pData->bAlphaThreadOK = true;

	DEL_P(pData);
	return 1;
}

CMainUIWnd::RETURN CMainUIWnd::SwitchDlg(bool btn /* = true */)
{
	//true是最大切换回复，false回复切换最大
	CControlUI* pbtnMax = static_cast<CControlUI*>(m_PaintManager.FindControl(_T("maxbtn")));
	CControlUI* pbtRestore = static_cast<CControlUI*>(m_PaintManager.FindControl(_T("restorebtn")));

	pbtnMax->SetVisible(false == btn);
	pbtRestore->SetVisible(true == btn);

	return SUCCED;
}

void CMainUIWnd::SetUserWnd()
{
	CDuiString temp;
	CLabelUI* pWndname = static_cast<CLabelUI*>(m_PaintManager.FindControl(_T("lbltitle")));

	temp = CDuiString(_T("用户名: ")) + m_strUserWnd;
	pWndname->SetText(temp);
}

void CMainUIWnd::SetUserWnd(CDuiString wnd_name)
{
	m_strUserWnd = wnd_name;
}

void CMainUIWnd::AddActiveX()
{
	CActiveXUI* pActive = static_cast<CActiveXUI*>(m_PaintManager.FindControl(_T("ActiveXDemo1")));
	if (pActive) {

		IWebBrowser2* pWebrower = NULL;
		pActive->SetDelayCreate(false);
		pActive->CreateControl(CLSID_WebBrowser);
		pActive->GetControl(IID_IWebBrowser2, (void**)&pWebrower);

		if (pWebrower != NULL) {
			pWebrower->Navigate(L"http://10.10.4.121:9000/", NULL, NULL, NULL, NULL);
			pWebrower->Release();
		}
	}
}