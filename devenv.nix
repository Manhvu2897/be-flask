{ pkgs, ... }:

{
  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  scripts."pip3.9".exec = "pip3 $@";

  enterShell = ''
    git --version
  '';

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    version = "3.11.4";
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };

  # https://devenv.sh/pre-commit-hooks/
  pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
