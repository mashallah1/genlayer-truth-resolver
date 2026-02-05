# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *


class TruthResolver(gl.Contract):
    claim: str
    resolved: bool
    verdict: u256   # 0 = unresolved, 1 = true, 2 = false

    def __init__(self, claim: str):
        self.claim = claim
        self.resolved = False
        self.verdict = u256(0)

    @gl.public.write
    def resolve(self) -> bool:
        if self.resolved:
            return False

        # Ask AI to resolve the claim using web knowledge
        prompt = (
            "Determine whether the following claim is TRUE or FALSE.\n\n"
            f"CLAIM: {self.claim}\n\n"
            "Respond with ONLY a single number:\n"
            "1 = true\n"
            "2 = false\n"
            "0 = cannot determine"
        )

        result = gl.nondet.exec_prompt(prompt).strip()

        if result == "1":
            self.verdict = u256(1)
            self.resolved = True
            return True

        if result == "2":
            self.verdict = u256(2)
            self.resolved = True
            return True

        return False

    @gl.public.view
    def get_claim(self) -> str:
        return self.claim

    @gl.public.view
    def get_verdict(self) -> u256:
        return self.verdict

    @gl.public.view
    def is_resolved(self) -> bool:
        return self.resolved
