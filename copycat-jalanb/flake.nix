{
  description = "copycat-jalanb";

  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";
  inputs.pyproject-nix.url = "github:nix-community/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { nixpkgs, pyproject-nix, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        project =
          pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
        python = pkgs.python312;
        arg = project.renderers.withPackages { inherit python; };
        pythonEnv = python.withPackages arg;
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs;
            [
              # python312Packages.pylint
              # python312Packages.pyflakes
            ] ++ [ pythonEnv ];
        };
        packages.default =
          let attrs = project.renderers.buildPythonPackage { inherit python; };
          in python.pkgs.buildPythonPackage attrs;
      });
}
