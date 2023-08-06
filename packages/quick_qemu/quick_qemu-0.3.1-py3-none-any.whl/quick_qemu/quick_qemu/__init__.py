#! /usr/bin/env python3

import sys
import os
import subprocess
import signal
import time
import stat

default_config = {
    "arch": "/usr/bin/qemu-system-x86_64",
    "virtviewer": "/usr/bin/remote-viewer",
    "mac": "00:aa:31:25:2a:00",
    "memory": "2048",
    "cores": "2",
    "sambashare": "$HOME/share_quickqemu",
    "output": "external_spice",
    "glrendering": "QUICK_QEMU_GL_RENDERING" in os.environ,
    "cpu": os.environ.get("QUICK_QEMU_CPU", "Opteron_G1"),
    "machine": os.environ.get("QUICK_QEMU_MACHINE", "pc,accel=kvm"),
}

qemu_process = None
viewer_process = None
cleanuptried = False


def is_device(path):
    try:
        return stat.S_ISBLK(os.stat(path).st_mode)
    except Exception:
        return False


def qqemu_cleanup(*args):
    global cleanuptried
    if not cleanuptried:
        if qemu_process:
            qemu_process.terminate()

        if viewer_process:
            viewer_process.terminate()
        cleanuptried = True
    else:
        if qemu_process:
            qemu_process.kill()

        if viewer_process:
            viewer_process.kill()


