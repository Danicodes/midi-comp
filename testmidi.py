from midiutil.MidiFile import MIDIFile
from dataclasses import dataclass
# MIDI Note Pitch:  https://studiocode.dev/resources/midi-middle-c/
track = 0

class MidiWriter():
    octave = 12 # Add 12 to jump an octave

    def __init__(self, tracks=2, tracknames=None, tempo=80) -> None:
        self.mf = MIDIFile(tracks) # Piano standard two midi tracks
        self.tracks = tracks

        # Init track names
        if not tracknames:
            tracknames = list(range(1, tracks))
        for track in range(1,tracks):
            self.mf.addTrackName(track, 0, tracknames[track])

        # Init tempo
        self.alter_tempo(tempo)
        self.duration = 4
        self.channel = 0
        self.volume = 100
        pass

    def alter_tempo(self, tempo, time=0, tracks=None):
        if not tracks:
            tracks = self.tracks
        
        for track in range(1, tracks):
            self.mf.addTempo(track, time, tempo)
    
    def write_note(self, track, note, time, duration=None, volume=None):
        if not duration:
            duration = self.duration
        if not volume:
            volume = self.volume

        self.mf.addNote(track, self.channel, note, time, duration, volume)

    def write_chord(self, track, chord, time, duration=None, volume=None, stagger=0):
        if not duration:
            duration = self.duration
        if not volume:
            volume = self.volume

        for pitch in chord.values():
            self.mf.addNote(track, self.channel, pitch, time + stagger, duration, volume)

    def write_out(self, filename):
        with open(filename, "wb") as outf:
            self.mf.writeFile(outf)

@dataclass
class Chord():
    one: int
    three: int
    five: int 
    seven: int = None

@dataclass
class MidiChord:
    chord: dict
    # Other attributes?

class Duration():
    sixtnth = 1/4
    eighth = 1/2
    threesixtnth = 3/4
    quarter = 1
    half = 2
    full = 4

class Chords():
    octave = 12
    # Rooted in C4
    c4 = 60
    csharp4 = dflat4 = 61
    d4 = 62
    dsharp4 = eflat4 = 63
    e4 = 64
    f4 = 65
    fsharp4 = gflat4 = 66 
    g4 = 67
    gsharp4 = aflat4 = 68
    a4 = 69
    asharp4 = bflat4 = 70
    b4 = 71

    cmaj =  {1: c4, 3: e4, 5: g4}
    dmaj = {1: 62, 3: 66, 5: 69}
    emaj = {1: 64, 3: 68, 5: 71}
    fmaj = {1: 65, 3: 69, 5: 72}
    gmaj = {1: 67, 3: 71, 5: 74}
    amaj = {1: 69, 3: csharp4, 5: 76}
    bmaj = {1: b4, 3: dsharp4 + octave , 5: fsharp4 + octave}

    cmin = {1: c4, 3: dsharp4, 5: g4}
    dmin = {1: d4, 3: f4, 5: a4}
    emin = {1: e4, 3: g4, 5: b4}
    fmin = {1: f4, 3: asharp4, 5: c4 + octave}
    gmin = {1: g4, 3: bflat4, 5: d4+octave}
    amin = {1: a4, 3: c4+octave, 5: e4+octave}
    bmin = {1: b4, 3: d4 + octave, 5: fsharp4 + octave}

    csharpmaj = dflatmaj = {1: csharp4, 3: f4, 5: gsharp4}
    dsharpmaj = eflatmaj = {1: dsharp4, 3: fsharp4, 5: asharp4}
    fsharpmaj = gflatmaj = {1: fsharp4, 3: asharp4, 5: csharp4 + octave}
    gsharpmaj = aflatmaj = {1: gsharp4, 3: c4, 5: dsharp4 + octave}
    asharpmaj = bflatmaj = {1: asharp4, 3: csharp4 + octave, 5: f4 + octave}
    
    csharpmin = dflatmin = {1: csharp4, 3: e4, 5: gsharp4}
    dsharpmin = eflatmin = {1: dsharp4, 3: f4, 5: asharp4}
    fsharpmin = gflatmin = {1: fsharp4, 3: a4, 5: csharp4 + octave}
    gsharpmin = aflatmin = {1: gsharp4, 3: b4, 5: dsharp4 + octave}
    asharpmin = bflatmin = {1: asharp4, 3: c4 + octave, 5: f4 + octave}

    @classmethod
    def stepup(cls, note, num_steps=0):
       return note + (cls.octave * num_steps)

    @classmethod
    def stepdown(cls, note, num_steps=0):
       return note - (cls.octave * num_steps)

    @classmethod
    def chordstepup(cls, chord, num_steps=0):
       return {k: v + (cls.octave * num_steps) for k, v in chord.items()}
    
    @classmethod
    def chordstepdown(cls, chord, num_steps=0):
       return {k: v - (cls.octave * num_steps) for k, v in chord.items()}

