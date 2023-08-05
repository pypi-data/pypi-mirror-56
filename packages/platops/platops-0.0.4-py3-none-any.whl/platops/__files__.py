target_linux = """[Unit]
After=network.target
Description=PlatOps agent
[Service]
Type=simple
User=platops
ExecStart=/etc/platops/platops -config /etc/platops/platops.conf
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartForceExitStatus=SIGPIPE
KillMode=control-group
TimeoutSec=300
[Install]
WantedBy=multi-user.target
"""
