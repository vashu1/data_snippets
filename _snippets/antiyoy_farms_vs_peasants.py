farm_price = 12
coins1 = coins2 = 12
coins1total = coins2total = coins1
peasants = farms = 0
land = 0
for n in range(20):
  if coins1 >= farm_price:
    farms += 1
    coins1 -= farm_price
    farm_price += 2
  if coins2 >= 10:
    peasants += 1
    coins2 -= 10
  land += peasants
  coins1 += 4 * farms
  coins1total += 4 * farms
  coins2 += land - 2*peasants
  coins2total += land
  print(f'{n=} {coins1total=} {farms=} {coins2total=} {peasants=} {land=} {coins1total>coins2total}')

# n=15 coins1total=308 farms=11 coins2total=295 peasants=9 land=55 True
# n=16 coins1total=356 farms=12 coins2total=360 peasants=10 land=65 False
# farms=11  ->  farm_price=32