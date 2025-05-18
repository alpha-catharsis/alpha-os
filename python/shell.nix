{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  hardeningDisable = [ "all" ];

  buildInputs = [
    pkgs.autoconf
    pkgs.automake
    pkgs.bison
    pkgs.gnumake
    pkgs.gcc
    pkgs.python3Packages.pip
    pkgs.python3

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
