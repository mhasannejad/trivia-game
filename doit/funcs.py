from leitner.models import Daroo


def assign_block():
    daroos = Daroo.objects.all()
    with open('doit/block_1.txt', 'r') as f:
        print(f.readlines())

        b1_daroos = daroos.filter(name__in=f.read().splitlines())
        for i in b1_daroos:
            print(i.name)

