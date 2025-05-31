{
  description = "Python development shell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      pythonEnv =
        pkgs.python3.withPackages (pythonPkgs:
          with pythonPkgs; [pynvml]);
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [pythonEnv];
      };
    });
}
