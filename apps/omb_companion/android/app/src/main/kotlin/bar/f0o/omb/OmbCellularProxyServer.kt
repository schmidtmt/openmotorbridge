package bar.f0o.omb

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.util.Log
import java.io.InputStream
import java.io.OutputStream
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicBoolean
import java.util.concurrent.atomic.AtomicLong

/**
 * OpenMotorBridge Layer-5 SOCKS5 & HTTP Relay Proxy
 * 
 * Specifically designed to route outbound telematics and internet requests strictly
 * through the cellular interface (TRANSPORT_CELLULAR) on Android, completely bypassing
 * the 5 GHz Wi-Fi link dedicated to Wireless CarPlay / Android Auto.
 * 
 * Crucially, this runs purely in user-space on L5 sockets and consumes ZERO VpnService slots,
 * allowing always-on VPNs like Tailscale (Home Assistant / Homesphere) to operate concurrently.
 */
class OmbCellularProxyServer(private val context: Context, private val port: Int = 8080) {

    companion object {
        private const val TAG = "OmbProxyServer"
        val isRunning = AtomicBoolean(false)
        val boundToCellular = AtomicBoolean(false)
        val totalBytesRx = AtomicLong(0)
        val totalBytesTx = AtomicLong(0)
        var activeConnections = 0
    }

    private var serverSocket: ServerSocket? = null
    private var cellularNetwork: Network? = null
    private val threadPool = Executors.newCachedThreadPool()
    private var networkCallback: ConnectivityManager.NetworkCallback? = null

    fun start() {
        if (isRunning.get()) return
        isRunning.set(true)

        // 1. Request cellular network specifically for outbound proxy routing
        acquireCellularNetwork()

        // 2. Start local listening socket
        threadPool.execute {
            try {
                serverSocket = ServerSocket(port, 50, InetAddress.getByName("127.0.0.1"))
                Log.i(TAG, "OMB SOCKS5/HTTP Proxy listening on 127.0.0.1:$port")

                while (isRunning.get() && serverSocket?.isClosed == false) {
                    val clientSocket = serverSocket?.accept() ?: break
                    threadPool.execute {
                        handleClient(clientSocket)
                    }
                }
            } catch (e: Exception) {
                if (isRunning.get()) {
                    Log.e(TAG, "Server socket error: ${e.message}", e)
                }
            } finally {
                stop()
            }
        }
    }

    fun stop() {
        isRunning.set(false)
        try {
            serverSocket?.close()
        } catch (_: Exception) {}
        serverSocket = null

        releaseCellularNetwork()
        Log.i(TAG, "OMB Proxy stopped")
    }

    private fun acquireCellularNetwork() {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager ?: return
        val request = NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_CELLULAR)
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()

