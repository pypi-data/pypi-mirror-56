import re
import os
import json
import textract

from collections import OrderedDict
from pathlib import Path

#text = "some. txt. that's punc. 1. Non punctuated words"
#p = re.compile(r'.*\d+\.[ ]*([\w+ ]+)')
#
#text = '1. 2.\n3.'
#p = re.compile(r'^\d+\.', flags=re.MULTILINE)
#

#text = 'F    I'
#p = re.compile('([CEFIW ]+)$')
#
#matches = p.findall(text)
#print("There are {} matches".format(len(matches)))
#for match in matches:
#    print(match)

#text = '...'
#print(text.replace('.', '\\.'))

#fn = 'locations.txt'
#path = os.path.join(os.getcwd(), fn)
#
#locs = ''
#with open(path) as f:
#    locs = f.read()
#
##locs = locs.split('\n')[:-1]
##locs.sort()
##locs = '\n'.join(locs)
##
##with open(path, 'w') as f:
##    f.write(locs)
#
#fn = 'geography.txt'
#path = os.path.join(os.getcwd(), fn)
#
#geo = ''
#with open(path) as f:
#    geo = f.read()
#
#key = {}
#rkey = {}
#for abbr, loc in zip(geo.split('\n')[:-1], locs.split('\n')[:-1]):
#    key[abbr] = loc
#    rkey[loc] = abbr
#
#fn = 'key.json'
#path = os.path.join(os.getcwd(), fn)
#with open(path, 'w') as f:
#    f.write(json.dumps(key))
#
#fn = 'rkey.json'
#path = os.path.join(os.getcwd(), fn)
#with open(path, 'w') as f:
#    f.write(json.dumps(rkey))
#s = """1. Leaf blades coriaceous, leaves thickened (0.15--0.3 mm thick), margins distinctly sinuate,
#surfaces dull to glossy adaxially, glabrous or hairy abaxially and adaxially; arid regions of
#Oklahoma, Texas ................................................................................................. 1. Cercis canadensis (in part)
#1. Leaf blades thin, leaves (0.05--0.25 mm thick) to subcoriaceous, margins flat, surfaces
#usually dull (sometimes slightly reflective but not glossy), glabrous or hairy abaxially,
#glabrous adaxially; s Canada, c, e United States, w United States (California, Oregon,
#Intermountain areas of Arizona, Nevada, Utah).
#
#
#Cercis05agal (Ballenger/Vincent) -- Fabaceae
#Volumes 10-11
#
#TaxonEds: Vincent et al.
#TechEd: Hill
#
#Page 2 of 8
#26 May 2019
#
#2. Leaf blade apex usually obtuse to acuminate, sometimes retuse; adaxial surface dull,
#abaxial surface glabrous or hairy, often much lighter in color; calyx 5--6.8 mm wide;
#s Canada, c, e United States............................................................................ 1. Cercis canadensis (in part)
#2. Leaf blade apex emarginate to retuse, adaxial surface dull or slightly reflective,
#abaxial surface glabrous or hairy, both surfaces nearly concolor; calyx 6.4--10 mm
#wide; w United States (California, Intermountain areas of Arizona, Nevada, Utah).
#3. Calyx 6.4--9.2 mm wide; banner 3.4--5.3 mm wide, wings 4.7--6.5 mm, keel 5.8-7.5 mm wide; California, Oregon ........................................................................2. Cercis occidentalis
#3. Calyx 8.4--10 mm wide; banner 4.9--6.3 mm wide, wings 7.2--9 mm, keel 7.2-8.9 mm wide; Intermountain region of Arizona, Nevada, Utah .............................. 3. Cercis orbiculata
#"""
#p = re.compile(r'\d+\.[ ]*([A-Za-z]+[A-Za-z ]*)'+
#               r'[ ]*(?:\(in part\))?$',
#        flags=re.MULTILINE)
#print(list(OrderedDict.fromkeys(p.findall(s))))

#s = ':C E'
#id_pattern = re.compile(r'([CEFIW ]+)$')
#matches = id_pattern.findall(s)
#print(matches)

#s = """1a. Cercis canadensis Linnaeus subsp. canadensis
#
#F
#
#Cercis canadensis var. pubescens Pursh; C. dilatata Greene;
#C. ellipsoidea Greene; C. georgiana Greene
#
#Shrubs or trees. Twigs glabrous. Leaves: petiole 19-50 mm, glabrous, or with sparse, pilose hairs distally;
#blade dull green abaxially, usually darker green
#adaxially, membranous to subcoriaceous, thin (0.05-0.25 mm), blades suborbiculate to reniform, 47--110 x
#56--116 mm, base cordate or nearly truncate, margins
#flat, apex acuminate or obtuse, surfaces glabrous or
#hairy abaxially (hairs sometimes restricted to veins or
#vein axils), glabrous adaxially. Pedicels glabrous.
#Flowers: calyx 5--6.8 mm wide; banner 4.7--6.5 x 3.3-5.8 mm, wings 4.5--6.7 x 3.3--4.8 mm, keel 6.5--8.2 x
#4.7--7 mm. Legumes dull brown, 50--109 x 9--19 mm,
#mostly glabrous. 2n = 14.
#Flowering Mar--May. Forests, forest edges; 0--1000
#m; Ont.; Ala., Ark., Conn., Del., D.C., Fla., Ga., Ill.,
#Ind., Iowa, Kans., Ky., La., Md., Mass., Mich., Miss.,
#Mo., Nebr., N.J., N.C., Ohio, Okla., Pa., S.C., Tenn.,
#Tex., Utah, Va., W.Va., Wis.; Mexico (Nuevo León,
#Tamaulipas).
#The only presumed native Canadian record of
#subsp. canadensis is from 1892 on Pelee Island,
#Ontario, where it was collected by John Macoun and
#has not been seen since; it occasionally escapes from
#cultivation in southern Ontario (G. E. Waldron 2003).
#The Utah populations are escapes from cultivation (S.
#L. Welsh et al. 2008).
#Siliquastrum cordatum Moench is an illegitimate,
#superfluous name that pertains here."""
#
#encoding = 'utf-8'
#fn = 'Cercis05agal.pdf'
#path = os.path.join(os.getcwd(), fn)
#text = textract.process(path, encoding=encoding).decode(encoding)
#
#flower_pattern = re.compile(r'(Flowering .*?\.\n)', re.DOTALL)
#matches = flower_pattern.findall(s)
#for match in matches:
#    print(match)

