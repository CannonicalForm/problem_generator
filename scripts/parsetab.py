
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = "M\xba'\x01\xcf\xab\xc2J-P\xad`!UE\xf0"
    
_lr_action_items = {'RPAREN':([1,4,8,9,10,11,],[-1,8,-5,-2,-3,-4,]),'NUMBER':([0,2,5,6,7,],[1,1,1,1,1,]),'TIMES':([1,3,4,8,9,10,11,],[-1,7,7,-5,7,7,-4,]),'PLUS':([1,3,4,8,9,10,11,],[-1,5,5,-5,-2,-3,-4,]),'LPAREN':([0,2,5,6,7,],[2,2,2,2,2,]),'MINUS':([1,3,4,8,9,10,11,],[-1,6,6,-5,-2,-3,-4,]),'$end':([1,3,8,9,10,11,],[-1,0,-5,-2,-3,-4,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,5,6,7,],[3,4,9,10,11,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> NUMBER','expression',1,'p_expression_number','/home/casey/Documents/calc/my_parse.py',41),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','/home/casey/Documents/calc/my_parse.py',45),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','/home/casey/Documents/calc/my_parse.py',46),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','/home/casey/Documents/calc/my_parse.py',47),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','/home/casey/Documents/calc/my_parse.py',53),
]