        networkCallback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                cellularNetwork = network
                boundToCellular.set(true)
                Log.i(TAG, "Cellular network acquired. Outbound sockets will be bound to cellular.")
            }

            override fun onLost(network: Network) {
                if (cellularNetwork == network) {
                    cellularNetwork = null
                    boundToCellular.set(false)
                    Log.w(TAG, "Cellular network lost.")
                }
            }
        }

        try {
            cm.requestNetwork(request, networkCallback!!)
        } catch (e: Exception) {
            Log.e(TAG, "Failed to request cellular network: ${e.message}", e)
        }
    }

    private fun releaseCellularNetwork() {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager
        networkCallback?.let {
            try {
                cm?.unregisterNetworkCallback(it)
            } catch (_: Exception) {}
        }
        networkCallback = null
        cellularNetwork = null
        boundToCellular.set(false)
    }

    private fun handleClient(client: Socket) {
        synchronized(this) { activeConnections++ }
        try {
            val input = client.getInputStream()
            val output = client.getOutputStream()

            val firstByte = input.read()
            if (firstByte == -1) {
                client.close()
                return
            }

            if (firstByte == 0x05) {
                handleSocks5(client, input, output)
            } else {
                handleHttp(client, firstByte, input, output)
            }
        } catch (e: Exception) {
            Log.d(TAG, "Client error: ${e.message}")
        } finally {
            synchronized(this) { activeConnections = maxOf(0, activeConnections - 1) }
            try { client.close() } catch (_: Exception) {}
        }
    }

    private fun handleSocks5(client: Socket, input: InputStream, output: OutputStream) {
        val nMethods = input.read()
        val methods = ByteArray(nMethods)
        input.read(methods)

        output.write(byteArrayOf(0x05, 0x00))
        output.flush()

        val ver = input.read()
        val cmd = input.read()
        val rsv = input.read()
        val atyp = input.read()

        var targetHost = ""
        var targetPort = 0

        when (atyp) {
            0x01 -> {
                val ip = ByteArray(4)
                input.read(ip)
                targetHost = InetAddress.getByAddress(ip).hostAddress ?: ""
            }
            0x03 -> {
                val len = input.read()
                val domain = ByteArray(len)
                input.read(domain)
                targetHost = String(domain)
            }
            else -> {
                output.write(byteArrayOf(0x05, 0x08, 0x00, 0x01, 0, 0, 0, 0, 0, 0))
                output.flush()
                return
            }
        }

        val portBytes = ByteArray(2)
        input.read(portBytes)
        targetPort = ((portBytes[0].toInt() and 0xFF) shl 8) or (portBytes[1].toInt() and 0xFF)

        if (cmd != 0x01) {
            output.write(byteArrayOf(0x05, 0x07, 0x00, 0x01, 0, 0, 0, 0, 0, 0))
            output.flush()
            return
        }

        val targetSocket = Socket()
        cellularNetwork?.bindSocket(targetSocket)
        targetSocket.connect(java.net.InetSocketAddress(targetHost, targetPort), 10000)

        output.write(byteArrayOf(0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0))
        output.flush()

        bridgeSockets(client, targetSocket)
    }

    private fun handleHttp(client: Socket, firstByte: Int, input: InputStream, output: OutputStream) {
        val headerBuilder = StringBuilder()
        headerBuilder.append(firstByte.toChar())

        var b: Int
        while (input.read().also { b = it } != -1) {
            val c = b.toChar()
            headerBuilder.append(c)
            if (c == '\n') break
        }

        val requestLine = headerBuilder.toString().trim()
        val parts = requestLine.split(" ")
        if (parts.size < 2) return

        val method = parts[0]
        val target = parts[1]

        var targetHost = ""
        var targetPort = 80

        if (method.equals("CONNECT", ignoreCase = true)) {
            val hostPort = target.split(":")
            targetHost = hostPort[0]
            targetPort = if (hostPort.size > 1) hostPort[1].toIntOrNull() ?: 443 else 443

            var line: String?
            val reader = input.bufferedReader()
            while (reader.readLine().also { line = it } != null) {
                if (line.isNullOrEmpty()) break
            }

            val targetSocket = Socket()
            cellularNetwork?.bindSocket(targetSocket)
            targetSocket.connect(java.net.InetSocketAddress(targetHost, targetPort), 10000)

            output.write("HTTP/1.1 200 Connection Established\r\n\r\n".toByteArray())
            output.flush()

            bridgeSockets(client, targetSocket)
        } else {
            var url = target
            if (url.startsWith("http://")) url = url.substring(7)
            val slashIdx = url.indexOf('/')
            val hostPart = if (slashIdx != -1) url.substring(0, slashIdx) else url
            val hostPort = hostPart.split(":")
            targetHost = hostPort[0]
            targetPort = if (hostPort.size > 1) hostPort[1].toIntOrNull() ?: 80 else 80

            val targetSocket = Socket()
            cellularNetwork?.bindSocket(targetSocket)
            targetSocket.connect(java.net.InetSocketAddress(targetHost, targetPort), 10000)

            targetSocket.getOutputStream().write((requestLine + "\r\n").toByteArray())
            bridgeSockets(client, targetSocket)
        }
    }

    private fun bridgeSockets(s1: Socket, s2: Socket) {
        val t1 = Thread {
            pipeStream(s1.getInputStream(), s2.getOutputStream(), totalBytesTx)
            try { s2.shutdownOutput() } catch (_: Exception) {}
        }
        val t2 = Thread {
            pipeStream(s2.getInputStream(), s1.getOutputStream(), totalBytesRx)
            try { s1.shutdownOutput() } catch (_: Exception) {}
        }
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    }

    private fun pipeStream(input: InputStream, output: OutputStream, counter: AtomicLong) {
        val buffer = ByteArray(8192)
        var bytesRead: Int
        try {
            while (input.read(buffer).also { bytesRead = it } != -1) {
                output.write(buffer, 0, bytesRead)
                output.flush()
                counter.addAndGet(bytesRead.toLong())
            }
        } catch (_: Exception) {}
    }
}