def boysALiar():
    piano = 40 # soft
    mezzopiano = 60
    # flatten b
    mw = MidiWriter(tracknames=['L', 'R'])
    def liststepup(lst, step=1):
        return list(map(lambda x: Chords.stepup(x, step), lst))

    # track0 = L; track1 = R
    def intro():
        mw.write_note(0, Chords.stepdown(Chords.bflat4, 2), 0, duration=4, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.bflat4, 1), 0, duration=4, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.f4, 1), 0, duration=4, volume=mezzopiano)
        mw.write_note(1, Chords.d4, 0, duration=4, volume=mezzopiano)

        ## 
        mw.write_note(0, Chords.stepdown(Chords.f4, 2), 4, duration=2, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.c4, 1), 4, duration=2, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.f4, 1), 4, duration=2, volume=mezzopiano)
        mw.write_note(1, Chords.stepdown(Chords.a4, 1), 4, duration=2, volume=mezzopiano)
        
        mw.write_note(0, Chords.stepdown(Chords.c4, 2), 6, duration=2, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.c4, 1), 6, duration=2, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.e4, 1), 6, duration=2, volume=mezzopiano)
        mw.write_note(1, Chords.stepdown(Chords.g4, 1), 6, duration=2, volume=mezzopiano)

        ##
        mw.write_note(0, Chords.stepdown(Chords.bflat4, 2), 8, duration=4, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.bflat4, 1), 8, duration=4, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.f4, 1), 8, duration=4, volume=mezzopiano)
        mw.write_note(1, Chords.stepdown(Chords.d4, 1), 8, duration=4, volume=mezzopiano)
        
        ##
        mw.write_note(0, Chords.stepdown(Chords.f4, 2), 12, duration=2, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.c4, 1), 12, duration=2, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.f4, 1), 12, duration=2, volume=mezzopiano)
        mw.write_note(1, Chords.stepdown(Chords.a4, 1), 12, duration=2, volume=mezzopiano)
        
        mw.write_note(0, Chords.stepdown(Chords.c4, 2), 14, duration=2, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.c4, 1), 14, duration=2, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.e4, 1), 14, duration=2, volume=mezzopiano)
        mw.write_note(1, Chords.stepdown(Chords.g4, 1), 14, duration=2, volume=mezzopiano)
        
        ## 
        mw.write_note(0, Chords.stepdown(Chords.c4, 2), 16, duration=2, volume=mezzopiano)
        mw.write_note(0, Chords.stepdown(Chords.c4, 1), 16, duration=2, volume=mezzopiano)

        mw.write_note(1, Chords.stepdown(Chords.e4, 1), 16, duration=4, volume=mezzopiano)
        mw.write_note(1, Chords.stepdown(Chords.g4, 1), 16, duration=4, volume=mezzopiano)
        return 16+4

    def verse(offset_bar=0, alt=False, melody_aug=False):
        # Track 1 in C4 - C5  # Track 2 C3 - C4
        # RH
        run4 = [Chords.a4, Chords.g4, Chords.f4, Chords.e4, Chords.d4, Chords.c4, Chords.stepdown(Chords.a4, 1), Chords.c4]
        run5 = list(map(lambda x: Chords.stepup(x, 1), run4))
        run5_durations = [Duration.sixtnth, Duration.eighth, Duration.eighth, Duration.eighth, Duration.threesixtnth, Duration.eighth, Duration.eighth, Duration.eighth]  
        
        time = 0 + offset_bar
        if melody_aug:
            mw.write_note(1, run5[-1], time, duration=Duration.half, volume=piano)
        for dur, note in zip(run5_durations, run5):
            mw.write_note(1, note, time, duration=dur, volume=piano)
            time += dur  

        run5 = [ Chords.g4, Chords.f4, Chords.e4, Chords.d4, Chords.c4 ]
        if alt:
            run5.append(Chords.stepdown(Chords.a4, 1))
        run5 = list(map(lambda x: Chords.stepup(x, 1), run4))
        run5_durations = [ Duration.sixtnth, Duration.eighth, Duration.eighth, Duration.eighth, Duration.sixtnth + Duration.half ]
        if alt:
            run5_durations.pop()
            run5_durations.extend([Duration.quarter + Duration.sixtnth, Duration.quarter])

        if melody_aug:
            mw.write_note(1, Chords.stepup(Chords.c4, 1), time, duration=Duration.half, volume=piano)
        for dur, note in zip(run5_durations, run5):
            mw.write_note(1, note, time, duration=dur, volume=piano)
            time += dur

        # LH
        # F3 Bb3 D4 -  
        time = 0 + offset_bar
        bflat3_maj_f3_root = { 1: Chords.stepdown(Chords.f4, 1), 2: Chords.stepdown(Chords.bflat4, 1), 3: Chords.d4 }
        cmaj3_g3_root = { 1: Chords.stepdown(Chords.g4, 1), 2: Chords.c4, 3: Chords.e4 }
        
        mw.write_chord(0, bflat3_maj_f3_root, time, duration=4, volume=piano)

        mw.write_chord(0, Chords.chordstepdown(Chords.fmaj, 1), time+4, duration=2, volume=piano)
        mw.write_chord(0, cmaj3_g3_root, time+6, duration=2, volume=piano)
        print(time+8)
        return time+8

    def chorus(offset_bar=0, alt=False):
        # RH
        time = 0 + offset_bar
        mw.write_note(1, Chords.c4, time, duration=Duration.eighth + Duration.quarter, volume=piano)
        mw.write_note(1, Chords.f4, time, duration=Duration.eighth + Duration.quarter, volume=piano)
        
        time += Duration.quarter + Duration.eighth
        run1 = [Chords.stepdown(Chords.a4, 1), Chords.stepdown(Chords.a4, 1), Chords.c4, Chords.d4, Chords.c4]
        dur1 = [Duration.eighth] * 4
        dur1.append(Duration.quarter + Duration.eighth + Duration.eighth)

        if alt == 1:
            run1 = liststepup(run1)
            run1.pop()
            run1.append(liststepup([Chords.stepdown(Chords.f4, 1), Chords.stepdown(Chords.a4, 1), Chords.c4]))
        elif alt == 2:
            run1 = [Chords.stepup(Chords.d4, 1), Chords.f4, Chords.e4, Chords.f4, Chords.f4, Chords.f4]

        run2 = [Chords.stepdown(Chords.a4, 1), Chords.stepdown(Chords.a4, 1), Chords.c4, Chords.e4, Chords.d4]
        if alt == 1:
            run2 = liststepup(run2)
            run2.pop()
            run2.append(liststepup([Chords.stepdown(Chords.f4, 1), Chords.stepdown(Chords.a4, 1), Chords.d4]))
        elif alt == 2:
            run2 = [Chords.f4, Chords.g4, Chords.e4, Chords.e4, Chords.e4]
            run3 = [Chords.f4, Chords.e4, Chords.f4, Chords.f4, Chords.f4]
            run4 = [Chords.f4, Chords.g4, Chords.e4, Chords.e4, Chords.e4]

        run4_2 = [Chords.f4, Chords.g4, [Chords.c4, Chords.a4], Chords.g4, Chords.f4, Chords.e4]

        if alt == 1:
            run4_2 = [Chords.f4, Chords.g4, 0, Chords.g4, Chords.f4, Chords.e4] 
            run4_2 = liststepup(run4_2)
            run4_2[2] = liststepup([Chords.c4, Chords.a4])

        dur2 = [Duration.eighth] * 6

        runs = [run1, run2, run1, run4_2]
        if alt == 2:
            runs = [run1, run2, run3, run4]
            dur = [Duration.eighth] * 3
            dur.append(Duration.eighth + Duration.eighth)
            dur.append(Duration.quarter)
            dur.append(Duration.eighth + Duration.eighth)
            for i, run in enumerate(runs):
                if i > 0:
                    dur = dur[1:]
                volume = piano
                for d, note in zip(dur, run): 
                    if type(note) == list:
                        for n in note:
                            mw.write_note(1, n, time, duration=d, volume=volume)
                            mw.write_note(1, n, time, duration=d, volume=volume)
                    else:
                        mw.write_note(1, note, time, duration=d, volume=volume)
                    time += d
                    volume += 5

                
        else:
            for i,run in enumerate(runs):
                if i == 3:
                    dur1.pop()
                    dur1.append(Duration.quarter)
                    dur = dur2
                dur = dur1
                volume=piano
                for d, note in zip(dur, run): 
                    if type(note) == list:
                        for n in note:
                            mw.write_note(1, n, time, duration=d, volume=volume)
                            mw.write_note(1, n, time, duration=d, volume=volume)
                    else:
                        mw.write_note(1, note, time, duration=d, volume=volume)
                    time += d
                    volume += 5

        # LH
        if alt == 1:
            run1_1 = [Chords.stepdown(Chords.bflat4, 1), Chords.f4, Chords.stepup(Chords.c4, 1), Chords.f4]
            run1_2 = [Chords.stepdown(Chords.bflat4, 1), Chords.f4, Chords.stepup(Chords.d4, 1), Chords.f4]
            run2_1 = [Chords.c4, Chords.g4, Chords.stepup(Chords.c4, 1), Chords.g4]
            run2_2 = [Chords.c4, Chords.g4, Chords.stepup(Chords.d4, 1), Chords.g4]
            run3_1 = [Chords.d4, Chords.a4, Chords.stepup(Chords.d4, 1), Chords.a4]
            run3_2 = [Chords.d4, Chords.a4, Chords.stepup(Chords.e4, 1), Chords.a4]
            run4_1 = [Chords.f4, Chords.a4, Chords.stepup(Chords.c4,1), Chords.a4]
            run4_2 = [Chords.c4, Chords.g4, Chords.stepup(Chords.c4,1), Chords.g4]

            runs = [run1_1, run1_2, run2_1, run2_2, run3_1, run3_2, run4_1, run4_2]
            
        elif alt == 2:
            run1_1 = [Chords.stepdown(Chords.bflat4, 1), Chords.f4, Chords.stepup(Chords.c4, 1), Chords.f4]
            run1_2 = [Chords.stepdown(Chords.bflat4, 1), Chords.f4, Chords.stepup(Chords.d4, 1), Chords.f4]
            run2_1 = [Chords.c4, Chords.g4, Chords.stepup(Chords.c4, 1), Chords.g4]
            run2_2 = [Chords.c4, Chords.g4, Chords.stepup(Chords.d4, 1), Chords.g4]
            run3_1 = [Chords.d4, Chords.a4, Chords.stepup(Chords.c4, 1), Chords.a4]
            run3_2 = [Chords.d4, Chords.a4, Chords.stepup(Chords.d4, 1), Chords.a4]
            run4_1 = [Chords.f4, Chords.a4, Chords.stepup(Chords.c4,1), Chords.a4]
            run4_2 = [Chords.c4, Chords.g4, Chords.stepup(Chords.c4,1), Chords.g4]
         
            runs = [run1_1, run1_2, run2_1, run2_2, run3_1, run3_2, run4_1, run4_2]
        else:
            run1 = [Chords.stepdown(Chords.bflat4, 1), Chords.f4, Chords.bflat4, Chords.f4]
            run2 = [Chords.c4, Chords.e4, Chords.g4, Chords.e4]
            run3 = [Chords.d4, Chords.f4, Chords.a4, Chords.f4]
            run4 = [Chords.stepdown(Chords.f4, 1), Chords.c4, Chords.f4, Chords.c4]
            run4_2 = [Chords.g4, Chords.c4, Chords.a4, Chords.c4]

            runs = [run1, run1, run2, run2, run3, run3, run4, run4_2]

        time = 0 + offset_bar
        for run in runs:
            run = liststepup(run, -1)
            volume = piano
            for note in run:
                mw.write_note(0, note, time, duration=Duration.eighth, volume=volume)
                time += Duration.eighth
                volume += 5

        return time

    t = intro()
    mw.alter_tempo(120, t)
    t = verse(t)
    t = verse(t, alt=True) # Ends on 36
    t = verse(t, melody_aug=True)
    t = verse(t, melody_aug=True, alt=True)
    t = chorus(t)
    t = chorus(t, alt=1)
    t = chorus(t, alt=2)
        
    mw.write_out("boysaliar.mid") 


if __name__ == "__main__":
    boysALiar()
   