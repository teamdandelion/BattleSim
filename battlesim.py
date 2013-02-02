#!/usr/bin/env ipython
import random, time


# class Soldier:
# 	# Attributes:
# 	# Weapon
# 	# Hitpoints
# 	# Stress
# 	# Stress Regen Rate
# 	# Movement speed
# 	# Evade Mod, Accuracy Mod
# 	# 



class Sniper:
	def __init__(self):
		self.aimTime = 5 # shoots once every five seconds
		self.magazineSize = 10 
		self.reloadTime = 10
		self.bulletsRemaining = self.magazineSize
		self.waitTime = self.aimTime 


	def accuracy(self, distance):
		return float(1000-distance) / 1000


	def canShoot(self):
		if self.waitTime > 0:
			self.waitTime -= 1
			return 0

		else:
			if self.bulletsRemaining > 0:
				self.bulletsRemaining -= 1
				self.waitTime = self.aimTime
				return 1 # shoots
			else:
				self.waitTime = self.reloadTime + self.aimTime
				self.bulletsRemaining = self.magazineSize
				return 2 # reloads


class BattleManager:
	def __init__(self, verbose=False):
		self.startingSoldiers = 10 # we start with 10 nSoldiers
		self.soldierSpeed = 4.47 # 4.47 m/s
		self.verbose = verbose

	def runTheSimulation(self):
		self.time = 0
		self.nSoldiers = self.startingSoldiers
		self.distanceRemaining = 1000
		self.theSniper = Sniper()
		while self.nSoldiers > 0 and self.distanceRemaining > 0:
			self.one_second_passes()

		if self.nSoldiers == 0:
			if self.verbose: print "The soldiers all died! The last one made it {} meters".format(self.distanceRemaining)
			return (0, self.distanceRemaining)

		if self.distanceRemaining <= 0:
			if self.verbose: print "{} soldiers made it to to their objective!".format(self.nSoldiers)
			return (self.nSoldiers, 0.00)

	def one_second_passes(self):
		if self.verbose: time.sleep(.5)
		self.distanceRemaining -= self.soldierSpeed
		sniper_status = self.theSniper.canShoot()
		self.time += 1
		hit = 0
		reloading = 0

		if sniper_status == 1:
			acc = self.theSniper.accuracy(self.distanceRemaining)
			rnd = random.random()
			if rnd <= acc:
				self.nSoldiers -= 1
				hit = 1

		if sniper_status == 2:
			reloading = 1

		if self.verbose and sniper_status > 0 :
			self.report(hit, reloading)

	def report(self, hit, reloading):
		if reloading:
			sniperText = "The sniper is reloading."
		elif hit:
			sniperText = "The sniper hit his target! {} soldiers remaining.".format(self.nSoldiers)
		else:
			sniperText = "The sniper missed!"
		print sniperText + " Time: {}, Distance: {}".format(self.time, self.distanceRemaining)


def simulate(repeats=100000):
	n_survivals = 0
	distance_remaining = 0
	bm = BattleManager()
	for i in xrange(repeats):
		(survived, distance) = bm.runTheSimulation()
		if survived:
			n_survivals += 1
		else:
			distance_remaining += distance

	print "They survived {} out of {} times".format(n_survivals, repeats)
	print "Avg distance when they died was {}".format(distance_remaining / (repeats-n_survivals))


def main():
	#simulate()
	bm = BattleManager(True)
	bm.runTheSimulation()

if __name__ == '__main__':
	main()



