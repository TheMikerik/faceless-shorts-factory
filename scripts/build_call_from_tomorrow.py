# Scene generator for video 004 (Call From Tomorrow) - the reference for quality.
# Copy it for a new video: change the props per location, characters, the hidden-swap
# actions, the shot list (w:<word index> from audio/words.json) and the lighting keys.
# Run: python3 scripts/build_call_from_tomorrow.py short.json
import json, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "short.json"
HIDE = -60
P = []
def prop(**k): P.append(k)
# ---------------- ROOM (x=0) ----------------
prop(type="box", pos=[0,0,3], size=[16,0.05,17], color="#c98a5a")          # wood floor
prop(type="box", pos=[0,0.05,-0.8], size=[3.4,0.02,2.4], color="#c7a3d6")     # rug
prop(type="wall", pos=[0,0,-4.3], size=[13,3.6,0.3], color="#8fb8c9")
prop(type="wall", pos=[-6.4,0,-0.5], size=[0.3,3.6,8], color="#7fa7bc")
prop(type="wall", pos=[6.4,0,-0.5], size=[0.3,3.6,8], color="#7fa7bc")
prop(type="box", pos=[-2.6,1.2,-4.12], size=[1.9,1.4,0.06], color="#ffe6a0")  # window
prop(type="box", pos=[-2.6,1.12,-4.05], size=[2.2,0.14,0.2], color="#6b3a5c")
prop(type="box", pos=[-2.6,1.2,-4.08], size=[0.1,1.4,0.08], color="#6b3a5c")
prop(type="box", pos=[3.2,0,-4.12], size=[1.3,2.4,0.1], color="#b5553a")      # front door
prop(type="box", pos=[3.65,1.05,-4.04], size=[0.14,0.14,0.08], color="#ffd860")
prop(type="box", pos=[-4.6,0,-3.1], size=[2.6,0.55,1.6], color="#e04f4f")     # bed
prop(type="box", pos=[-5.5,0.55,-3.1], size=[0.7,0.25,1.2], color="#fff3e0")
prop(type="box", pos=[1.1,0,-3.7], size=[1.5,0.8,0.7], color="#b5653a")       # desk
prop(type="post", pos=[1.5,0.8,-3.8], h=0.55, color="#4a3a3f")
prop(type="barrel", pos=[1.5,1.3,-3.8], r=0.24, h=0.28, color="#ffd860")
prop(type="box", pos=[-0.3,1.9,-4.05], size=[1.8,0.08,0.3], color="#6b3a5c")  # shelf + books
for i,c in enumerate(["#e04f4f","#5f9a4c","#ffd860","#6f8fa8","#c7a3d6"]):
    prop(type="box", pos=[-1.0+i*0.3,1.98,-4.05], size=[0.2,0.34+0.06*(i%2),0.24], color=c)
prop(type="box", pos=[0.9,1.75,-4.12], size=[0.8,0.6,0.04], color="#ffab70")  # picture
prop(type="barrel", pos=[-1.5,0.05,-1.3], r=0.55, h=0.18, color="#6f8fa8")     # empty dog bed
prop(type="tree", pos=[-4.6,0,1.8], scale=0.55, color="#5f9a4c")                # plant (fg)
prop(type="barrel", pos=[-4.6,0,1.8], r=0.3, h=0.4, color="#d98c6c")
prop(type="crate", pos=[3.6,0,1.6], size=0.7, color="#5f9a4c")                  # toy box (fg)
prop(type="post", pos=[5.2,0,-2.5], h=1.9, color="#6b4429")                     # coat stand
prop(type="box", pos=[5.2,1.5,-2.5], size=[0.5,0.5,0.15], color="#e04f4f")
# ---------------- YARD (x=80) ----------------
X=80
prop(type="house", pos=[X,0,-9], size=[6,3.4,5], color="#e9b872", roof="#b5553a")
prop(type="box", pos=[X,0,-3.8], size=[1.6,0.03,7], color="#d9a86a")           # path
for dx in (-6,-3.4,3.4,6):
    prop(type="wall", pos=[X+dx,0,-3.6], size=[2.4,0.9,0.15], color="#fff3e0")
