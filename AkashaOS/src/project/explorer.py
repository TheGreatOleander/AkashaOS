def explore(topic:str)->list[str]:
    connections={'spiral':['galaxies','DNA','snail shells','golden ratio'],'mirror':['symmetry','reflection','inversion','duality'],'music':['rhythm','harmony','frequencies','silence'],'art':['contrast','composition','negative space','gesture']}
    return connections.get(topic.lower(),['Look deeper into the unknown...'])
