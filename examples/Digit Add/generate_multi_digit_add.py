from pathlib import Path

def bits(n):
 assert n>=0
 return ''.join('[' if d=='1' else ']' for d in bin(n)[2:]) if n else ''
def push(n):return '('+bits(n)+')'
def label(n):return '>'+bits(n)+'<'
def pick(n):return '<'+bits(n)+'>'
def jump(n):return push(n)+push(1)+'><'
class Asm:
 def __init__(self):self.lines=[];self.names={};self.nextid=1
 def lid(self,name):
  if name not in self.names:self.names[name]=self.nextid;self.nextid+=1
  return self.names[name]
 def mark(self,name):self.lines.append(label(self.lid(name)))
 def emit(self,*parts):self.lines.extend(parts)
 def goto(self,name):self.lines.append(jump(self.lid(name)))
 def jne_top(self,name,n):
  # existing [..., x] ; compare x with n, preserve x: [..., x, target, x-n] 
  self.emit(push(self.lid(name)),pick(1),push(n),'][','><')
 def source(self):return '\n'.join(self.lines)+'\n'

def build(maxdigits=20):
 a=Asm()
 a.emit(push(0));a.mark('READ_A');a.emit(' ')
 a.jne_top('A_DIGIT',43) # compare char to +
 a.emit(push(43),'][');a.goto('READ_B') # A,0
 a.mark('A_DIGIT');a.emit(push(48),'][',pick(1),push(9),'{}','[]','[]');a.goto('READ_A')
 a.mark('READ_B');a.emit(' ');a.jne_top('B_DIGIT',61)
 a.emit(push(61),'][','[]','[]');a.goto('CHECK_'+str(maxdigits-1))
 a.mark('B_DIGIT');a.emit(push(48),'][',pick(1),push(9),'{}','[]','[]');a.goto('READ_B')
 for power in range(maxdigits-1,0,-1):
  a.mark('CHECK_'+str(power));a.emit(push(a.lid('DIGIT_'+str(power))),pick(1),push(10**power),'}{','><')
 # if none bigger nonzero, start ones
 a.goto('DIGIT_0')
 for power in range(maxdigits-1,-1,-1):
  a.mark('DIGIT_'+str(power))
  # N -> N, (N // 10**power)%10 -> N, ascii -> N
  a.emit(pick(0),push(10**power),'}{',pick(0),push(10),'}{',push(10),'{}','][',push(48),'[]',')(')
 return a.source()

if __name__ == '__main__':
 import argparse
 parser = argparse.ArgumentParser(description='Generate LayerUpon decimal adder (input: 123+456=)')
 parser.add_argument('--digits', type=int, default=20, help='Maximum output decimal digits (default: 20)')
 parser.add_argument('--output', default='multi_digit_add.layer', help='Output file path')
 args = parser.parse_args()
 if args.digits < 1:
  parser.error('--digits must be >= 1')
 src = build(args.digits)
 Path(args.output).write_text(src, encoding='utf-8')
 print(f'Generated {args.output}: {len(src)} chars, {args.digits} output digits')