prop(type="tree", pos=[X-7,0,-7], scale=1.8, color="#5f9a4c")
prop(type="tree", pos=[X+7.5,0,-8], scale=2.0, color="#4f8f4a")
prop(type="tree", pos=[X-4.5,0,-6], scale=0.7, color="#6fae54")
prop(type="tree", pos=[X+4.6,0,-6.2], scale=0.6, color="#6fae54")
prop(type="house", pos=[X-13,0,-19], size=[5,4,5], color="#8fb8c9", roof="#7a2f2f")
prop(type="house", pos=[X+14,0,-18], size=[5,4.6,5], color="#c7a3d6", roof="#6b3a5c")
prop(type="post", pos=[X-2.6,0,-2.6], h=1.2, color="#6b4429")                  # mailbox
prop(type="box", pos=[X-2.6,1.2,-2.6], size=[0.5,0.35,0.3], color="#e04f4f")
prop(type="barrel", pos=[X+4.4,0,-1.6], color="#6f8fa8")
prop(type="crate", pos=[X-5.2,0,2.4], size=0.8)                                 # fg
prop(type="post", pos=[X+4.2,0,3.2], h=2.4, color="#7a5a4a")                    # fg
for i,c in enumerate(["#e04f4f","#ffd860","#c7a3d6","#ffab70"]):
    prop(type="box", pos=[X-1.6-i*0.5,0,-3.1], size=[0.3,0.3,0.3], color=c)
# ---------------- PARK flashback (x=-80) ----------------
X=-80
prop(type="box", pos=[X,0,-0.5], size=[18,0.03,4], color="#d9a86a")
prop(type="box", pos=[X-4,0,-3.2], size=[2.2,0.45,0.7], color="#b5653a")         # bench
prop(type="box", pos=[X-4,0.45,-3.5], size=[2.2,0.6,0.12], color="#b5653a")
for x,s,c in ((-86,1.6,"#5f9a4c"),(-74,1.9,"#4f8f4a"),(-77,1.4,"#6fae54"),(-89,2.1,"#4f8f4a")):
    prop(type="tree", pos=[x,0,-6 if s<1.8 else -8], scale=s, color=c)
prop(type="post", pos=[X-2.4,0,-2.2], h=3, color="#4a3a3f")
prop(type="barrel", pos=[X-2.4,3,-2.2], r=0.25, h=0.35, color="#ffd860")
prop(type="wall", pos=[X,0,-10], size=[24,1.2,0.3], color="#c98a55")
prop(type="barrel", pos=[X+6,0,-3.5], r=2.0, h=0.06, color="#6fb8e8")            # pond
prop(type="box", pos=[X+2.2,0,-0.8], size=[0.35,1.0,0.35], color="#7a5a4a")      # bird stand
prop(type="crate", pos=[X-6.5,0,2.2], size=0.7)                                  # fg
prop(type="tree", pos=[X+5,0,2.6], scale=0.6, color="#6fae54")                  # fg bush

C = [
 {"id":"tlama","puppet":"puppets/main_hero_tlama_phone","pos":[0.2,0,-1.2],"height":1.8,"face":"neutral","pose":{"armR":-105}},
 {"id":"tomorrow","puppet":"puppets/main_hero_tlama_nest","pos":[3.2,HIDE,-3.4],"height":1.8,"face":"nervous","flip":True},
 {"id":"tlama_y","puppet":"puppets/main_hero_tlama","pos":[78.6,0,1.0],"height":1.8,"face":"neutral"},
 {"id":"neighbor","puppet":"puppets/red_bun_mom","pos":[82.8,0,0.4],"height":1.75,"face":"neutral","flip":True},
 {"id":"dog","puppet":"puppets/dog_floppy_ears","pos":[80.9,4.05,-6.75],"height":0.9},
 {"id":"tlama_p","puppet":"puppets/main_hero_tlama","pos":[-82.2,0,0.4],"height":1.8,"face":"neutral"},
 {"id":"dog_p","puppet":"puppets/dog_floppy_ears","pos":[-86.5,0,1.0],"height":0.9},
 {"id":"bird_tiny","puppet":"puppets/grey_bird","pos":[-77.8,1.0,-0.8],"height":0.6,"flip":True},
]
ROOF = [80,4.45,-7.4]
for bid,h in (("bird_s",1.6),("bird_m",4.2),("bird_l",5.8),("bird_xl",7.6)):
    C.append({"id":bid,"puppet":"puppets/grey_bird","pos":[ROOF[0],HIDE,ROOF[2]],"height":h})
