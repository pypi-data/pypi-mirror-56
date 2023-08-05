import ast
from typing import List
import astunparse

from flake8_boto3 import __version__
BOTO3_NAME = "boto3"
BAD_KEYWORDS = {"aws_access_key_id", "aws_secret_access_key", "aws_session_token"}


class CheckHardcodedAccessTokens(object):
    name = "r2c-avoid-hardcoded-access-token"
    version = __version__

    def __init__(self, tree: ast.Module):
        self.tree = tree

    def run(self):
        visitor = CodeVisitor()
        visitor.visit(self.tree)

        if visitor.using_boto3:
            warnings = visitor.warnings
        else:
            warnings = (
                []
            )  # must be a false positive because not importing boto3 (better than a dumb grep)

        for warning in warnings:
            yield (
                warning.lineno,
                warning.col_offset,
                self._message_for(warning),
                "CheckHardcodedAccessTokens",
            )

    def _message_for(self, warning: ast.Call):
        code_snippit = astunparse.unparse(warning)
        return f"{self.name} Hardcoded Access Token Detected: {code_snippit}"


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.warnings: List[ast.Call] = []
        self.using_boto3 = False

    def visit_Call(self, call: ast.Call):
        keywords = call.keywords
        for keyword in keywords:
            if keyword.arg in BAD_KEYWORDS:
                self.warnings.append(call)
                # only report this call once even if (likely) multiple bad keyword args
                break

    def visit_Import(self, _import: ast.Import):
        names = _import.names
        for fqn in names:
            if fqn.name == BOTO3_NAME:
                self.using_boto3 = True

    def visit_ImportFrom(self, import_from: ast.ImportFrom):
        if import_from.module == BOTO3_NAME:
            self.using_boto3 = True
