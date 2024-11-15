{
  description = "metacat-marshall develpment envronment";

  inputs.nixpkgs.url = "nixpkgs/nixos-24.05";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default =
          pkgs.mkShell { packages = with pkgs; [ nixd nixpkgs-fmt chez ]; };
      });
}
