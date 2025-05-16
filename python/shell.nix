{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
