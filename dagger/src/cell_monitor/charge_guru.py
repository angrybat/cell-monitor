from dagger import dag, function, object_type, Container, Directory


DEPENDENCIES = [
    "libusb-1.0", 
    "libusb-1.0-0-dev", 
    "cmake", 
    "build-essential", 
    "qtbase5-dev", 
    "qtchooser", 
    "qt5-qmake", 
    "qttools5-dev-tools", 
    "libqt5charts5-dev", 
    "pkg-config", 
    "xfce4", 
    "xfce4-terminal", 
    "x11vnc", 
    "xvfb", 
    "novnc", 
    "websockify", 
    "python3", 
    "python3-websockify", 
    "dbus-x11"
]

@object_type
class ChargeGuru:
    @function
    def container(self, source: Directory, version: str = "24.04") -> Container:
        """Returns a Ubuntu container with libb6 and charge-guru installed this is accessible via VNC and noVNC."""
        libb6_repository = dag.git("https://github.com/angrybat/libb6").branch("main").tree()
        charge_guru_repository = dag.git("https://github.com/angrybat/charge-guru").branch("main").tree()
        apt_cache = dag.cache_volume("apt-cache")
        apt_lists = dag.cache_volume("apt-lists")
        return ( 
            dag.container()
            .from_(f"ubuntu:{version}")
            .with_mounted_cache("/var/cache/apt", apt_cache)
            .with_mounted_cache("/var/lib/apt/lists", apt_lists)
            .with_env_variable("DEBIAN_FRONTEND", "noninteractive")
            .with_env_variable("DISPLAY", ":1")
            .with_env_variable("VNC_PORT", "5901")
            .with_env_variable("NOVNC_PORT", "8080")
            .with_env_variable("VNC_RESOLUTION", "1920x1080")
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y"] + DEPENDENCIES)
            .with_mounted_directory("/src/libb6", libb6_repository)
            .with_mounted_directory("/src/charge-guru", charge_guru_repository)
            .with_workdir("/src/libb6")
            .with_exec(["mkdir", "-p", "build"])
            .with_workdir("/src/libb6/build")
            .with_exec(["cmake", "..", "-DCMAKE_INSTALL_PREFIX=/usr", "-DCMAKE_BUILD_TYPE=Release"])
            .with_exec(["make"])
            .with_exec(["make", "install"])
            .with_workdir("/src/charge-guru")
            .with_exec(["mkdir", "-p", "build"])
            .with_workdir("/src/charge-guru/build")
            .with_exec(["cmake", "..", "-DCMAKE_BUILD_TYPE=Release"])
            .with_exec(["make"])
            .with_exec(["make", "install"])
            .without_directory("/src")
            .with_file("/app/start.sh", source.file("start.sh"))
            .with_exposed_port(5901)
            .with_exposed_port(8080)
            .with_entrypoint(["/app/start.sh"])
        )
