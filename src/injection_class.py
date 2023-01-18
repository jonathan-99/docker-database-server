#!/usr/bin/env python3

class InjectorCheck:
    _concern = ['--', 'DEL', 'DELETE']

    def __init__(self):
        self.incoming = ""

    def add(self, value) -> None:
        self.incoming = value

    def check_against_comment(self) -> bool:
        if self._concern in self.incoming:
            # this is bad -> remove the comment?
            return False
        else:
            return True
