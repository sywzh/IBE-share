// stdafx.h : ��׼ϵͳ�����ļ��İ����ļ���
// ���Ǿ���ʹ�õ��������ĵ�
// �ض�����Ŀ�İ����ļ�
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


// TODO: �ڴ˴����ó�����Ҫ������ͷ�ļ�
