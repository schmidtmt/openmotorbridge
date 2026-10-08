package bar.f0o.omb

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat

class OmbForegroundService : Service() {

    companion object {
        const val CHANNEL_ID = "omb_foreground_channel"
        const val NOTIFICATION_ID = 4040
        const val ACTION_START = "bar.f0o.omb.action.START_PROXY"
        const val ACTION_STOP = "bar.f0o.omb.action.STOP_PROXY"
        const val EXTRA_PORT = "bar.f0o.omb.extra.PORT"

        fun startService(context: Context, port: Int = 8080) {
            val intent = Intent(context, OmbForegroundService::class.java).apply {
                action = ACTION_START
                putExtra(EXTRA_PORT, port)
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }

        fun stopService(context: Context) {
            val intent = Intent(context, OmbForegroundService::class.java).apply {
                action = ACTION_STOP
            }
            context.startService(intent)
        }
    }

    private var proxyServer: OmbCellularProxyServer? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action ?: ACTION_START
        val port = intent?.getIntExtra(EXTRA_PORT, 8080) ?: 8080

        when (action) {
            ACTION_START -> {
                val notification = buildNotification(port)
                startForeground(NOTIFICATION_ID, notification)

                if (proxyServer == null) {
                    proxyServer = OmbCellularProxyServer(applicationContext, port)
                    proxyServer?.start()
                }
            }
            ACTION_STOP -> {
                proxyServer?.stop()
                proxyServer = null
                stopForeground(STOP_FOREGROUND_REMOVE)
                stopSelf()
            }
        }

        return START_STICKY
    }

    override fun onDestroy() {
        proxyServer?.stop()
        proxyServer = null
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "OpenMotorBridge Service",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Hintergrunddienst für BLE-Telemetrie und Mobilfunk-Proxy"
                setShowBadge(false)
            }
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(channel)
        }
    }

    private fun buildNotification(port: Int): Notification {
        val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            launchIntent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("OpenMotorBridge Aktiv")
            .setContentText("Mobilfunk-Proxy läuft auf Port $port (Kein VPN-Konflikt)")
            .setSmallIcon(android.R.drawable.stat_notify_sync)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }
}
