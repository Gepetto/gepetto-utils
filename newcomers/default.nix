{
  lib,
  ldap3,
  buildPythonApplication,
}:
buildPythonApplication {
  pname = "greet-newcomers";
  version = "1.0.0";
  pyproject = false;
  dependencies = [ ldap3 ];

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./greet_newcomers.py
      ./template.txt
    ];
  };

  installPhase = ''
    install -D -m 755 greet_newcomers.py $out/bin/greet-newcomers
    install -D -m 644 template.txt $out/share/greet-newcomers/template.txt
  '';

  meta = {
    description = "Greet gepetto newcomers";
    homepage = "https://github.com/gepetto/gepetto-utils/tree/master/newcomers";
    license = lib.licenses.bsd2;
    maintainers = [ lib.maintainers.nim65s ];
    mainProgram = "greet-newcomers";
  };
}
