# gpmb

gpmb with kivy
3个屏幕，一个屏幕为控制，另一个屏幕为图片展示，一个为设置屏幕。
逻辑已经完成，5个定时。
只要修改进入屏保，屏保切换延迟即可。

sudo leafpad /etc/apt/sources.list
deb http://mirrors.aliyun.com/raspbian/raspbian/ jessie main non-free contrib
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ jessie main non-free contrib

要装的程序
sudo apt-get upgrade -y

sudo apt-get update
sudo apt-get install -y python3-smbus i2c-tools xrdp xclip feh ttf-wqy-zenhei ttf-wqy-microhei python-rpi.gpio python3-rpi.gpio samba-common-bin samba
sudo apt-get install -y python-smbus python3-smbus i2c-tools
sudo pip3 install pexpect aiohttp==0.22.5 aiohttp_jinja2 configparser

sudo leafpad /etc/modules    add
i2c-bcm2708  
i2c-dev  

lsmod | grep i2c_
That will list all the modules starting with “i2c_”. If it lists “i2c_bcm2708” then the module is running correctly.

If you’ve got a Model A, B Rev 2 or B+ Pi then type the following command :
sudo i2cdetect -y 1


直接在图形界面设置:固定IP
raspi-config:设置中文，设置时区，设置背景,关闭设置里接口


开机运行Python脚本
sudo pcmanfm 复制desktop文件到 /home/pi/.config/autostart
有两个，一个主程序gpmb，一个在线升级upgrade


samba文件共享
sudo leafpad /etc/samba/smb.conf  
[homes]段
browseable = yes
read only = no
create mask = 0755
directory mask = 0755
增加samba用户
sudo smbpasswd -a pi 输入两次密码，重启
重启samba服务：
/etc/init.d/samba restart
or
sudo service samba restart

禁用屏保和休眠
sudo leafpad /etc/lightdm/lightdm.conf
- locate [Seat Defaults] section
- line "#xserver-command=X" to
xserver-command=X -s o -dpms

或者安装xscreensaver，然后在系统设置里面禁用屏保


#feh-小巧的查看图片工具
feh -Y -x -q -D 5 -B black -F -Z -z -r /media/
man feh
-Z Auto Zoom
-x Borderless
-F Fullscreen
-Y hide pointer
-B image background
-q quiet no error reporting
-z Randomise
-r Recursive search all folders in folders
-D Slide delay in seconds

vkeyboard 行662 改字体 为 80
sudo leafpad /home/pi/kivy/uix/vkeyboard.py
sudo leafpad /usr/local/lib/python3.4/dist-packages/kivy/uix/vkeyboard.py

Install Kivy
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev cython
sudo pip3 install cython
sudo pip3 install git+https://github.com/kivy/kivy.git@master
sudo pip3 install pexpect


运行一次后才会产生ini文件
sudo leafpad /home/pi/.kivy/config.ini
keyboard_mode = dock
旋转屏幕 line 24 ratation=>90

Using Official RPi touch display
edit the file ~/.kivy/config.ini and go to the [input] section. Add this:
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput


sudo leafpad /boot/config.txt
display_rotate=0 Normal
display_rotate=1 90 degrees
display_rotate=2 180 degrees
display_rotate=3 270 degrees

$ sudo apt-get install xinput
xinput --list
(if you're on the Rasp Pi via SSH)
    DISPLAY=:0 xinput --list

/HOME/PI下面创建文件 rot.sh ，内容为

#!/bin/bash
xinput set-prop 'FT5406 memory based driver' 'Evdev Axes Swap' 1
xinput --set-prop 'FT5406 memory based driver' 'Evdev Axis Inversion' 0 1

赋予rot.sh执行权限！！！
sudo chmod 755 /home/pi/rot.sh

sudo leafpad /home/pi/.config/lxsession/LXDE-pi/autostart
加入一行
@/home/pi/rot.sh



看网上的教程都是用hostapd和isc-dhcp-server来搞，对着教程敲了一大堆命令折腾了三个小时无果，看网上都是针对的pi2用usb网卡整的，而pi3自带wifi，可能pi3不适用吧。于是网上各种搜，最后在github上发现神器create_ap，好家伙，看着安装方法好简单。废话不多说，下面上干货：

1.git clone https://github.com/oblique/create_ap.git

2.cd create_ap

3.sudo make install就这样安装好了

4.接下来安装依赖库，记得软件源换成 阿里云
sudo apt-get update
sudo apt-get install util-linux procps hostapd iproute2 iw haveged dnsmasq

5.就这么简单几个命令就能安装好全部环境

6.接下来保证你的网线插在pi3上并且能上网就行了。输入下面的命令启动无线AP：

sudo create_ap --no-virt wlan0 eth0 热点名 密码

接下来就去打开手机wifi看看有没有上面命令中设置的热点名吧，有的话输入密码即可连接上，enjoy your PI3 wireless AP！

可以把上述的启动命令添加到/etc/rc.local就可以开机自启动了。

是不是很简单，这个AP的局域网无线传输速度居然比我原来那个老AP还快一倍，也算是惊喜了，从此我的树莓派3又增加了一个功能。

ifup、ifdown = ifconfig eth0  up/down

sudo apt-get update
sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq
git clone https://github.com/oblique/create_ap.git
cd create_ap
sudo make install
sudo ifdown wlan0
sudo create_ap --no-virt -n -g 192.168.11.22 wlan0 zmj001 66341703

在线升级:上传 gpmb.zip 到 192.168.11.22:9002
热点名zmj001 热点密码66341703