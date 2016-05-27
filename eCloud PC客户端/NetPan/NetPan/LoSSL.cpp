#include "StdAfx.h"
#include "LoSSL.h"
using namespace NETPAN_TOOL;
LoSSL::LoSSL()
{
	connected = false;
	wsa_ok = false;
	SSLeay_add_ssl_algorithms();
	SSL_load_error_strings();
}

LoSSL::~LoSSL()
{
	SSL_shutdown(ssl);
	if(wsa_ok) WSACleanup();
	if(connected) closesocket(sock);
	SSL_free(ssl);
	SSL_CTX_free(ctx);	
}
void LoSSL::Initialize()
{
	WORD wVersionRequested;
	WSADATA wsaData;
	wVersionRequested = MAKEWORD(2, 2);

	if (WSAStartup(wVersionRequested, &wsaData) != 0)
	{
		MessageBox(NULL,_T("WSAStartup initialize failed"),_T("ERROR"),MB_OK);
	}
	wsa_ok = true;

	if (LOBYTE(wsaData.wVersion) != 2 || HIBYTE(wsaData.wVersion) != 2)
	{
		MessageBox(NULL,_T("socket error"),_T("ERROR"),MB_OK);
	}

	sock = socket(AF_INET, SOCK_STREAM, 0);

	if(sock == INVALID_SOCKET)
	{
		MessageBox(NULL,_T("creat socket error"),_T("EOOR"),MB_OK);
	}

	SSL_METHOD *meth = SSLv3_client_method();
	ctx = SSL_CTX_new(meth);
	if(ctx == NULL)
	{
		MessageBox(NULL,_T("ERR_SSL_CTX"),_T("ERROR"),MB_OK);
	}	   
	ssl = SSL_new(ctx);
	if(ssl == NULL)
	{
		MessageBox(NULL,_T("ERR_SSL_NEW"),_T("ERROR"),MB_OK);
	}
}

bool LoSSL::Connect(const char *host, unsigned short port)
{
	struct sockaddr_in addr = {0};
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = inet_addr(host);
	addr.sin_port = htons(port);

	struct timeval timeout;
	timeout.tv_sec = 9;
	timeout.tv_usec = 1000;
	socklen_t len = sizeof(timeout);
	setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeout, len);

	if(connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR)
	{
		//MessageBox(NULL,_T("connect error"),_T("ERROR"),MB_OK);
		return false;
	}
	connected = true;
	SSL_set_fd(ssl, sock);
	if(SSL_connect(ssl) == -1)
	{
		//MessageBox(NULL,_T("ERR_SSL_CONN"),_T("ERROR"),MB_OK);
		return false;
	}
	return true;
}

int LoSSL::Read(unsigned char *buf, int len)
{
	int remain = len;
	while(remain)
	{
		int ret = SSL_read(ssl, buf, remain);
		if(ret == -1)
		{
			MessageBox(NULL,_T("ERR_SSL_READ"),_T("ERROR"),MB_OK);
		}
		if(ret == 0)
			return len - remain;
		buf += ret;
		remain -= ret;
	}
	return len;
}

int LoSSL::Write(const unsigned char *buf, int len)
{
	int remain = len;
	while (remain)
	{
		int ret = SSL_write(ssl,buf,remain);
		if(ret == -1)
		{
			MessageBox(NULL,_T("ERR_SSL_WRITE"),_T("ERROR"),MB_OK);
		}
		if(ret == 0)
			return len - remain;
		remain -= ret;
		buf += ret;
	}
	return len;
}