import csv,glob,sys,collections
S=sys.argv[1]; stage=sys.argv[2]
scr={r['key']:r for r in csv.DictReader(open('slr/data/screening.csv'))}
r2={}
for f in glob.glob(f"{S}/{stage}_b*_r2.csv"):
    for r in csv.DictReader(open(f)): r2[r['key']]=r
def k(pairs):
    n=len(pairs); po=sum(a==b for a,b in pairs)/n
    ca=collections.Counter(a for a,_ in pairs); cb=collections.Counter(b for _,b in pairs)
    pe=sum(ca[x]*cb[x] for x in set(ca)|set(cb))/n/n
    return n,po,(po-pe)/(1-pe)
if stage=='abs':
    m=lambda d:'exclude' if d=='exclude' else 'pass'
    pairs=[(m(scr[x]['abs_decision']),m(r['decision'].strip().lower())) for x,r in r2.items()]
else:
    pairs=[(scr[x]['ft_decision'],r['decision'].strip().lower()) for x,r in r2.items()]
n,po,kap=k(pairs)
print(stage,'n=%d agreement=%.3f kappa=%.3f'%(n,po,kap))
print(collections.Counter(pairs))
dis=[(x,scr[x]['abs_decision' if stage=='abs' else 'ft_decision'],scr[x]['abs_reason' if stage=='abs' else 'ft_reason'],r['decision'],r['reason'],scr[x]['title'][:70]) for x,r in r2.items() if (m(scr[x]['abs_decision'])!=m(r['decision'].strip().lower()) if stage=='abs' else scr[x]['ft_decision']!=r['decision'].strip().lower())]
# final-outcome view for abs disagreements: was R1-excluded record actually in corpus? / R1-passed record finally included?
for d in dis: print(d, "| final:", scr[d[0]]["ft_decision"] or "-", "| r2:", r2[d[0]]["justification"][:120])
