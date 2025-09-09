
import argparse
try:
    from .hello import hello
except Exception:
    def hello(): return "🌱 AkashaOS awakens."
from .codex import spiral as codex_spiral, sigil as codex_sigil
from .temple import celestial_time
from .veil import gentle_nudge, drop_truth, nudge_code
from .curiosity import spark as curiosity_spark, explore as curiosity_explore, connect as curiosity_connect

def main():
    parser = argparse.ArgumentParser(prog="akasha", description="AkashaOS Gateforge CLI")
    sub = parser.add_subparsers(dest="cmd")
    parser.add_argument("--hello", action="store_true", help="Greet the keeper")

    scry = sub.add_parser("scry", help="Codex utilities")
    scry.add_argument("what", choices=["spiral","sigil"])
    scry.add_argument("--size", type=int, default=7)
    scry.add_argument("--text", type=str, default="")

    ttime = sub.add_parser("time", help="Temple timekeeper")
    ttime.add_argument("--calendar", choices=["gregorian","celestial"], default="celestial")

    veil = sub.add_parser("veil", help="Mentor nudges and truths")
    veil.add_argument("what", choices=["nudge","truth","code"])
    veil.add_argument("--snippet", type=str, default="")
    veil.add_argument("--seed", type=int, default=0)

    curious = sub.add_parser("curiosity", help="Curiosity sparks and bridges")
    curious.add_argument("action", choices=["spark","explore","connect"])
    curious.add_argument("--topic", type=str, default="spiral")
    curious.add_argument("--a", type=str, default="art")
    curious.add_argument("--b", type=str, default="physics")

    args = parser.parse_args()

    if args.hello:
        print(hello()); return

    if args.cmd == "scry":
        print(codex_spiral(args.size) if args.what=='spiral' else codex_sigil(args.text or 'intention')); return

    if args.cmd == "time":
        if args.calendar=='celestial':
            print(celestial_time())
        else:
            import datetime
            print({'gregorian': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')})
        return

    if args.cmd == "veil":
        if args.what=='nudge': print(gentle_nudge(args.seed))
        elif args.what=='truth': print(drop_truth(args.seed))
        else: print(nudge_code(args.snippet or ""))
        return

    if args.cmd == "curiosity":
        if args.action=='spark': print(curiosity_spark())
        elif args.action=='explore': print(curiosity_explore(args.topic))
        else: print(curiosity_connect(args.a, args.b))
        return

    parser.print_help()

if __name__ == "__main__":
    main()
