{
  description = "Set of tools for the Gepetto Team";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
        };
      laas-cnrs-typst-templates = {
        url = "https://gitlab.laas.fr/gsaurel/laas-cnrs-typst-templates/-/archive/main/laas-cnrs-typst-templates-main.tar.gz";
        inputs = {
          flake-parts.follows = "flake-parts";
          nixpkgs.follows = "nixpkgs";
          treefmt-nix.follows = "treefmt-nix";
      };
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
          inputs',
          pkgs,
          self',
          ...
        }:
        {
          apps.onboarding = {
            type = "app";
            program = self'.packages.onboarding;
          };
          devShells.default = pkgs.mkShellNoCC {
            nativeBuildInputs = [ config.treefmt.build.wrapper ];
            packages = [
              self'.packages.python
              self'.packages.typst
            ];
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
            typst = pkgs.typst.withPackages (_p: [ inputs'.laas-cnrs-typst-templates.packages.laas-cnrs-page ]);
          };
          treefmt = {
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
