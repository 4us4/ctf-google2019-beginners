import sys

from itertools import chain
from sympy import isprime


# Implements a simple stack-based VM
class VM:

  def __init__(self, rom):
    self.rom = rom
    self.accumulator1 = 0
    self.accumulator2 = 0
    self.instruction_pointer = 1
    self.stack = []
    self.A002385 = sorted((n for n in chain((int(str(x) + str(x)[::-1]) for x in range(1, 11000)),
                                            (int(str(x) + str(x)[-2::-1]) for x in range(1, 11000))) if isprime(n)))

  def step(self):
    cur_ins = self.rom[self.instruction_pointer]
    self.instruction_pointer += 1

    fn = VM.OPERATIONS.get(cur_ins, None)

    if cur_ins[0] == '🖋':
      return
    if fn is None:
      raise RuntimeError("Unknown instruction '{}' at {}".format(
          repr(cur_ins), self.instruction_pointer - 1))
    else:
      fn(self)

  def add(self):
    self.stack.append(self.stack.pop() + self.stack.pop())

  def sub(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b - a)

  def if_zero(self):
    if self.stack[-1] == 0:
      while self.rom[self.instruction_pointer] != '😐':
        if self.rom[self.instruction_pointer] in ['🏀', '⛰']:
          break
        self.step()
    else:
      self.find_first_endif()
      self.instruction_pointer += 1

  def if_not_zero(self):
    if self.stack[-1] != 0:
      while self.rom[self.instruction_pointer] != '😐':
        if self.rom[self.instruction_pointer] in ['🏀', '⛰']:
          break
        self.step()
    else:
      self.find_first_endif()
      self.instruction_pointer += 1

  def find_first_endif(self):
    while self.rom[self.instruction_pointer] != '😐':
      self.instruction_pointer += 1

  def jump_to(self):
    marker = self.rom[self.instruction_pointer]
    if marker[0] != '💰':
      print('Incorrect symbol : ' + marker[0])
      raise SystemExit()
    marker = '🖋' + marker[1:]
    if marker == '🖋🏁🚩🎌💠🔶':
      prime_index = self.stack.pop()
      return_address = self.stack.pop()
      self.stack.append(self.A002385[prime_index - 1])
      self.instruction_pointer = return_address
    else:
      self.instruction_pointer = self.rom.index(marker) + 1

  def jump_top(self):
    self.instruction_pointer = self.stack.pop()

  def exit(self):
    print('\nDone.')
    raise SystemExit()

  def print_top(self):
    sys.stdout.write(chr(self.stack.pop()))
    sys.stdout.flush()

  def push(self):
    if self.rom[self.instruction_pointer] == '🥇':
      self.stack.append(self.accumulator1)
    elif self.rom[self.instruction_pointer] == '🥈':
      self.stack.append(self.accumulator2)
    else:
      raise RuntimeError('Unknown instruction {} at position {}'.format(
          self.rom[self.instruction_pointer], str(self.instruction_pointer)))
    self.instruction_pointer += 1

  def pop(self):
    if self.rom[self.instruction_pointer] == '🥇':
      self.accumulator1 = self.stack.pop()
    elif self.rom[self.instruction_pointer] == '🥈':
      self.accumulator2 = self.stack.pop()
    else:
      raise RuntimeError('Unknown instruction {} at position {}'.format(
          self.rom[self.instruction_pointer], str(self.instruction_pointer)))
    self.instruction_pointer += 1

  def pop_out(self):
    self.stack.pop()

  def load(self):
    num = 0

    if self.rom[self.instruction_pointer] == '🥇':
      acc = 1
    elif self.rom[self.instruction_pointer] == '🥈':
      acc = 2
    else:
      raise RuntimeError('Unknown instruction {} at position {}'.format(
          self.rom[self.instruction_pointer], str(self.instruction_pointer)))
    self.instruction_pointer += 1

    while self.rom[self.instruction_pointer] != '✋':
      num = num * 10 + (ord(self.rom[self.instruction_pointer][0]) - ord('0'))
      self.instruction_pointer += 1

    if acc == 1:
      self.accumulator1 = num
    else:
      self.accumulator2 = num

    self.instruction_pointer += 1

  def clone(self):
    self.stack.append(self.stack[-1])

  def multiply(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b * a)

  def divide(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b // a)

  def modulo(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b % a)

  def xor(self):
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(b ^ a)

  OPERATIONS = {
      '🍡': add,
      '🤡': clone,
      '📐': divide,
      '😲': if_zero,
      '😄': if_not_zero,
      '🏀': jump_to,
      '🚛': load,
      '📬': modulo,
      '⭐': multiply,
      '🍿': pop,
      '📤': pop_out,
      '🎤': print_top,
      '📥': push,
      '🔪': sub,
      '🌓': xor,
      '⛰': jump_top,
      '⌛': exit
  }


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Missing program')
    raise SystemExit()

  with open(sys.argv[1], 'r') as f:
    print('Running ....')
    all_ins = ['']
    all_ins.extend(f.read().split())
    vm = VM(all_ins)

    while 1:
      vm.step()
