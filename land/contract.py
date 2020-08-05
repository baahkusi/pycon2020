import smartpy as sp

class LandRegister(sp.Contract):
    
    def __init__(self, manager, registrars):
        
        self.init(
            manager=manager,
            registrars=registrars,
            lands=sp.big_map(tkey=sp.TString, tvalue=sp.TRecord(
                A=sp.TPair(sp.TInt, sp.TInt),
                B=sp.TPair(sp.TInt, sp.TInt),
                C=sp.TPair(sp.TInt, sp.TInt),
                D=sp.TPair(sp.TInt, sp.TInt)
                )),
            
            land_owners=sp.map(tkey=sp.TAddress, tvalue=sp.TSet(sp.TString))
            )

    @sp.entry_point
    def add_registrar(self, params):
        
        sp.verify_equal(sp.sender, self.data.manager, message="Unauthorized Action. You are not manager.")
        
        self.data.registrars.add(params.registrar)
        
    
    @sp.entry_point
    def remove_registrar(self, params):
        
        sp.verify_equal(sp.sender, self.data.manager, message="Unauthorized Action. You are not manager.")
        
        self.data.registrars.remove(params.registrar)
    
    
    @sp.entry_point
    def add_land(self, params):
        sp.verify(self.data.registrars.contains(sp.sender), message = "You must be a registrar")
        
        self.data.lands[params.code] = sp.record(A=params.land['A'], B=params.land['B'], C=params.land['C'], D=params.land['D'])
        
        
        sp.if self.data.land_owners.contains(params.owner):
            self.data.land_owners[params.owner].add(params.code)
        sp.else:
            self.data.land_owners[params.owner] = sp.set([params.code])
            


@sp.add_test(name = "Land Register Tests")
def test():
    scenario = sp.test_scenario()
    scenario.h1('Land Register')
    
    manager = sp.test_account('Manager')
    
    r1 = sp.test_account('Registrar 1')
    r2 = sp.test_account('Registrar 2')
    r3 = sp.test_account('Registrar 3')
    
    c = LandRegister(manager=manager.address, registrars=sp.set([r1.address, r2.address, r3.address]) )
    
    scenario += c
    
    scenario.h2("Add Registrar")
    
    r4 = sp.test_account('Registrar 4')
    
    scenario += c.add_registrar(registrar=r4.address).run(sender=manager)
    
    scenario.h2("Add Registrar with Wrong Manager")
    
    wrong = sp.test_account('Wrong Manager')
    
    r5 = sp.test_account('Registrar 5')
    
    scenario += c.add_registrar(registrar=r5.address).run(sender=wrong, valid=False)
    
    
    scenario.h2("Remove Registrar")

    scenario += c.remove_registrar(registrar=r1.address).run(sender=manager)
    
    scenario.h2("Remove Registrar with Wrong Manager")
    
    scenario += c.remove_registrar(registrar=r2.address).run(sender=wrong, valid=False)
    
    
    scenario.h2("Add Land")
    
    land_owner = sp.test_account('Land Owner')
    
    land = {
        'A': (1,2),
        'B': (3,2),
        'C': (4,3),
        'D': (5,4)
    }
    
    code = "ABCD"
    
    scenario += c.add_land(owner=land_owner.address, land=land, code=code).run(sender=r3)
    
    
    scenario.h2("Add Land with Wrong Registrar")
    
    scenario += c.add_land(owner=land_owner.address, land=land, code=code).run(sender=wrong, valid=False)
    
    
    
    
# @sp.add_test(name = "Land Register Tests")
# def test():
#     scenario = sp.test_scenario()
#     scenario.h1('Land Register')
    
#     manager = sp.address('tz1UyrTvzWzvkxeWjZEiadXAuccw5druNTkN')
    
#     r1 = sp.test_account('Registrar 1')
#     r2 = sp.test_account('Registrar 2')

#     c = LandRegister(manager=manager, registrars=sp.set([r1.address, r2.address]) )
    
#     scenario += c
