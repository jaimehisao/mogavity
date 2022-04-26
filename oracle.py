semantic_oracle = []

"""
1 y 2
Int = 0
Float = 1
Char = 2

3
Sum = 0
Subtract = 1
Multiply = 2
Divide = 3

Results 
-1 = Error
"""

semantic_oracle[0][0][0] = 0   # Int y Int (Sum)
semantic_oracle[0][0][1] = 0   # Int y Int (Subtract)
semantic_oracle[0][0][2] = 0   # Int y Int (Multiply)
semantic_oracle[0][0][3] = 0   # Int y Int (Divide)

semantic_oracle[1][1][0] = 1   # Float y Float (Sum)
semantic_oracle[1][1][1] = 1   # Float y Float (Subtract)
semantic_oracle[1][1][2] = 1   # Float y Float (Multiply)
semantic_oracle[1][1][3] = 1   # Float y Float (Divide)

semantic_oracle[0][1][0] = 1   # Int y Float (Sum)
semantic_oracle[0][1][1] = 1   # Int y Float (Subtract)
semantic_oracle[0][1][2] = 1   # Int y Float (Multiply)
semantic_oracle[0][1][3] = 1   # Int y Float (Divide)
semantic_oracle[1][0][0] = 1   # Int y Float (Sum)
semantic_oracle[1][0][1] = 1   # Int y Float (Subtract)
semantic_oracle[1][0][2] = 1   # Int y Float (Multiply)
semantic_oracle[1][0][3] = 1   # Int y Float (Divide)







semantic_oracle[1][1][0] = 1   # Char y Char (Sum)
semantic_oracle[1][1][1] = 1   # Char y Char (Subtract)
semantic_oracle[1][1][2] = 1   # Char y Char (Multiply)
semantic_oracle[1][1][3] = 1   # Char y Char (Divide)

semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
semantic_oracle[0][0][0] = 1
