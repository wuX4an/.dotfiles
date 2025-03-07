# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).

{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      ./tmpfs.nix
    ];

  # Bootloader.
  boot = {
    loader = {
      grub.enable = true;
      grub.device = "/dev/sda";
      grub.useOSProber = true;
    };
    tmp.cleanOnBoot = true;
    kernelPackages = pkgs.linuxPackages_6_11;
    kernelParams = [
      "quiet"
      "loglevel=0"
      "rd.systemd.show_status=false"
      "rd.udev.log_level=0"
      "udev.log_priority=0"
      "amdgpu.dcdebugmask=0x10"
    ];
    consoleLogLevel = 0;
    initrd.systemd.enable = true;
    initrd.verbose = true;
  };

  networking.hostName = "nixos"; # Define your hostname.
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Enable networking
  networking.networkmanager.enable = true;
  # Enable Bluetooth
  hardware.bluetooth.enable = true;
  hardware.bluetooth.powerOnBoot = true;

  # Set your time zone.
  time.timeZone = "America/Panama";

  # Select internationalisation properties.
  i18n.defaultLocale = "es_PA.UTF-8";

  i18n.extraLocaleSettings = {
    LC_ADDRESS = "es_PA.UTF-8";
    LC_IDENTIFICATION = "es_PA.UTF-8";
    LC_MEASUREMENT = "es_PA.UTF-8";
    LC_MONETARY = "es_PA.UTF-8";
    LC_NAME = "es_PA.UTF-8";
    LC_NUMERIC = "es_PA.UTF-8";
    LC_PAPER = "es_PA.UTF-8";
    LC_TELEPHONE = "es_PA.UTF-8";
    LC_TIME = "es_PA.UTF-8";
  };

  # Enable the X11 windowing system.
  services.xserver.enable = true;

  # Enable the XFCE Desktop Environment.
  services.displayManager.ly.enable = true;
  services.displayManager.ly.settings = {
      # tty = 1;
      # lang = "es";
    };
  # services.xserver.desktopManager.xfce.enable = true;
  services.xserver.windowManager.qtile = {
    enable = true;
    extraPackages = python3Packages: with python3Packages; [
      qtile-extras
    ];
  };


  # Configure keymap in X11
  services.xserver.xkb = {
    layout = "latam";
    variant = "";
  };

  # Configure console keymap
  console.keyMap = "la-latin1";

  # Enable CUPS to print documents.
  services.printing.enable = true;

  # Enable sound with pipewire.
  hardware.pulseaudio.enable = false;
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    # If you want to use JACK applications, uncomment this
    #jack.enable = true;

    # use the example session manager (no others are packaged yet so this is enabled by default,
    # no need to redefine it in your config for now)
    #media-session.enable = true;
  };

  # Enable touchpad support (enabled default in most desktopManager).
  # services.xserver.libinput.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.wux4an = {
    isNormalUser = true;
    description = "wuX4an";
    extraGroups = [ "networkmanager" "wheel" ];
    packages = with pkgs; [
    #  thunderbird
    ];
  };

  # Enable automatic login for the user.
  # services.xserver.displayManager.autoLogin.enable = true;
  # services.xserver.displayManager.autoLogin.user = "wux4an";

  # Install firefox.
  programs.firefox.enable = true;

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  # List packages installed in system profile. To search, run:
  # $ nix search wget
  environment.systemPackages = with pkgs; [
    # Networking
    bluez
    bluez-alsa
    bluez-tools
    bluetui
    # Sound
    playerctl
    pulsemixer
    pamixer
    # Brightness
    brightnessctl
    # LockScreen
    i3lock-color
    imagemagick
    maim
    # Music
    mpd
    mpc
    mpv
    rmpc
    alsa-utils
    # Menu
    rofi
    fzf
    # Icons
    papirus-icon-theme
    bibata-cursors
    # Terminal
    kitty
    # Editor
    neovim
    # Notification
    dunst
    # Compositor
    picom-pijulius
    # Python
    python3Full
    python3Packages.qrcode
    # X11
    xclip
    flameshot
    xdg-utils
    # Misc
    git
    stow
    ffmpeg
  ];

  # Fonts
  fonts = {
    enableDefaultPackages = true;
    packages = with pkgs; [
      noto-fonts
      noto-fonts-extra
      noto-fonts-emoji
      open-sans
      source-han-mono
      departure-mono
      (nerdfonts.override { fonts = [ "NerdFontsSymbolsOnly" ]; })
    ];
  };

  programs.nix-ld.enable = true;
  programs.nix-ld.libraries = with pkgs; [
    xorg.libX11
    xorg.libXext
    xorg.libXinerama
    xorg.libXrandr
    xorg.libXcursor
    xorg.libXrender
    alsa-lib
    libpulseaudio
    libGL
    SDL2
    libxkbcommon
    xorg.libXi
  ];

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };

  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  # services.openssh.enable = true;

  # Open ports in the firewall.
  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  # Or disable the firewall altogether.
  # networking.firewall.enable = false;

  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It‘s perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  # Before changing this value read the documentation for this option
  # (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
  system.stateVersion = "24.11"; # Did you read the comment?

}