def start_qemu(qemu_argv, config):
    cmdargs = [config["arch"]]
    cmdargs += ["-machine", config["machine"]]
    cmdargs += ["-cpu", config["cpu"]]
    cmdargs += ["-rtc", "base=localtime,driftfix=slew", "-no-hpet"]
    cmdargs += ["-global", "kvm-pit.lost_tick_policy=discard"]
    cmdargs += ["-enable-kvm"]
    cmdargs += ["-device", "virtio-balloon"]
    cmdargs += ["-smp", "cpus={cores},threads=1".format(cores=config["cores"])]
    cmdargs += ["-m", config["memory"]]
    cmdargs += ["-device", "virtio-serial"]
    if config["output"] == "external_spice":
        if config["glrendering"]:
            cmdargs += ["-device", "virtio-vga,virgl=on"]
            cmdargs += [
                "-spice",
                "gl=on,disable-ticketing,unix,addr=/run/user/{}/quick_qemu_spice.sock".format(  # noqa: 501
                    os.getuid()
                )
            ]
        else:
            cmdargs += ["-vga", "qxl"]
            cmdargs += [
                "-spice",
                "disable-ticketing,unix,addr=/run/user/{}/quick_qemu_spice.sock".format(  # noqa: 501
                    os.getuid()
                )
            ]

        cmdargs += ["-device", "ich9-usb-ehci1,id=usb"]
        cmdargs += ["-device", "ich9-usb-uhci1,masterbus=usb.0,firstport=0,multifunction=on"]  # noqa: 501
        cmdargs += ["-device", "ich9-usb-uhci2,masterbus=usb.0,firstport=2"]
        cmdargs += ["-device", "ich9-usb-uhci3,masterbus=usb.0,firstport=4"]
        cmdargs += ["-chardev", "spicevmc,name=usbredir,id=usbredirchardev1"]
        cmdargs += ["-device", "usb-redir,chardev=usbredirchardev1,id=usbredirdev1"]  # noqa: 501
        cmdargs += ["-chardev", "spicevmc,name=usbredir,id=usbredirchardev2"]
        cmdargs += ["-device", "usb-redir,chardev=usbredirchardev2,id=usbredirdev2"]  # noqa: 501
        cmdargs += ["-chardev", "spicevmc,name=usbredir,id=usbredirchardev3"]
        cmdargs += ["-device", "usb-redir,chardev=usbredirchardev3,id=usbredirdev3"]  # noqa: 501
        # cmdargs += [
        #   "-device",
        #   "virtserialport,chardev=charchannel1,id=channel1,name=org.spice-space.webdav.0",  # noqa: 501
        #   "-chardev",
        #   "spiceport,name=org.spice-space.webdav.0,id=charchannel1"
        # ]
    else:
        cmdargs += ["-vga", "qxl"]
        cmdargs += ["-display", config["output"]]
    cmdargs += ["-soundhw", "hda"]
    cmdargs += ["-boot", "order=cd,once=dc"]
    cmdargs += [
        "-netdev", "user,id=qemunet0,net=10.0.2.0/24,dhcpstart=10.0.2.15"
    ]

    if config["sambashare"]:
        sambashare = os.path.realpath(os.path.expandvars(os.path.expanduser(
            config["sambashare"]
        )))
        if os.path.exists(sambashare):
            cmdargs[-1] += ",smb={},smbserver=10.0.2.4".format(sambashare)
        else:
            print("\"{}\" does not exist, disable sambashare".format(
                sambashare
            ))
    else:
        print("Sambashare disabled")
    cmdargs += [
        "-device",
        "virtio-net-pci,mac={},netdev=qemunet0".format(
            config["mac"]
        )
    ]

    index = 0
    is_part_argument = False
    for elem in qemu_argv:
        if elem[0] != "-" and not is_part_argument:
            path = os.path.realpath(os.path.expandvars(os.path.expanduser(
                elem
            )))
            if os.path.isfile(path):
                if elem[-4:] == ".iso":
                    params = "media=cdrom,readonly"
                    cmdargs += [
                        "-drive",
                        "file={path},index={index},{params}".format(
                            path=path, index=index, params=params
                        )
                    ]
                else:
                    if os.access(path, os.W_OK):
                        params = "media=disk,cache=writeback"
                    else:
                        params = "media=disk,readonly"
                    cmdargs += [
                        "-drive", "file={path},index={index},{params}".format(
                            path=path, index=index, params=params
                        )
                    ]
                index += 1
            elif is_device(path):
                if os.access(path, os.W_OK):
                    params = "media=disk,discard=on,cache=none,format=raw"
                else:
                    params = "media=disk,readonly"
                cmdargs += [
                    "-drive",
                    "file={path},index={index},{params}".format(  # noqa: 501
                        path=path, index=index, params=params
                    )
                ]
                index += 1
            else:
                print(
                    "Not a valid file:", path, "({})".format(elem),
                    file=sys.stderr
                )
                return None
                # cmdargs.append(elem)  # not path
            # first check if it is a valid file then check read access
            if not os.access(path, os.R_OK):
                print(
                    "No permission:", path, file=sys.stderr
                )
                return None
        else:
            # switch if - less argument is encountered
            if elem[0] != "-":
                is_part_argument = False
            else:
                is_part_argument = True
            cmdargs.append(elem)
    return subprocess.Popen(cmdargs)


# part of virt-viewer
def start_viewer(config):
    cmdargs = [
        config["virtviewer"],
        "spice+unix:///run/user/{}/quick_qemu_spice.sock".format(
            os.getuid()
        )
    ]
    return subprocess.Popen(cmdargs)


def help():
    print(
        "Usage: quick_quemu [<isofile>|<discfile>|<devicefile>|-<parameter>"
        " <argument>]..."
    )


def main(argv, config=default_config):
    global qemu_process
    global viewer_process

    if len(argv) == 0 or argv[0] in ("-h", "-help", "--help"):
        help()
        return

    if not os.path.isfile(config["arch"]):
        print("Qemu not found:", config["arch"], file=sys.stderr)
        return

    if not os.path.isfile(config["virtviewer"]):
        print(
            "remote-view of virtviewer not found:",
            config["virtviewer"],
            file=sys.stderr
        )
        return

    signal.signal(signal.SIGINT, qqemu_cleanup)
    qemu_process = start_qemu(argv, config)
    if not qemu_process:
        return
    if config["output"] == "external_spice":
        time.sleep(5)
        viewer_process = start_viewer(config)

    while True:
        if qemu_process.poll() is not None:
            break
        if config["output"] == "external_spice":
            if viewer_process.poll() is not None:
                break
        time.sleep(3)
    qqemu_cleanup()
