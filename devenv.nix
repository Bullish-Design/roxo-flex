{ pkgs, ... }:
{
  packages = [ pkgs.hugo pkgs.python3 pkgs.git pkgs.chromium ];
  scripts.check.exec = ''bash tests/build.sh'';
  enterTest = ''check'';
}
