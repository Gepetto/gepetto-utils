{
  description = "Set of tools for the Gepetto Team";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.treefmt-nix.flakeModule ];
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      perSystem =
        {
          config,
          pkgs,
          self',
          ...
        }:
        {
          apps.onboarding = {
            type = "app";
            program = self'.packages.onboarding;
          };
          devShells.default = pkgs.mkShell {
            nativeBuildInputs = [ config.treefmt.build.wrapper ];
            packages = [ self'.packages.python ];
          };
          packages = {
            onboarding = pkgs.python3Packages.callPackage ./onboarding { };
            python = pkgs.python3.withPackages (
              p: with p; [
                beautifulsoup4
                httpx
                ldap3
                numpy
                pandas
                requests
                tabulate
                wand
              ]
            );
          };
          treefmt = {
            projectRootFile = "flake.nix";
            programs = {
              deadnix.enable = true;
              nixfmt-rfc-style.enable = true;
              ruff = {
                check = true;
                format = true;
              };
            };
          };
        };
    };
}
