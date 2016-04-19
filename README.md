# Kenwood-morse-beacon
Turns a Kenwood TS-480 into a helicopter beacon

We have a homemade helicopter non-directional beacon onboard the Greenpeace ship MY Esperanza, tuned with a crystal to frequency 1625.5. Unfortunately the ADF on the helicopter we got, a Bendix King KR87m, cannot tune to half kilohertzs.

However we have a Kenwood TS-480, which can transmit within the range of this ADF. So I wrote this little script to control the Kenwood via serial, to loop through a morse message (our ship's call sign) on CW and it works good.

##Usage:
```python heli_beacon.py {timer in minutes}```

###Example: 
```python heli_beacon.py 30```

