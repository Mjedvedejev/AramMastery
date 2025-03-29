from ChallengeDriver import ARAMChampion, ARAMFinesse, ARAMKeystones, ARAMWarrior, ChallengeTiers, Challenge
# Example challenge query
"""
Challenge(ARAMFinesse.AnotherDayAnotherBullseye).get()
Challenge(ARAMFinesse.ItWasANearHit).get()
Challenge(ARAMFinesse.SnowDay).get()
Challenge(ARAMFinesse.FreeMoney).get()
Challenge(ARAMFinesse.FreeTicketToBase).get()

Challenge(ARAMChampion.AllRandomAllChampions).get()
Challenge(ARAMChampion.AllRandomAllFlawless).get()
Challenge(ARAMChampion.RapidDemolition).get()
Challenge(ARAMChampion.ActiveParticipant).get()
Challenge(ARAMChampion.CantTouchThis).get()
Challenge(ARAMChampion.NARAM).get()

Challenge(ARAMWarrior.DPSThreat).get()
Challenge(ARAMWarrior.DoubleDecimation).get()
Challenge(ARAMWarrior.ARAMLegend).get()
Challenge(ARAMWarrior.BadMedicine).get()
Challenge(ARAMWarrior.NoHiding).get()
Challenge(ARAMWarrior.ARAMEradication).get()
Challenge(ARAMWarrior.FarmChampionsNotMinions).get()
Challenge(ARAMWarrior.SoloCarry).get()

Challenge(ARAMKeystones.ARAMAuthority).get()
Challenge(ARAMKeystones.ARAMChampion).get()
Challenge(ARAMKeystones.ARAMFinesse).get()
Challenge(ARAMKeystones.ARAMWarrior).get()
"""
Challenge().get_completed()
print("----------------------------------------------------------------------")
Challenge().get_uncompleted()