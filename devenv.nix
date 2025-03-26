{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = [ pkgs.git ];

  languages.python.enable = true;
  languages.python.poetry.enable = true;
  languages.python.poetry.activate.enable = true;
  languages.python.version = "3.12";

  git-hooks.hooks = {
    # TODO: enable later
    # ruff.enable = true;
    # ruff-format.enable = true;
    # typos.enable = true;
    # check-toml.enable = true;
    # markdownlint.enable = true;
    yamllint.enable = true;
    yamlfmt.enable = true;
    yamlfmt.settings.lint-only = false;
    nixfmt-rfc-style.enable = true;
  };

  scripts.build.exec = ''
    poetry build
  '';

  scripts.format.exec = ''
    pre-commit run --all-files
  '';
}
