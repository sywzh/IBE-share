#pragma once
#include "duilib.h"
namespace NETPAN_WND {

	class CNetDiskWnd :public CNetPanWnd
	{
	public:
		explicit CNetDiskWnd(LPCTSTR pszNetPanPath);
		~CNetDiskWnd(void);
	};
}

