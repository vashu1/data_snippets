import argparse

class CheckPositiveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values <= 0:
            parser.error(f'{self.dest} = {values} should be positive!')
        setattr(namespace, self.dest, values)

class Check2ByteHexAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            values = int(values, 16)
        except:
            parser.error(f'{self.dest} = {values} must be valid hex!')
        if values < 0 or values >= (1<<16):
            parser.error(f'{self.dest} = {values} should fit uint16!')
        setattr(namespace, self.dest, values)