{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  hardeningDisable = [ "fortify" ];

  buildInputs = [
    pkgs.automake
    pkgs.clang
    pkgs.autoconf
    pkgs.gcc
    pkgs.gdb
    pkgs.libtool

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
