"""Recompute proposal arithmetic from hand-extracted source data; no evaluator re-scoring."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
cases=json.loads((root/'REFERENCE_GEOMETRY.json').read_text())
checks={}
for case,d in cases.items():
 plates=[(name,i+1,w,l,m['nfa'][i]) for name,m in d['masses'].items() for i,(w,l) in enumerate(m['plates'])]
 gfa=sum(w*l for _,_,w,l,_ in plates); nfa=sum(n for *_,n in plates)
 ratios={name:min(m['plates'][0])/max(m['plates'][0]) for name,m in d['masses'].items()}
 splits={}
 for key,total in [('core_floor_nfa',14280),('sped_floor_nfa',5610),('custodial_floor_nfa',2200)]:
  v=d[key]; occupied=[i for i,n in enumerate(v) if n]
  splits[key]={'sum':sum(v),'contiguous':occupied==list(range(min(occupied),max(occupied)+1)), 'minimum_occupied_nfa':min(n for n in v if n)}
  assert sum(v)==total and splits[key]['contiguous'] and splits[key]['minimum_occupied_nfa']>=753
 assert nfa==44270 and gfa==d['reported_gfa']
 assert all(.4-1e-9<=r<=.625+1e-9 for r in ratios.values())
 assert all(l*.3048<=60 for _,_,w,l,_ in plates)
 assert all(n<=w*l for _,_,w,l,n in plates)
 assert d['gross_basis']*.97<=gfa<=d['gross_basis']*1.03
 checks[case]={'gfa_recomputed':gfa,'nfa_recomputed':nfa,'gross_basis':d['gross_basis'],'lower_band_margin_sf':round(gfa-d['gross_basis']*.97,4),'upper_band_margin_sf':round(d['gross_basis']*1.03-gfa,4),'principal_ratios':ratios,'ratio_interpretation':d['ratio_basis'],'plate_ratios':[{'mass':name,'floor':i,'ratio':min(w,l)/max(w,l)} for name,i,w,l,n in plates], 'split_checks':splits,'plate_use':[{'mass':name,'floor':i,'gross':w*l,'scheduled_nfa':n,'nfa_fraction':n/(w*l)} for name,i,w,l,n in plates], 'anchor_evidence':{k:'explicit dimensions' if d[k] else 'minimum-size commitment; final dimensions absent' for k in ['gym','cafeteria']},'wide_masses_with_pinned_daylight_departments':[name for name,m in d['masses'].items() if m['daylight'] and any(w>90 for w,l in m['plates'])], 'realized_room_fit':'not established by this arithmetic audit'}
assert len(checks)==12
(root/'NUMERIC_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('12 cases: area totals, declared principal ratios, length caps, split totals and necessary plate-area bounds verified. Actual room fit remains unverified.')
