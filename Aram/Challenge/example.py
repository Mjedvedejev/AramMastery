from Challenge.Drivers.ChallengeDriver import ARAMChampion, ARAMFinesse, Keystones, ARAMWarrior, ChallengeTiers, Challenge, ARENAChampion, MachineHuntingMercenary
from Challenge.Drivers.NotepadDriver import Notepad, Notepads
from Challenge.Api_Values.api_values import PUUID, API_KEY
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
Challenge().get_completed(PUUID.Me)
"""


Notepad(Notepads.ArenaPlay).add_entry("Jhin")
#Notepad(Notepads.ArenaPlay).get_missing_champions()

