# Seeed IRCamera

The IRCamera is a 32x24 thermal imagery sensor.

## Support python verison
```
Best version is 3.7
```

## Before intall this packetage
```
Make sure that your computer intall python...
Then, make sure that python's path and python's scripts path add your computer PATH variable.
```

## Installing from PyPI
On windows system:
```
pip install seeed_python_ircamera
```
if you think that the speed of download too slowly, you can try below command:
```
pip install seeed_python_ircamera -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

on unix/linux system:
```
sudo pip3 install seeed_python_ircamera
```
if you think that the speed of download too slowly, you can try below command:
```
sudo pip install seeed_python_ircamera -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## Usage Notes
On Windows, you should input the below command in cmd.exe:
```cmd
ircamera PortName
```
The parameter "PortName" indicate:
```
"PortName" may look like "COM1" on windows system, or "tty", "usb" on unix system
```

On Unix/linux system, you should input below command in terminal:
```shell
sudo ircamera PortName
```
just add sudo, the meaning of "PortName" the same as above.

## Contributing
If you have any good suggestions or comments, send email to me: 874751353@qq.com.
