Intended for use on Ubuntu Linux, but THIS IMPLEMENTATION IS MEANT TO RUN ON WINDOWS.
The backend and frontend were developed on different OSes and encountered several
incompatibilities, though we have achieved proper usage in one (convoluted) way:

Correct operation was obtained using the following:
    -   A Windows machine
    -   WSL (Windows Subsystem for Linux) installed, Ubuntu distro
        (this can be done simply by typing "wsl" into Command Prompt)
    -   Inside WSL, each of the dependencies for main.sh and hops.sh installed, including:
        -   traceroute
        -   delv
        -   perl-like regular expressions (the grep -Po flag), this should almost certainly come with WSL as-is.
    -   Dependencies for the frontend as well
        -   Python
        -   pip

To begin execution:

(this MAY work on various Linux distributions unlike the Windows configuration above,
but these often have some hurdles involving missing dependencies/drivers)

pip install -r requirements.txt
python ./GUI/main.py


IP/Domain Input Formatting:

Ipv4 [space] domain; for instance:

8.8.8.8 isc.org

or

Ipv4; for instance:

8.8.8.8

Expect roughly a 60-second hang while the GUI awaits the presence of dump.txt and hopdump.txt in
the current directory of THIS FILE