#pragma once

#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#pragma comment(lib, "libeay32.lib")
#pragma comment(lib, "ssleay32.lib")

namespace NETPAN_TOOL {
	class LoSSL
	{
	public:
		LoSSL(void);
		~LoSSL(void);
		void Initialize();
		bool Connect(const char *host, unsigned short port);
		int Read(unsigned char *buf, int len);
		int Write(const unsigned char *buf, int len);
	private:
		SSL_CTX* ctx;
		SSL* ssl;
		bool connected;
		SOCKET sock;
		bool wsa_ok;
	};
}

