vim /etc/systemd/system/ssh-monitor.service :


```

[Unit]
Description=SSH Connection Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/ssh_monitor/ssh_monitoring.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target

```
