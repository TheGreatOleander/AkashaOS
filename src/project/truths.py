TRUTHS=['All spirals expand, but none returns to the same point.','The mirror never lies, but it always bends.','Every glyph is a doorway; the word is the key.','Stillness is not absence; it is presence without motion.']

def drop_truth(level:int=0)->str:
    return TRUTHS[level%len(TRUTHS)]
