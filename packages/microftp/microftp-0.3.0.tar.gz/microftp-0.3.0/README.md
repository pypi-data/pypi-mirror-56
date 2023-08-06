microftp
======
Python module to handle FTP protocol (client side only). It is modified original ftplib to handle broken FTP servers in embedded world.

Requirements
============

It should work with both python2 and python3 with simple pip commands:
```
pip install microftp
```

microftpcmd examples
========

Few microftpcmd examples:
```
microftpcmd --host 192.168.4.1 ls
microftpcmd --host 192.168.4.1 -d -v ls
microftpcmd --host 192.168.4.1 put local.txt remote.txt
microftpcmd --host 192.168.4.1 put local.txt remote.txt
microftpcmd --host 192.168.4.1 get remote-file.txt local-file.txt
microftpcmd --host 192.168.4.1 rm file-to-delete.txt
```

Note that you can also specify basic parameters using environment variables:
```
export MICROFTP_HOST=127.0.0.1
export MICROFTP_USER=user
export MICROFTP_PASSWORD=password
export MICROFTP_DIR=/something
```

and then you can just specify command:
```
microftpcmd ls
```

All options are listed using --help:

```
microftpcmd --help
```

Requirements
============

It should work with both python2 and python3 with simple pip commands:
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip
sudo pip3 install microftp
```

Examples
========

Simple example to get devices and its current status:

```
import microftp

ftp = microftp.microFTP("127.0.0.1")
ftp.set_pasv(True)
ftp.login()
ftp.set_debuglevel(9999)
ftp.cwd(args.dir)
print(ftp.raw_retrlines('LIST'))
ftp.quit()
```

