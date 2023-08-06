import os
import sys
from unittest import skipIf

from kecpkg.cli import kecpkg
from kecpkg.gpg import list_keys, get_gpg
from kecpkg.utils import create_file
from tests.utils import BaseTestCase, temp_chdir

TEST_SECRET_KEY = """
-----BEGIN PGP PRIVATE KEY BLOCK-----

lQIGBFzLAUQBBADZqa2AjOwDRb6D/lkuNKRFwTHF1x2SnhinTv5bosUZDRakZ6zd
dEeZiMBe6sSS9x+GTK8izkcZV6cEH8Xpcr7ngaH3bsfiiZvnI6ooyGTt/KFXP6jg
bPHEXi9zceZWIdZtZ3td4I7P52rwkPRSwEDHJcyyZYkG5/73s6Rf9xLkfQARAQAB
/gcDAoPb6jcCOLHi/RU1ynJZBz9PS+nrMUdzzRhRTKzgbhu+ijWhLUyWeXJeLtR2
1OVlPUBPVUya7nII7Puk5a0YM4m7M4GDUdrOM9pGZ6t5ocfgQ/tb+fI5FkYP6d9/
8eJaUn/OmnVl4QF2ZBBjMyWi9bJoUAa1Jq868f8qLN7YSUnJVEEx+CkMRAeP9oj/
/O7KBYn+bIRitOEqTyQyxMbBj/YLRG6F3/2kZjPDJWR/rlbpGttYIxAA+TiQnBCN
0PuLg8vTLFEcmIgsrkT8Q3ODjunJq70GII72Hf3qSM6Po1lBqlyj0RxUydFJkkQa
WQZYOKZyUbnIcOMozxFuNWoNYl8KVBoWawEvS0pzTojzwQy8PEsiqOFYH59dy0VD
2fqnM9Lf6TzcFeHwMu2Ps/vDQEKUZkOPOydAFJZw0IwozZtdPfDcccMItAXjCxjr
x/1+keOSU8V1d3wuppYAO7qve2OTYf5CZAEEJmy1ovYNWqhjcNvZ+O20LnRlc3Rr
ZXkgKEtFQ1BLRyBUT09MUyB0ZXN0aW5nIG9ubHkga2V5IDNNQVkxOSmI1AQTAQoA
PhYhBI0JL8wGC8wel87EiYehd6qyNx5oBQJcywFEAhsDBQkAAVGABQsJCAcCBhUK
CQgLAgQWAgMBAh4BAheAAAoJEIehd6qyNx5o8ZsEAInYfs7EhwUknBDbFHuZt+AE
TI80SIj/VD528EZyrDzyz5p/eeg2HQd470HDSPgwnChUJdMOKSUR7oSTxoOyGJcP
p0M/ydnmSraCOhWI8srW8edtWp16OOK5y/t7CbJ97CVOenImkSwT5uzxHgZWM9Tu
qTdggGeiZjdzXYSbq0pW
=Xq/K
-----END PGP PRIVATE KEY BLOCK-----
"""
TEST_SECRET_KEY_PASSPHRASE = "test"
TEST_SECRET_KEY_FINGERPRINT = "8D092FCC060BCC1E97CEC48987A177AAB2371E68"


@skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
@skipIf("sys.version_info <= (2, 7)",
        reason="Skipping tests for python 2.7, as PGP signing cannot be provided")
class TestCommandSign(BaseTestCase):

    def _import_test_key(self):
        with self.runner.isolated_filesystem() as d:
            create_file('TESTKEY.asc', TEST_SECRET_KEY)
            self.runner.invoke(kecpkg, ['sign', '--import-key', 'TESTKEY.asc'])

    def tearDown(self):
        super(TestCommandSign, self).tearDown()
        self.runner.invoke(kecpkg, ['sign', '--delete-key', TEST_SECRET_KEY_FINGERPRINT])

    def test_sign_list_keys(self):
        self._import_test_key()
        result = self.runner.invoke(kecpkg, ['sign', '--list'])
        self.assertIn(result.exit_code, [0, 1], "Results of the run were: \n---\n{}\n---".format(result.output))

    def test_import_key(self):
        with temp_chdir() as d:
            create_file('TESTKEY.asc', TEST_SECRET_KEY)
            result = self.runner.invoke(kecpkg, ['sign', '--import-key', 'TESTKEY.asc'])
            self.assertEqual(result.exit_code, 0, "Results of the run were: \n---\n{}\n---".format(result.output))

            # teardown
            result = self.runner.invoke(kecpkg, ['sign', '--delete-key', TEST_SECRET_KEY_FINGERPRINT])
            self.assertEqual(result.exit_code, 0, "Results of the run were: \n---\n{}\n---".format(result.output))

    def test_delete_key(self):
        self._import_test_key()

        result = self.runner.invoke(kecpkg, ['sign', '--delete-key', TEST_SECRET_KEY_FINGERPRINT])
        self.assertEqual(result.exit_code, 0, "Results of the run were: \n---\n{}\n---".format(result.output))

    def test_delete_key_wrong_fingerprint(self):
        self._import_test_key()

        result = self.runner.invoke(kecpkg, ['sign', '--delete-key', 'THISISAWRONGFINGERPRINT'])
        self.assertEqual(result.exit_code, 1, "Results of the run were: \n---\n{}\n---".format(result.output))

    def test_create_key(self):
        result = self.runner.invoke(kecpkg, ['sign', '--create-key'],
                                    input="Testing\n"
                                          "KECPKG TESTING CREATE KEY\n"
                                          "no-reply@ke-works.com\n"
                                          "1\n"
                                          "pass\n"
                                          "pass\n")
        self.assertEqual(result.exit_code, 0, "Results of the run were: \n---\n{}\n---".format(result.output))

        keys = list_keys(get_gpg())
        last_key = keys[-1]
        fingerprint = last_key[-1]

        result = self.runner.invoke(kecpkg, ['sign', '--delete-key', fingerprint])
        self.assertEqual(result.exit_code, 0, "Results of the run were: \n---\n{}\n---".format(result.output))

    def test_export_key(self):
        self._import_test_key()

        with self.runner.isolated_filesystem() as d:
            result = self.runner.invoke(kecpkg, ['sign',
                                                 '--export-key', 'out.asc',
                                                 '--keyid', TEST_SECRET_KEY_FINGERPRINT])
            self.assertEqual(result.exit_code, 0, "Results of the run were: \n---\n{}\n---".format(result.output))
            self.assertExists('out.asc')


@skipIf("sys.version_info >= (3, 4)", reason="These tests are for python 2 only.")
class TestCommandSign27(BaseTestCase):
    def test_sign_capability_unaivable(self):
        result = self.runner.invoke(kecpkg, ['sign', '--list'])
        self.assertEqual(result.exit_code, 1, "Results of the run were: \n---\n{}\n---".format(result.output))