#s = """Cercis05agal (Ballenger/Vincent) -- Fabaceae
#Volumes 10-11
#
#TaxonEds: Vincent et al.
#TechEd: Hill
#
#Page 1 of 8
#26 May 2019
#
#1. CERCIS Linnaeus, Sp. Pl. 1: 374. 1753; Gen. Pl. ed. 5, 176. 1754 * Redbud [Greek
#kerkis, weaver’s shuttle, alluding to shape of fruit]
#Julie A. Ballenger
#Michael A. Vincent
#Siliquastrum Duhamel
#Trees or shrubs, unarmed. Stems gray or gray-brown to red-brown, twigs dark red-brown,
#erect, hairy or glabrous. Leaves alternate, 2-ranked, unifoliolate; stipules present, caducous,
#ovate, membranous; petiolate, petiole glabrous or hairy; pulvinate proximally and distally;
#blade margins entire, surfaces glabrous or hairy. Inflorescences cauliflorous or from short
#shoots on wood one year or older, fasciculate; bracts present, caducous.
#Flowers
#pseudopapilionaceous, appearing before leaves, banner enclosed by wings, wings enclosed by
#keel petals; calyx slightly zygomorphic, enlarged adaxially, persistent, lobes 5, connate,
#magenta, rounded to broadly triangular; corolla: petals 5, free, clawed, usually pink, rarely
#white, [magenta], inserted on floral cup; keel locked abaxially by folds in each petal forming a
#pocket; stamens 10, distinct, enclosed in keel pocket; filaments hairy proximally, inserted on
#floral cup; anthers versatile, 2-locular, dehiscing by longitudinal slits; ovary laterally
#compressed, short stalked; style tapering to a narrow tube, stigma triangular, terminal. Fruits
#legumes, sessile or short-stipitate, brown to red-brown or dark magenta, compressed laterally,
#lanceolate, narrowly winged on prominently veined abaxial suture, dull or glossy, indehiscent
#or dehiscent, if dehiscent, opening on one or both margins, glabrous or sparsely hairy. Seeds
#3--7, red-brown, laterally compressed, with circular hilum, funicular aril lobes absent,
#orbicular. x = 7.
#Species 10 (3 in the flora): North America, n Mexico, e, s Europe, Asia.
#Cercis is found in mesic to arid habitats in North America and Eurasia. North American
#Cercis appears to have diverged from western Eurasian Cercis in the middle Miocene (P. A.
#Fritsch and B. C. Cruz 2012). Cercis spokanensis Knowlton is a fossil taxon from the Pacific
#Northwest.
#In spite of the inclusion of Cercis in floras of New Mexico (I. Tidestrom and T. Kittell
#1941; W. C. Martin and C. R. Hutchins 1980; K. W. Allred and R. D. Ivey 2012), no
#specimens of Cercis outside cultivation in that state could be located.
#SELECTED REFERENCES Ballenger, J. A. 1992. A Biosystematic Revision of the Genus Cercis L. (Leguminosae) in North
#America. Ph.D. dissertation. Miami University. Fritsch, P. W. and B. C. Cruz. 2012. Phylogeny of Cercis based on DNA
#sequences of nuclear ITS and four plastid regions: Implications for transatlantic historical biogeography. Molec. Phylogen. Evol.
#62: 816--825. Hopkins, M. 1942. Cercis in North America. Rhodora 44: 193--211.
#
#1. Leaf blades coriaceous, leaves thickened (0.15--0.3 mm thick), margins distinctly sinuate,
#surfaces dull to glossy adaxially, glabrous or hairy abaxially and adaxially; arid regions of
#Oklahoma, Texas ................................................................................................. 1. Cercis canadensis (in part)
#1. Leaf blades thin, leaves (0.05--0.25 mm thick) to subcoriaceous, margins flat, surfaces
#usually dull (sometimes slightly reflective but not glossy), glabrous or hairy abaxially,
#glabrous adaxially; s Canada, c, e United States, w United States (California, Oregon,
#Intermountain areas of Arizona, Nevada, Utah).
#"""
#genus_pattern = re.compile(r'^[ ]*\d+\.[ ]*([A-Z]+)', flags=re.MULTILINE)
#def build_key_pattern(genus):
#    key_pattern = re.compile(r'^[ ]*\d+\.[ ]*[\s\S]+\d+\.[ ]*('+genus+
#                             r' [a-z]+)(?: \(in part\))?\n',
#                             flags=re.MULTILINE)
#    return key_pattern
#
#def main():
#    genus = genus_pattern.search(s)
#    if not genus:
#        print("Couldn't find genus name")
#        return
#    genus = genus[1] # get the first parenthiszed subgroup as a string
#    genus = genus[0]+genus[1:].lower() # De-"caps lock" the string
#
#    key_pattern = build_key_pattern(genus)
#    print(key_pattern.pattern)
#    keys = key_pattern.findall(s)
#    print(keys)
#
#main()

print("File path:", Path(__file__).absolute())
