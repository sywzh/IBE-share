// stdafx.h : 标准系统包含文件的包含文件，
// 或是经常使用但不常更改的
// 特定于项目的包含文件
//

#pragma once

#include "targetver.h"

#include <stdio.h>
#include <stdlib.h>
#include <tchar.h>
#include <afxsock.h>
#include <string>
#include <WinUser.h>

using namespace std;

#ifdef _UNICODE
	typedef wchar_t              char_t;
	typedef std::wstring         string_t;
	typedef std::wstringstream   stringstream_t;
#else
	typedef char                 char_t;
	typedef std::string          string_t;
	typedef std::stringstream    stringstream_t;
#endif

#define DEL_P(p) if (p != NULL) {\
	delete []p;\
	p = NULL;\
	}


// TODO: 在此处引用程序需要的其他头文件
