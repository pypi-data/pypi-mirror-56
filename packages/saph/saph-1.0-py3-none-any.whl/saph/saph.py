# Copyright 2019 Marcos Del Sol Vives <marcos@orca.pet>
# SPDX-License-Identifier: WTFPL

import hashlib
from Crypto.Cipher import AES
from typing import Union

class Saph:
	"""
	SAPH implementation, with configurable memory size and iteration count.

	Due to how the pseudo-random memory is created for hashing a password, increasing memory
	increases both time and space complexity.

	Increasing iterations, however, increase time complexity only.

	:ivar memory: memory size, in 64-byte blocks
	:vartype memory: int
	:ivar iterations: number of iterations
	:vartype iterations: int
	"""

	def __init__(self, memory:int=16384, iterations:int=8):
		"""
		Creates a new instance of a SAPH hasher with the given memory size and iteration count.
		
		:param memory: memory size, in 64-byte blocks
		:param iterations: number of iterations
		:type memory: int
		:type iterations: int
		"""

		self.memory = memory
		self.iterations = iterations

	def hash(self, *parts:Union[str, bytes, bytearray]) -> bytes:
		"""
		Hashes the given passwords/salt/pepper.

		:param `*parts`: parts to hash
		:type `*parts`: Union[str, bytes, bytearray]
		:return: password hash
		:rtype: bytes
		"""

		# Hash each part and calculate initial value
		part_md = hashlib.sha256()
		for part in parts:
			if isinstance(part, str):
				part = part.encode('utf-8')

			part = hashlib.sha256(part).digest()
			part_md.update(part)
		current = part_md.digest()

		# Create initial memory with all zeros
		mem = bytearray(64 * self.memory)

		for iteration in range(self.iterations):

			# Encrypt array using AES-CBC
			key = current[0:16]
			iv = current[16:32]
			aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
			aes.encrypt(mem, mem)

			# Create shuffle map
			order = list(range(self.memory))
			for a in range(self.memory):
				chunk = a * 64
				b = \
					mem[chunk + 0] << 0 | \
					mem[chunk + 1] << 8 | \
					mem[chunk + 2] << 16 | \
					mem[chunk + 3] << 24
				b %= self.memory

				x = order[a]
				order[a] = order[b]
				order[b] = x

			# Hash memory according to indexes list
			new_md = hashlib.sha256()
			for index in order:
				start = index * 64
				end = start + 64
				new_md.update(mem[start:end])
			current = new_md.digest()

		return bytes(current)
