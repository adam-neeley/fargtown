{
  description = "arc dev env";

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
        python = pkgs.python313;
        arg = project.renderers.withPackages { inherit python; };
        pythonEnv = python.withPackages arg;
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs;
            [
            ] ++ [ pythonEnv ];
        };
        packages.default =
          let attrs = project.renderers.buildPythonPackage { inherit python; };
          in python.pkgs.buildPythonPackage
          (attrs // { propogatedBuildInputs = [ ]; });
      });
}
