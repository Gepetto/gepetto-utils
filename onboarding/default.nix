{
  lib,
  ldap3,
  buildPythonApplication,
}:
buildPythonApplication {
  pname = "onboarding";
  version = "1.0.0";
  pyproject = false;
  dependencies = [ ldap3 ];

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./onboarding.py
      ./template.txt
    ];
  };

  installPhase = ''
    install -D -m 755 onboarding.py $out/bin/onboarding
    install -D -m 644 template.txt $out/share/onboarding/template.txt
  '';

  meta = {
    description = "Greet gepetto newcomers";
    homepage = "https://github.com/gepetto/gepetto-utils/tree/master/onboarding";
    license = lib.licenses.bsd2;
    maintainers = [ lib.maintainers.nim65s ];
    mainProgram = "onboarding";
  };
}
