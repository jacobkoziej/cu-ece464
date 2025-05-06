{
  description = "The Cooper Union - ECE 464: Databases";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    inputs:

    inputs.flake-utils.lib.eachDefaultSystem (
      system:

      let
        pkgs = import inputs.nixpkgs {
          inherit system;
        };

        inherit (pkgs) lib;
        inherit (pkgs) python3;

        python3-pkgs = python3.withPackages (
          python-pkgs:
          let
            jankins-dependencies =
              let
                inherit (lib) importTOML;
                inherit (lib.attrsets) attrVals;

                pyproject = importTOML ./pyproject.toml;

                inherit (pyproject.project) dependencies;

              in
              attrVals dependencies python-pkgs;

          in
          with python-pkgs;
          [
            beautifulsoup4
            ipython
            pytest
            requests
            sqlalchemy
          ]
          ++ jankins-dependencies
        );

      in
      {
        devShells.default = pkgs.mkShellNoCC (
          let
            pre-commit-bin = "${lib.getBin pkgs.pre-commit}/bin/pre-commit";

          in
          {
            packages = with pkgs; [
              black
              litecli
              mdformat
              pre-commit
              python3-pkgs
              ruff
              shfmt
              sleek
              sqlite
              sqlite-web
              toml-sort
              treefmt
              yamlfmt
              yamllint
            ];

            shellHook = ''
              ${pre-commit-bin} install --allow-missing-config > /dev/null
            '';
          }
        );

        formatter = pkgs.nixfmt-rfc-style;
      }
    );
}
