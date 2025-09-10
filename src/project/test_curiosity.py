from akashaos.curiosity import spark, explore, connect

def test_curiosity():
    assert isinstance(spark(), str)
    assert isinstance(explore('spiral'), list)
    assert isinstance(connect('art','physics'), str)
