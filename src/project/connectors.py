def connect(craft_a:str, craft_b:str)->str:
    pair=(craft_a.lower(),craft_b.lower())
    bridges={('music','physics'):'Sound is vibration. Physics is the dance of vibrations.',('art','math'):'Geometry is frozen art; art is geometry set free.',('writing','coding'):'Both are spells. Syntax is incantation.',('art','physics'):'Light paints; physics names the pigments.'}
    return bridges.get(pair,'Their overlap is waiting to be discovered.')
