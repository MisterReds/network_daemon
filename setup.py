import os
import shutil
import stat

def create_files():
    # Создаем файл конфигурации
    with open('network.conf', 'w') as f:
        f.write('''auto eth0
    iface eth0 inet dhcp

auto wlan0
    iface wlan0 inet static
        address 192.168.1.2
        netmask 255.255.255.0
        gateway 192.168.1.1
        dns-nameservers 8.8.8.8
''')

    # Создаем файл юнита systemd
    with open('/etc/systemd/system/network-daemon.service', 'w') as f:
        f.write('''[Unit]
Description=Network Configuration Daemon
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/network_daemon.py
Restart=always
User=nobody
Group=nogroup
WorkingDirectory=/path/to/your/
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
''')

    # Копируем скрипт демона в нужное место
    shutil.copy('network_daemon.py', '/path/to/your/network_daemon.py')

def set_permissions():
    # Устанавливаем права на исполняемый файл
    os.chmod('/path/to/your/network_daemon.py', stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
              stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
              stat.S_IROTH | stat.S_IXOTH)

def main():
    create_files()
    set_permissions()
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl enable network-daemon.service')
    os.system('sudo systemctl start network-daemon.service')

if __name__ == '__main__':
    main()
