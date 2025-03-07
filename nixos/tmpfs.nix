{ config, lib, ... }:

with lib;

{
  # tmpfs (a filesystem stored in RAM) settings for the NixOS boot process.
  # Clean tmpfs on system boot, useful for ensuring a clean state.

  # Enable tmpfs for the specified directories.
  boot.tmp.useTmpfs = true;

  # NEW: set to auto to dynamically grow    OLD:Allocate 35% of RAM for tmpfs. You can adjust this percentage to your needs.
  boot.tmp.tmpfsSize = "50%";

  fileSystems."/run" = {
    device = "tmpfs";
    options = [ "size=6G" ]; # Adjust based on your preferences and needs
  };

  # Fixed : better to use Dynamic 
   fileSystems."/tmp" = {
    device = "tmpfs";
    options = [ "size=7G" ];  # Adjust based on your preferences and needs
   };

}
