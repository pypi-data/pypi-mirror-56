# -----------------------------------------------------------------------------
# Copyright (C) 2019 Xinyu Ma
#
# This file is part of python-ndn.
#
# python-ndn is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-ndn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-ndn.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
from typing import List
from Cryptodome.Hash import SHA256
from ...encoding import Signer, SignatureType, VarBinaryStr


class DigestSha256Signer(Signer):
    def write_signature_info(self, signature_info):
        signature_info.signature_type = SignatureType.DIGEST_SHA256
        signature_info.key_locator = None

    def get_signature_value_size(self):
        return 32

    def write_signature_value(self, wire: VarBinaryStr, contents: List[VarBinaryStr]) -> int:
        h = SHA256.new()
        for blk in contents:
            h.update(blk)
        wire[:] = h.digest()
        return 32
