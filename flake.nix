{
  description = "A C++/Go/Rust/Fortran project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          # Build tools
          meson
          ninja
          pkg-config
          # Compilers
          gcc # Provides C and C++
          gfortran # Provides Fortran
          go
          cargo
          rustc
        ];
      };
    };
}