A = []
def at(t, who, **k): A.append({"t":t, "who":who, **k})
def show(t, who, pos): at(t, who, to=pos, over=0.01, ease=0.01)
up = lambda: ROOF; down = [ROOF[0],HIDE,ROOF[2]]
show(0,"bird_m",ROOF)
show("w:77","bird_m",down); show("w:77","bird_l",ROOF)
show("w:82","bird_l",down); show("w:82","bird_xl",ROOF)
show("w:168","bird_xl",down); show("w:168","bird_l",ROOF)
show("w:172","bird_l",down); show("w:172","bird_m",ROOF)
show("w:174","bird_m",down); show("w:174","bird_s",ROOF)
show("w:94","tomorrow",[3.2,0,-3.4]); show("w:189","tomorrow",[3.2,HIDE,-3.4])
at("w:176","dog",to=[78.75,0.42,1.25],over=0.55)
at("w:44","tlama",to=[-2.0,0,-2.9],walk=True,over=1.2)
at("w:90","tlama",to=[1.3,0,-2.5],walk=True,over=1.3)
show("w:195","tlama",[-3.3,0,-1.5])
show("w:214","tlama",[0.2,0,-1.2])
at("w:129","dog_p",to=[-79.7,0,0.9],walk=True,over=1.5)

S = []
def shot(start, target=None, hw=0.2, yaw=0, pitch=0, zoom=6, pan=None, acts=(), out=None, **k):
    s = {"start":start}
    if target: s["target"]=target; s["headWidth"]=hw
    s.update(yaw=yaw, pitch=pitch, zoom=zoom)
    if pan: s["pan"]=pan
    s.update(k)
    if acts: s["actions"]=list(acts)
    if out: s["out"]=out
    S.append(s)
