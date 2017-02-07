import os
import shutil

def main():
    module = AnsibleModule(argument_spec = dict(ISO_PATH = dict(required = True,type='str')))
    ISO_PATH = module.params['ISO_PATH']
    #Mount the ISO in your OS
    os.system("mkdir /media/tmp_iso")
    os.system("mount -o rw,loop %s /media/tmp_iso" % ISO_PATH)

    #Create tftpboot folder
    #os.system("mkdir /var/lib/tftpboot")
    os.system("rm -rf /var/lib/tftpboot/pxelinux") 
    os.system("mkdir /var/lib/tftpboot/pxelinux")
    shutil.copy2('/media/tmp_iso/isolinux/initrd.img', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/media/tmp_iso/isolinux/TRANS.TBL', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/media/tmp_iso/isolinux/vmlinuz', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/media/tmp_iso/isolinux/vesamenu.c32', '/var/lib/tftpbootpxelinux')
    shutil.copy2('/media/tmp_iso/isolinux/initrd.img', '/var/lib/tftpboot/pxelinux')
    os.system("mkdir /var/lib/tftpboot/pxelinux/pxelinux.cfg")
    shutil.copy2('/media/tmp_iso/isolinux/isolinux.cfg', '/var/lib/tftpboot/pxelinux/pxelinux.cfg/default')
    exp = 21 # the line where text need to be added or exp that calculates it for ex %2
    file1 = "/var/lib/tftpboot/pxelinux/pxelinux.cfg/default"
    with open(file1, 'r') as f:
        lines = f.readlines()

    with open(file1, 'w') as f:
        for i,line in enumerate(lines):
            if i == exp:
                f.write('%s%s\n' %(line.rstrip('\n'),' ksdevice=eth0 ks=nfs:10.61.25.31:/share/kickstart/ks.cfg'))
            f.write(line)
    os.system("sed --in-place '23d' /var/lib/tftpboot/pxelinux/pxelinux.cfg/default")
    shutil.copy2('/usr/share/syslinux/ldlinux.c32', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/usr/share/syslinux/libutil.c32', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/usr/share/syslinux/menu.c32', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/usr/share/syslinux/pxelinux.0', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/usr/share/syslinux/libcom32.c32', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/usr/share/syslinux/vesamenu.c32', '/var/lib/tftpboot/pxelinux')
    shutil.copy2('/boot/grub/splash.xpm.gz', '/var/lib/tftpboot/pxelinux')
    os.system("sudo mkdir -p /share/images/rhel6/iso_image")
    os.system("cp -pr /media/tmp_iso/* /share/images/rhel6/iso_image/")   
    os.system("umount /media/tmp_iso")
    os.system("rm -rf /media/tmp_iso")
    os.system("sudo mkdir -p /share/kickstart")
    os.system("rm -rf /home/RedHat-rhel-server-6.7-x86_64-dvd.iso")
    os.system("service iptables stop")
    #os.system("service dhcpd stop")
    #os.system("service dhcpd start")
    #os.system("service xinetd stop")
    #os.system("service xinetd start")
    #os.system("service nfs stop")  
    #os.system("service nfs start")
    module.exit_json(changed=True,msg="mounted")

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()

