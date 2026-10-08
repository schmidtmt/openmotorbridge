package bar.f0o.omb

import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.core.content.FileProvider
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File

class MainActivity : FlutterActivity() {

    private val PROXY_CHANNEL = "bar.f0o.omb/proxy"
    private val UPDATER_CHANNEL = "bar.f0o.omb/updater"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        // 1. Proxy Control Channel
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, PROXY_CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "startProxy" -> {
                    val port = call.argument<Int>("port") ?: 8080
                    OmbForegroundService.startService(applicationContext, port)
                    result.success(true)
                }
                "stopProxy" -> {
                    OmbForegroundService.stopService(applicationContext)
                    result.success(true)
                }
                "getProxyStatus" -> {
                    val status = mapOf(
                        "running" to OmbCellularProxyServer.isRunning.get(),
                        "boundToCellular" to OmbCellularProxyServer.boundToCellular.get(),
                        "bytesRx" to OmbCellularProxyServer.totalBytesRx.get(),
                        "bytesTx" to OmbCellularProxyServer.totalBytesTx.get(),
                        "activeConnections" to OmbCellularProxyServer.activeConnections
                    )
                    result.success(status)
                }
                else -> result.notImplemented()
            }
        }

        // 2. In-App APK Self-Updater Channel
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, UPDATER_CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "installApk" -> {
                    val filePath = call.argument<String>("filePath")
                    if (filePath == null) {
                        result.error("INVALID_PATH", "File path cannot be null", null)
                        return@setMethodCallHandler
                    }
                    try {
                        val file = File(filePath)
                        if (!file.exists()) {
                            result.error("FILE_NOT_FOUND", "APK file does not exist at $filePath", null)
                            return@setMethodCallHandler
                        }

                        val intent = Intent(Intent.ACTION_VIEW).apply {
                            val uri: Uri = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                FileProvider.getUriForFile(
                                    applicationContext,
                                    "${applicationContext.packageName}.fileProvider",
                                    file
                                )
                            } else {
                                Uri.fromFile(file)
                            }
                            setDataAndType(uri, "application/vnd.android.package-archive")
                            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
                        }
                        startActivity(intent)
                        result.success(true)
                    } catch (e: Exception) {
                        result.error("INSTALL_ERROR", e.message, null)
                    }
                }
                else -> result.notImplemented()
            }
        }
    }
}