def a(at_, who, **k): return {"at":at_, "who":who, **k}
T="tlama"
shot("w:0",T,.22,14,2,6,[-10,4],[a(0,T,face="shocked",ease=0.01)])
shot("w:3",T,.30,-14,0,7,None,[a(0,T,face="confused",pose={"head":8})])
shot("w:8",T,.40,6,-4,9,None,[a(0,T,face="shocked",pose={"head":0},shake=0.8)])
shot("w:14",T,.12,28,8,5,None,[a(0,T,face="nervous",pose={"armL":60,"head":-8})])
shot("w:18",T,.09,-30,12,6,None,[a(0.1,T,face="shocked",pose={"armL":0},hop=0.25)])
shot("w:22",T,.30,10,0,8,None,[a(0,T,face="shocked",pose={"armL":120}),a(0.6,T,shake=0.6)])
shot("w:28",T,.10,-18,28,4,None,[a(0,T,face="confused",pose={"armL":0,"head":16})])
shot("w:33",None,anchor=[-1.5,0.3,-1.3],distance=3.6,yaw=10,pitch=26,zoom=6)
shot("w:36",T,.34,-8,0,8,None,[a(0,T,face="nervous",pose={"head":0},hop=0.15,shake=0.6)])
shot("w:44",T,.16,32,0,5,None,[a(0,T,face="happy",pose={"head":-10})])
shot("w:50","bird_m",.13,18,4,5,[0,6])
shot("w:61","dog",.14,-14,-8,7)
shot("w:66",T,.30,16,0,7,None,[a(0,T,face="nervous",pose={"head":0})])
shot("w:72",T,.38,-14,-6,9,None,[a(0,T,face="shouting",pose={"armL":120},shake=1.0)])
shot("w:77","bird_l",.18,-20,4,6,None,[a(0,T,pose={"armL":0})])
shot("w:82","bird_xl",.22,22,3,5)
shot("w:86","neighbor",.26,14,0,7,None,[a(0,"neighbor",face="shocked",pose={"armL":60,"armR":-60},shake=0.8)])
shot("w:90",T,.10,-26,4,5,None,[a(0,T,face="nervous")])
shot("w:95","tomorrow",.24,16,0,6,None,[a(0,"tomorrow",face="nervous")])
shot("w:100","tomorrow",.14,-18,22,6,None,[a(0,"tomorrow",face="confused")])
shot("w:107","tomorrow",.11,8,6,5,None,[a(0,T,face="shocked"),a(0.9,"tomorrow",face="shouting",pose={"armR":-110})])
shot("w:114",T,.28,-10,0,6,None,[a(0,T,face="confused",pose={"head":10}),a(0,"tomorrow",face="nervous",pose={"armR":0})],out="dissolve")
shot("w:121","tlama_p",.24,16,0,7,None,[a(0,"tlama_p",face="shouting",pose={"armL":120,"armR":-120}),a(0.6,"tlama_p",hop=0.2)])
shot("w:129","dog_p",.12,-22,6,4)
shot("w:135","bird_tiny",.08,-10,4,6,None,[a(0.3,"dog_p",hop=0.15),a(0.8,"dog_p",hop=0.15),a(0.2,"tlama_p",face="shocked",pose={"armL":0,"armR":0})],frameX=0.22)
shot("w:142","bird_xl",.24,-24,5,-4,None,out="dissolve")
shot("w:152",T,.22,12,0,6,None,[a(0,T,face="happy",pose={"armL":150,"head":0})])
shot("w:157",T,.30,-14,0,8,None,[a(0,T,face="neutral",pose={"armL":0,"head":-6})])
shot("w:160",T,.12,24,6,5,None,[a(0,T,face="nervous",pose={"armR":-60,"head":0},shake=0.4)])
shot("w:164",T,.34,8,0,7,None,[a(0,T,face="happy",pose={"head":10})])
shot("w:168","bird_l",.18,-16,5,5)
shot("w:172","bird_m",.14,14,5,7)
shot("w:174","tlama_y",.12,-12,6,4,None,[a(0,"tlama_y",face="shocked",pose={"armL":150,"armR":-150}),a(0.9,"tlama_y",face="happy",pose={"armL":40,"armR":-40})])
shot("w:181","tlama_y",.30,16,0,8,None,[a(0.2,"dog",hop=0.12),a(0.6,"dog",hop=0.12)])
shot("w:185",None,anchor=[3.2,1.3,-3.4],distance=3.4,yaw=-14,pitch=0,zoom=6,actions=[a(0,"tomorrow",face="happy",pose={"armR":-140}),a(0.4,"tomorrow",pose={"armR":-100},ease=0.2),a(0.7,"tomorrow",pose={"armR":-140},ease=0.2),a(1.0,"tomorrow",pose={"armR":-100},ease=0.2)])
shot("w:191",T,.10,30,5,6,None,[a(0,T,face="happy",pose={"armL":150,"armR":-105,"head":0},hop=0.4)],out="dissolve")
shot("w:195",T,.20,22,0,5,None,[a(0,T,face="neutral",pose={"armL":0,"armR":0}),a(1.0,T,face="nervous")])
shot("w:203",T,.30,34,0,7,None,[a(0,T,face="confused",pose={"head":10})])
shot("w:210",T,.42,14,0,11,None,[a(0,T,face="shocked",pose={"head":0},hop=0.2,shake=0.6)],out="dissolve")
shot("w:214",T,.14,-22,6,5,None,[a(0,T,face="nervous"),a(0.3,T,pose={"armR":-105})])
shot("w:223",T,.22,14,2,6,[-10,4],[a(0,T,face="nervous")])

HB={"bird_s":1.6,"bird_m":4.2,"bird_l":5.8,"bird_xl":7.6}
for sh in S:
    if sh.get("target") in HB:
        h=HB[sh.pop("target")]; hw=sh.pop("headWidth")
        sh["anchor"]=[ROOF[0]+h*(635.7-469)/994, ROOF[1]+h*(994-148.9)/994, ROOF[2]]
        sh["distance"]=round(415.5*h/994/(hw*0.4095),2)
    if sh.get("target")=="tlama" and sh.get("headWidth",0)>0.3 and sh["pitch"]<2: sh["pitch"]=2
XS={c["id"]:c["pos"][0] for c in C}
loc=lambda s: (lambda x: "park" if x<-40 else "yard" if x>40 else "room")(s["anchor"][0] if "anchor" in s else XS[s["target"]])
for i in range(len(S)-1):
    if loc(S[i])!=loc(S[i+1]): S[i]["out"]="dissolve"
    if S[i]["pitch"]<2 and S[i].get("headWidth",1)<0.2: S[i]["pitch"]=4
moods = {"day": {"sun": {"azimuth": 35, "elevation": 50, "color": "#ffe0b5", "intensity": 2.4}, "sky": {"top": "#5f86d8", "horizon": "#f2b98a"}, "fill": {"sky": "#8ea2ff", "ground": "#7a4a7c", "intensity": 1.2}}, "dusk": {"sun": {"azimuth": 60, "elevation": 20, "color": "#ffb070", "intensity": 2.3}, "sky": {"top": "#6a5fb0", "horizon": "#ffab70"}, "fill": {"sky": "#a08cff", "ground": "#6a3b6e", "intensity": 1.2}}, "red": {"sun": {"azimuth": 20, "elevation": 40, "color": "#ff7a6a", "intensity": 2.3}, "sky": {"top": "#7a1f3d", "horizon": "#ff7a5a"}, "fill": {"sky": "#ff9a9a", "ground": "#5a2a4a", "intensity": 1.2}}, "night": {"sun": {"azimuth": -40, "elevation": 38, "color": "#a9bcff", "intensity": 1.8}, "sky": {"top": "#1d2a6e", "horizon": "#6268b4"}, "fill": {"sky": "#7686ee", "ground": "#4c3f8c", "intensity": 1.6}, "exposure": 1.2}, "tense": {"sun": {"azimuth": -50, "elevation": 32, "color": "#d2b0ff", "intensity": 2.4}, "sky": {"top": "#3a2a78", "horizon": "#a77ac0"}, "fill": {"sky": "#9a8af0", "ground": "#5a4a9c", "intensity": 1.9}, "exposure": 1.35}, "gold": {"sun": {"azimuth": 30, "elevation": 55, "color": "#ffd860", "intensity": 3.0}, "sky": {"top": "#f0a830", "horizon": "#fff0b0"}, "fill": {"sky": "#ffe6a0", "ground": "#8a5a3a", "intensity": 1.4}, "exposure": 1.1}}
moods["flashback"] = {"sun":{"azimuth":-30,"elevation":40,"color":"#c9b0ff","intensity":2.2},"sky":{"top":"#4a3a8a","horizon":"#c08ad0"},"fill":{"sky":"#a090f0","ground":"#5a4a9c","intensity":1.8},"exposure":1.3}
moods["morning"] = {"sun":{"azimuth":70,"elevation":18,"color":"#ffd2a0","intensity":2.2},"sky":{"top":"#8ab0e8","horizon":"#ffd8b0"},"fill":{"sky":"#b0c0ff","ground":"#7a5a7c","intensity":1.4}}
L = [("0","day",0.01),("w:36","red",.15),("w:44","day",.3),("w:66","red",.15),("w:72","day",.3),("w:77","tense",.3),("w:82","red",.15),("w:90","tense",.4),
     ("w:114","night",.6),("w:121","flashback",.4),("w:142","night",.4),("w:152","dusk",.5),("w:168","day",.4),("w:191","gold",.2),("w:195","morning",.6),("w:210","red",.15),("w:214","day",.4)]
spec = {"fps":30,"audio":{"voice":"audio/voice.mp3","music":"music/music.mp3","musicDb":-18},"words":"audio/words.json","captions":{"wordsPer":1},
  "moods":moods,"lighting":[{"t":(0 if t=="0" else t),"mood":m,"fade":f} for t,m,f in L],
  "ground":{"color":"#8cbf5a"},"backdrop":{"image":"bg/valley.jpg"},"ink":{"set":4},
  "characters":C,"props":P,"shots":S,"actions":A,"end":"audio"}
json.dump(spec, open(OUT,"w"), indent=1)
print(len(P),"props",len(S),"shots")
